from rest_framework import generics, views, status
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from .services.order_service import OrderService
from .models.order import Order
from .models.product import Product
from .models.category import Category
from .serializers import OrderSerializer, ProductSerializer, CategorySerializer
from .agents.fashion_order_agent import FashionOrderAgent
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler
import logging
import time
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StreamingCallbackHandler(BaseCallbackHandler):
    """Custom callback handler for streaming responses"""
    
    def __init__(self, queue):
        self.queue = queue
    
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        self.queue.put(token)


# Store agents by session (in-memory cache)
_agent_cache = {}


# Views
class OrderChatView(views.APIView):
	"""Fashion Order Chat - AI Agent for conversational ordering"""
	
	def post(self, request):
		user_message = request.data.get('message') or request.data.get('user_input')
		chat_history = request.data.get('chat_history', [])
		
		if not user_message:
			return Response({'error': 'Missing message'}, status=status.HTTP_400_BAD_REQUEST)
		
		logger.info(f"User message: {user_message}")
		logger.info(f"Received chat history: {len(chat_history)} messages")
		
		# Get or create session key
		if not request.session.session_key:
			request.session.create()
		session_key = request.session.session_key
		
		# Generator function để stream response
		def event_stream():
			from queue import Queue
			
			# Create queue for streaming
			queue = Queue()
			callback_handler = StreamingCallbackHandler(queue)
			
			try:
				# Get existing agent from cache or create new one
				if session_key not in _agent_cache:
					logger.info(f"Creating new agent for session: {session_key}")
					_agent_cache[session_key] = FashionOrderAgent(callbacks=[callback_handler], queue=queue)
				else:
					logger.info(f"Reusing existing agent for session: {session_key}")
					# Update callbacks for existing agent
					_agent_cache[session_key].callbacks = [callback_handler]
					_agent_cache[session_key].llm.callbacks = [callback_handler]
				
				agent = _agent_cache[session_key]
				
				# Restore history from frontend if provided and agent memory is empty
				if chat_history and len(agent.agent.memory.chat_memory.messages) == 0:
					logger.info("Restoring chat history from frontend")
					from langchain_core.messages import HumanMessage, AIMessage
					
					for msg in chat_history[:-1]:  # Exclude current message
						role = msg.get('role', 'user')
						content = msg.get('content', '')
						
						if role == 'user':
							agent.agent.memory.chat_memory.add_message(HumanMessage(content=content))
						elif role in ['assistant', 'bot']:
							agent.agent.memory.chat_memory.add_message(AIMessage(content=content))
					
					logger.info(f"Restored {len(chat_history)-1} messages to agent memory")
				
				# Run agent in separate thread
				import threading
				agent_response = {"output": "", "error": None}
				
				def run_agent():
					try:
						result = agent.run(user_message)
						agent_response["output"] = result.get("output", "")
					except Exception as e:
						logger.error(f"Agent error: {e}")
						agent_response["error"] = str(e)
				
				thread = threading.Thread(target=run_agent)
				thread.start()
				
				# Stream tokens from queue
				while thread.is_alive() or not queue.empty():
					try:
						token = queue.get(timeout=0.1)
						yield f"data: {{\"type\": \"token\", \"content\": {json.dumps(token)} }}\n\n"
						time.sleep(0.01)
					except:
						continue
				
				thread.join()
				
				# Check for errors
				if agent_response["error"]:
					yield f"data: {{\"type\": \"error\", \"error\": {json.dumps(agent_response['error'])} }}\n\n"
				
				yield f"data: {{\"type\": \"end\"}}\n\n"
				
			except Exception as e:
				logger.error(f"Stream error: {e}")
				yield f"data: {{\"type\": \"error\", \"error\": {json.dumps(str(e))} }}\n\n"
				yield f"data: {{\"type\": \"end\"}}\n\n"
		
		response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
		response['Cache-Control'] = 'no-cache'
		response['Access-Control-Allow-Origin'] = '*'
		response['Access-Control-Allow-Headers'] = 'Cache-Control'
		return response


class OrderChatResetView(views.APIView):
	"""Reset conversation history"""
	
	def post(self, request):
		session_key = request.session.session_key
		if session_key and session_key in _agent_cache:
			logger.info(f"Resetting conversation for session: {session_key}")
			del _agent_cache[session_key]
			return Response({'message': 'Conversation reset successfully'})
		return Response({'message': 'No active conversation found'})


class OrderChatInfoView(views.APIView):
	"""Get collected information from current conversation"""
	
	def get(self, request):
		session_key = request.session.session_key
		if session_key and session_key in _agent_cache:
			agent = _agent_cache[session_key]
			collected_info = agent.get_collected_info()
			return Response({
				'collected_info': collected_info,
				'is_complete': self._check_complete(collected_info)
			})
		return Response({'message': 'No active conversation found'}, status=404)
	
	def _check_complete(self, info):
		"""Check if order information is complete"""
		return bool(
			info.get('selected_product_id') and
			info.get('customer_name') and
			info.get('customer_phone') and
			info.get('customer_address')
		)


class OrderListCreateView(generics.ListCreateAPIView):
	serializer_class = OrderSerializer
	service = OrderService()

	def get_queryset(self):
		return self.service.list_orders()

	def perform_create(self, serializer):
		order = self.service.create_order(self.request.data)
		serializer.instance = order

class OrderDetailView(generics.RetrieveAPIView):
	serializer_class = OrderSerializer
	service = OrderService()

	def get_object(self):
		return self.service.get_order(self.kwargs["pk"])

class ProductListView(generics.ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer

class CategoryListView(generics.ListAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
