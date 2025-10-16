import threading
import json
from restaurant_booking.agents.restaurant_booking_agent import RestaurantBookingAgent
from langchain_core.callbacks import BaseCallbackHandler
from queue import Queue


class StreamingCallbackHandler(BaseCallbackHandler):
    def __init__(self, queue: Queue):
        self.queue = queue

    def send(self, event_type: str, content=None):
        self.queue.put({"type": event_type, "content": content})

    def on_chain_start(self, *args, **kwargs):
        self.queue.put({"type": "start"})

    def on_llm_new_token(self, token: str, **kwargs):
        self.queue.put({"type": "token", "content": token})

    def on_chain_end(self, *args, **kwargs):
        self.queue.put({"type": "end"})
    
    def on_chain_error(self, error, **kwargs):
        self.queue.put({"type": "error", "content": str(error)})

class RestaurantBookingChatService:
    def __init__(self):
        self.queue = Queue()
        self.callback_handler = StreamingCallbackHandler(self.queue)
        self.agent_wrapper = RestaurantBookingAgent(callbacks=[self.callback_handler], queue=self.queue)
        self.agent = self.agent_wrapper.agent

    def chat(self, request, data):
        user_input = data.get("user_input", "")
        chat_history = data.get("chat_history", [])

        # Load chat history into memory if provided
        if chat_history:
            self._load_chat_history_into_agent_memory(self.agent, chat_history) 

        # Start the agent execution in a separate thread to allow streaming
        def run_agent():
            try:
                result = self.agent_wrapper.run(user_input)
            except Exception as e:
                print(e)
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
