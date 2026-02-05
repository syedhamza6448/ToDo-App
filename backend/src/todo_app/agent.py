import json
import os
import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolParam
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from sqlmodel import Session, select

from todo_app.models import Conversation, Message
from todo_app.database import engine

# Configuration
MCP_SERVER_SCRIPT = "todo_app.mcp"

class TodoAgent:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o"
    
    async def _get_mcp_tools(self, session: ClientSession) -> List[ChatCompletionToolParam]:
        """Fetch tools from MCP server and convert to OpenAI format."""
        mcp_tools = await session.list_tools()
        openai_tools: List[ChatCompletionToolParam] = []
        
        for tool in mcp_tools.tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
            })
        return openai_tools

    async def _save_message(self, db: Session, conversation_id: int, role: str, content: str):
        """Persist message to database."""
        # Clean up tool calls from content if necessary, or store structured data
        # For simplicity, we store the text content.
        if not content:
            return # Don't save empty content (e.g. from tool calls)
            
        msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        db.add(msg)
        db.commit()

    async def process_message(self, message: str, conversation_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Process a user message:
        1. Load history.
        2. Connect to MCP.
        3. Call LLM.
        4. Execute tools.
        5. Return response.
        """
        # 1. Database & Context
        with Session(engine) as db:
            if conversation_id:
                conversation = db.get(Conversation, conversation_id)
                if not conversation or conversation.user_id != self.user_id:
                    raise ValueError("Conversation not found or access denied.")
            else:
                conversation = Conversation(user_id=self.user_id, title=message[:30])
                db.add(conversation)
                db.commit()
                db.refresh(conversation)
                conversation_id = conversation.id

            # Save user message
            await self._save_message(db, conversation_id, "user", message)
            
            # Load history
            history_msgs = db.exec(
                select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
            ).all()
            
            messages: List[ChatCompletionMessageParam] = [
                {"role": "system", "content": f"You are a helpful task assistant. Today is {datetime.now().strftime('%A, %B %d, %Y')}. You can manage tasks using the available tools."}
            ]
            for msg in history_msgs:
                messages.append({"role": msg.role, "content": msg.content}) # type: ignore

        # 2. Connect to MCP Server
        server_params = StdioServerParameters(
            command="uv",
            args=["run", "python", "-m", MCP_SERVER_SCRIPT],
            env={**os.environ, "MCP_USER_ID": self.user_id} # Pass user context to MCP
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # 3. Get Tools
                tools = await self._get_mcp_tools(session)
                
                # 4. LLM Loop
                while True:
                    response = await self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        tools=tools,
                        tool_choice="auto"
                    )
                    
                    response_message = response.choices[0].message
                    messages.append(response_message)
                    
                    # Check for tool calls
                    if response_message.tool_calls:
                        for tool_call in response_message.tool_calls:
                            # Execute tool
                            tool_name = tool_call.function.name
                            tool_args = json.loads(tool_call.function.arguments)
                            
                            # Call MCP tool
                            result = await session.call_tool(tool_name, arguments=tool_args)
                            
                            # Append result
                            messages.append({
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": tool_name,
                                "content": json.dumps(result.content)
                            })
                    else:
                        # Final response
                        assistant_content = response_message.content or ""
                        
                        # Save assistant response
                        with Session(engine) as db:
                            await self._save_message(db, conversation_id, "assistant", assistant_content)
                            
                        return {
                            "conversation_id": conversation_id,
                            "role": "assistant",
                            "content": assistant_content
                        }

# Example usage (for testing)
if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Mock env for testing
        if not os.environ.get("OPENAI_API_KEY"):
            print("Please set OPENAI_API_KEY")
            return

        agent = TodoAgent(user_id="test-user-1")
        response = await agent.process_message("Add a task to buy milk")
        print("Agent:", response["content"])
        
        response = await agent.process_message("List my tasks", conversation_id=response["conversation_id"])
        print("Agent:", response["content"])

    asyncio.run(main())
