import os
import json
from typing import Optional, AsyncGenerator, Any, List, Dict
from chatkit.server import ChatKitServer, ThreadItem, UserMessageItem, AssistantMessageItem, StreamingResult, NonStreamingResult, Store, Thread, ThreadItem
from fastapi import APIRouter, Request, Response, BackgroundTasks
from fastapi.responses import StreamingResponse
from todo_app.agent import TodoAgent
from todo_app.database import engine
from sqlmodel import Session, select

# --- Concrete Store Implementation ---
class InMemoryStore(Store):
    def __init__(self):
        self.threads: Dict[str, Thread] = {}  # Stores Thread objects by thread_id
        self.thread_items: Dict[str, List[ThreadItem]] = {} # Stores list of ThreadItem for each thread_id
        self.attachments: Dict[str, Any] = {} # Stores attachment data by attachment_id

    async def add_thread_item(self, thread_id: str, item: ThreadItem):
        if thread_id not in self.thread_items:
            self.thread_items[thread_id] = []
        if not any(i.id == item.id for i in self.thread_items[thread_id]):
            self.thread_items[thread_id].append(item)
        await self.save_item(item) # Ensure item is saved if it has persistence needs

    async def delete_thread_item(self, thread_id: str, item_id: str):
        if thread_id in self.thread_items:
            initial_len = len(self.thread_items[thread_id])
            self.thread_items[thread_id] = [i for i in self.thread_items[thread_id] if i.id != item_id]
            return len(self.thread_items[thread_id]) < initial_len
        return False

    async def delete_thread(self, thread_id: str):
        if thread_id in self.threads:
            del self.threads[thread_id]
            if thread_id in self.thread_items:
                del self.thread_items[thread_id]
            return True
        return False

    async def load_thread(self, thread_id: str) -> Thread | None:
        return self.threads.get(thread_id)

    async def load_thread_items(self, thread_id: str) -> List[ThreadItem]:
        return self.thread_items.get(thread_id, [])

    async def load_threads(self, limit: int, offset: int) -> List[Thread]:
        all_threads = list(self.threads.values())
        return all_threads[offset : offset + limit]

    async def save_item(self, item: ThreadItem):
        if hasattr(item, 'thread_id') and item.thread_id:
             if item.thread_id not in self.thread_items:
                 self.thread_items[item.thread_id] = []
             if not any(i.id == item.id for i in self.thread_items[item.thread_id]):
                self.thread_items[item.thread_id].append(item)

    async def save_thread(self, thread: Thread):
        self.threads[thread.id] = thread
        if thread.id not in self.thread_items:
            self.thread_items[thread.id] = []

    async def save_attachment(self, attachment: Any): # Use Any as Attachment type might not be directly importable
        self.attachments[attachment.id] = attachment

    async def load_attachment(self, attachment_id: str) -> Any | None: # Use Any for attachment type
        return self.attachments.get(attachment_id)
        
    async def delete_attachment(self, attachment_id: str):
        if attachment_id in self.attachments:
            del self.attachments[attachment_id]
            return True
        return False
    
    async def update_thread_item(self, thread_id: str, item_id: str, updated_item: ThreadItem):
        if thread_id in self.thread_items:
            for i, item in enumerate(self.thread_items[thread_id]):
                if item.id == item_id:
                    self.thread_items[thread_id][i] = updated_item
                    return True
        return False

    async def add_thread_metadata(self, thread_id: str, key: str, value: str):
        thread = await self.load_thread(thread_id)
        if thread and thread.metadata is not None:
            thread.metadata[key] = value
            await self.save_thread(thread)
            return True
        return False
    
    async def update_thread_metadata(self, thread_id: str, key: str, value: str):
        thread = await self.load_thread(thread_id)
        if thread and thread.metadata is not None and key in thread.metadata:
            thread.metadata[key] = value
            await self.save_thread(thread)
            return True
        return False

    # --- Implemented abstract method ---
    async def load_item(self, item_id: str) -> ThreadItem | None:
        # Basic in-memory search for an item across all threads.
        # A more robust implementation would index items.
        for thread_id in self.thread_items:
            for item in self.thread_items[thread_id]:
                if item.id == item_id:
                    return item
        return None

# --- Custom ChatKitServer Implementation ---
class CustomChatKitServer(ChatKitServer):
    def __init__(self):
        # Initialize with the concrete store implementation
        super().__init__(store=InMemoryStore()) 

    async def respond(self, request: str | bytes | bytearray, context: Any) -> StreamingResult | NonStreamingResult:
        user_id = context.get("user_id", "mcp-user")
        agent = TodoAgent(user_id=user_id)
        
        try:
            req_data = json.loads(request)
            message_text = req_data.get("text")
            
            if not message_text:
                raise ValueError("Message text is required.")
            
            conversation_id = req_data.get("conversation_id")

            response = await agent.process_message(message_text, conversation_id=conversation_id)
            
            content = response["content"]
            tools = response.get("tools_used", [])
            if tools:
                content += "\n\n(Tools used: " + ", ".join(tools) + ")"
                
            async def stream_response():
                yield AssistantMessageItem(text=content)

            return StreamingResult(stream_response())

        except Exception as e:
            error_message = f"Error processing message: {str(e)}"
            print(f"Error in respond: {error_message}") 
            async def stream_error():
                yield AssistantMessageItem(text=error_message)
            return StreamingResult(stream_error())

# Initialize ChatKit Server with the custom implementation
chatkit = CustomChatKitServer() 
router = APIRouter()

@router.post("")
@router.post("/")
async def chatkit_endpoint(request: Request):
    body = await request.body()
    context = {"user_id": "mcp-user"} 
    
    try:
        result = await chatkit.process(body, context)
        
        if isinstance(result, StreamingResult):
            return StreamingResponse(result, media_type="text/event-stream")
        elif isinstance(result, NonStreamingResult):
            return Response(content=result.content, media_type="application/json")
        else:
            return Response(content=str(result), media_type="text/plain")
            
    except Exception as e:
        error_message = f"Error in chatkit_endpoint: {str(e)}"
        print(error_message)
        return Response(content=json.dumps({"error": error_message}), status_code=500, media_type="application/json")
