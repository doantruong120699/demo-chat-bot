import json
import time
from django.http import StreamingHttpResponse
from api_chat_bot import settings
from ..models import Chat, Message
from ..serializers import ChatHistoryListSerializer, ChatHistoryDetailSerializer
from agents.text2sql import Text2SQL
from common.tools.sql_tool import execute_sql_query, connect_to_db
from openai import OpenAI
from agents.pscd_agent import PscdAgent


class DbInteractAiChatService:
    def __init__(self):
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        model = "gpt-4o-mini"

        self.llm = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.agent = PscdAgent().agent

        # Configurable streaming delay (in seconds)
        self.streaming_delay = 0.05  # 50ms default delay

        self.text2sql = Text2SQL(model=model)
        self.conn = connect_to_db()
        self.model = model

    def get_chat_history(self, user):
        chats = Chat.objects.filter(user=user, is_deleted=False)
        return ChatHistoryListSerializer(chats, many=True).data

    def get_chat_history_detail(self, chat_id):
        chat = Chat.objects.get(uuid=chat_id, is_deleted=False)
        return ChatHistoryDetailSerializer(chat).data

    def chat(self, request, data):
        user = request.user
        chat_id = data.get("chat_id", None)
        message = data.get("message", None)
        chat = self.get_chat_by_id(user, chat_id, message)
        history = self.get_history_by_chat_id(chat_id)

        return self.stream_chat(data, chat, history)

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

    def stream_chat(self, input_data, chat, history):
        """
        Stream chat response using LangChain and OpenAI with whitepaper context.

        Args:
            input_data: Dictionary containing user input, typically {'message': 'user message'}
        """
        user_message = input_data.get("message", "")

        if not user_message:
            return self._create_error_response("No message provided")

        def event_stream():
            try:
                # Initialize output_message
                messages = self._build_messages(history, user_message)

                answer_stream = self.agent.invoke({"input": user_message})
                print("================================================")
                print(answer_stream)
                print("================================================")

                # Stream the answer generation
                # answer_stream = self.llm.chat.completions.create(
                #     model=self.model,
                #     messages=[*messages, {"role": "user", "content": answer_prompt}],
                #     stream=True,
                # )

                for chunk in answer_stream["output"]:
                    yield self._format_stream_data("token", content=chunk)
                    time.sleep(self.streaming_delay)
                self._save_conversation_messages(
                    chat, user_message, answer_stream["output"]
                )

            except Exception as e:
                print("================================================")
                print(e)
                print("================================================")
                error_message = self._handle_streaming_error(e)
                yield self._format_stream_data("error", error=error_message)
            finally:
                print("================================================")
                print("Stream chat completed")
                print("================================================")
                yield self._format_stream_data("end")

        response = StreamingHttpResponse(
            event_stream(), content_type="text/event-stream"
        )
        response["Cache-Control"] = "no-cache"
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "Cache-Control"
        return response

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

    def _format_stream_data(self, data_type: str, **kwargs) -> str:
        """Format streaming data as Server-Sent Events."""
        data = {"type": data_type}
        data.update(kwargs)
        return f"data: {json.dumps(data)}\n\n"

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

    def _create_error_response(self, error_message: str):
        """Create an error response for invalid requests."""

        def error_stream():
            yield self._format_stream_data("error", error=error_message)

        response = StreamingHttpResponse(
            error_stream(), content_type="text/event-stream"
        )
        response["Cache-Control"] = "no-cache"
        return response

    def _save_conversation_messages(self, chat, user_message: str, bot_message: str):
        """Save both user and bot messages to the database."""
        self.save_message(chat, user_message, Message.Sender.HUMAN)
        self.save_message(chat, bot_message, Message.Sender.BOT)

    def save_message(self, chat, message, sender):
        Message.objects.create(chat=chat, message=message, sender=sender)
