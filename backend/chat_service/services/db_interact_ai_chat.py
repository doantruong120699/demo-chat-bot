import json
import time
import threading
from django.http import StreamingHttpResponse
from ..models import Chat, Message
from ..serializers import ChatHistoryListSerializer, ChatHistoryDetailSerializer
from agents.pscd_agent import PscdAgent
from langchain_core.callbacks import BaseCallbackHandler
from queue import Queue


class StreamingCallbackHandler(BaseCallbackHandler):
    def __init__(self, queue: Queue):
        self.queue = queue
        self.finished = False

    def send(self, event_type: str, content=None):
        self.queue.put({"type": event_type, "content": content})

    def on_chain_start(self, *args, **kwargs):
        self.queue.put({"type": "start"})

    def on_llm_new_token(self, token: str, **kwargs):
        if "image" in token:
            self.queue.put({"type": "image", "content": token})
        if "table" in token:
            self.queue.put({"type": "table", "content": token})
        else:
            self.queue.put({"type": "token", "content": token})

    def on_chain_end(self, *args, **kwargs):
        self.queue.put({"type": "end"})


class DbInteractAiChatService:
    def __init__(self):
        self.queue = Queue()
        self.callback_handler = StreamingCallbackHandler(self.queue)
        self.agent = PscdAgent(callbacks=[self.callback_handler], queue=self.queue).agent

    def get_chat_history(self, user):
        chats = Chat.objects.filter(user=user, is_deleted=False)
        return ChatHistoryListSerializer(chats, many=True).data

    def get_chat_history_detail(self, chat_id):
        chat = Chat.objects.get(uuid=chat_id, is_deleted=False)
        return ChatHistoryDetailSerializer(chat).data

    def chat(self, request, data):
        user = request.user
        chat_id = data.get("chat_id", None)
        user_message = data.get("message", "")
        chat = self.get_chat_by_id(user, chat_id, user_message)
        history = self.get_history_by_chat_id(chat_id)

        self._load_chat_history_into_agent_memory(self.agent, history)

        # Start the agent execution in a separate thread to allow streaming
        def run_agent():
            try:
                result = self.agent.invoke({"input": user_message})
                self._save_conversation_messages(chat, user_message, result["output"])
            except Exception as e:
                self.callback_handler.send("error", str(e))

        # Start agent in background thread
        agent_thread = threading.Thread(target=run_agent)
        agent_thread.start()

        # Stream events from the callback handler
        while True:
            try:
                event = self.callback_handler.queue.get(timeout=1)
                yield f"data: {json.dumps(event)}\n\n"
                if event["type"] == "end" or event["type"] == "error":
                    break
            except:
                # Check if agent thread is still running
                if not agent_thread.is_alive():
                    break

    def get_chat_by_id(self, user, chat_id, title=None):
        return Chat.objects.get_or_create(
            user=user,
            uuid=chat_id,
            is_deleted=False,
            defaults={
                "uuid": chat_id,
                "user": user,
                "title": title if title and len(title) <= 50 else title[:50],
            },
        )[0]

    def get_history_by_chat_id(self, chat_id):
        messages = Message.objects.filter(chat__uuid=chat_id).order_by("created_at")
        # Build history input for LLM as a list of dicts with role and content
        history = []
        for msg in messages:
            if msg.sender == Message.Sender.HUMAN:
                history.append({"role": "user", "content": msg.message})
            else:
                history.append({"role": "assistant", "content": msg.message})
        return history

    def _load_chat_history_into_agent_memory(self, agent, messages):
        """Load chat history into the agent's memory."""
        if not messages:
            return

        # Clear existing memory first
        if hasattr(agent, "memory") and agent.memory:
            agent.memory.clear()

        # Load history into memory
        for msg in messages:
            if msg["role"] == "user":
                agent.memory.chat_memory.add_user_message(msg["content"])
            elif msg["role"] == "assistant":
                agent.memory.chat_memory.add_ai_message(msg["content"])

    def _build_messages(self, history: list, user_message: str) -> list:
        """Build the complete message list for the LLM."""
        system_message = """
        You are a helpful AI assistant for PSCD company. You are developed for PSCD's admin team to interact with the database.
        """
        messages = [{"role": "system", "content": system_message}]

        # Add conversation history
        for hist_msg in history:
            if hist_msg["role"] == "user":
                messages.append({"role": "user", "content": hist_msg["content"]})
            elif hist_msg["role"] == "assistant":
                messages.append({"role": "assistant", "content": hist_msg["content"]})

        # Add current user message
        messages.append({"role": "user", "content": user_message})
        return messages

    def _handle_streaming_error(self, error: Exception) -> str:
        """Handle and format streaming errors."""
        error_message = str(error)

        if "429" in error_message or "Too Many Requests" in error_message:
            return "Rate limit exceeded. Please wait a moment and try again."
        elif "401" in error_message or "Unauthorized" in error_message:
            return "Invalid API key. Please check your OpenAI API key."
        elif "400" in error_message:
            return "Invalid request. Please check your input."
        elif "500" in error_message:
            return "OpenAI service is temporarily unavailable. Please try again later."
        else:
            return f"Error generating response: {error_message}"

    def _save_conversation_messages(
        self, chat, user_message: str, bot_message: str, html_message: str = None
    ):
        """Save both user and bot messages to the database."""
        self.save_message(chat, user_message, Message.Sender.HUMAN)
        self.save_message(chat, bot_message, Message.Sender.BOT, html_message)

    def save_message(self, chat, message, sender, html_message=None):
        Message.objects.create(
            chat=chat, message=message, sender=sender, html_message=html_message
        )
