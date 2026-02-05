import os
import json
from typing import Optional, AsyncGenerator, Any
from chatkit.server import ChatKitServer, ThreadItem, UserMessageItem, AssistantMessageItem, StreamingResult
from fastapi import APIRouter, Request, Response, BackgroundTasks
from fastapi.responses import StreamingResponse
from todo_app.agent import TodoAgent

# Initialize ChatKit Server
chatkit = ChatKitServer()
router = APIRouter()

@chatkit.on_user_message_added()
async def handle_message(message: UserMessageItem, ctx) -> AsyncGenerator[ThreadItem, None]:
    """
    Handle user messages using the TodoAgent logic.
    """
    user_id = ctx.get("user_id", "mcp-user")
    agent = TodoAgent(user_id=user_id)
    
    try:
        # Call agent
        response = await agent.process_message(message.text)
        
        # Build Assistant message
        content = response["content"]
        tools = response.get("tools_used", [])
        if tools:
            # According to ChatKit protocol, we can just yield the message.
            # To show tools specifically, we might need more advanced usage, 
            # but for now, appending to text is a solid way to "Show" them.
            content += "\n\n(Tools used: " + ", ".join(tools) + ")"
            
        yield AssistantMessageItem(text=content)
        
    except Exception as e:
        yield AssistantMessageItem(text=f"Error: {str(e)}")

@router.post("")
@router.post("/")
async def chatkit_endpoint(request: Request):
    """
    FastAPI endpoint that proxies to ChatKitServer.
    """
    body = await request.body()
    # Context can include user_id if we want to pass it from auth
    context = {"user_id": "mcp-user"} 
    
    result = await chatkit.process(body, context)
    
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    else:
        # Non-streaming result
        return Response(content=result.content, media_type="application/json")