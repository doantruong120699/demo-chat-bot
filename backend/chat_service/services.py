import os
import json
import time
from django.http import StreamingHttpResponse
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.callbacks import BaseCallbackHandler
from api_chat_bot import settings
from langchain_community.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Tuple
import re
import docx
from .models import create_document_embedding

class StreamingCallbackHandler(BaseCallbackHandler):
    """Custom callback handler for streaming responses."""
    
    def __init__(self):
        self.response_tokens = []
    
    def on_llm_new_token(self, token: str, **kwargs):
        """Called when a new token is generated."""
        self.response_tokens.append(token)
    
    def get_streaming_response(self):
        """Yield tokens as they are generated."""
        for token in self.response_tokens:
            yield f"data: {json.dumps({'content': token, 'type': 'token'})}\n\n"
        
        # Send end signal
        yield f"data: {json.dumps({'type': 'end'})}\n\n"


class ChatService:
    def __init__(self):
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        model = "gpt-4o-mini"

        self.llm = ChatOpenAI(
            model=model,
            temperature=0.7,
            streaming=True,
            openai_api_key=api_key,
            verbose=False,
        )
        
        # Load whitepaper content
        self.whitepaper_content = self.load_whitepaper_content()

    def load_whitepaper_content(self):
        """Load the whitepaper content from the extracted file"""
        try:
            with open('whitepaper_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data['content']
        except FileNotFoundError:
            print("Warning: whitepaper_data.json not found. Using empty context.")
            return ""
        except Exception as e:
            print(f"Error loading whitepaper: {e}")
            return ""

    def chat(self, input_data):
        return self.stream_chat(input_data)

    def stream_chat(self, input_data):
        """
        Stream chat response using LangChain and OpenAI with whitepaper context.
        
        Args:
            input_data: Dictionary containing user input, typically {'message': 'user message'}
        """
        user_message = input_data.get('message', '')
        
        if not user_message:
            def error_stream():
                yield f"data: {json.dumps({'error': 'No message provided', 'type': 'error'})}\n\n"
            
            response = StreamingHttpResponse(error_stream(), content_type='text/event-stream')
            response['Cache-Control'] = 'no-cache'
            return response

        def event_stream():
            try:
                # Create system message with whitepaper context
                system_message = f"""You are a helpful AI assistant with access to a whitepaper about Tosi Growth Holding. 
                Use the following whitepaper content to answer questions accurately and comprehensively:

                {self.whitepaper_content}

                When answering questions:
                1. Base your responses on the whitepaper content provided above
                2. If the question is not related to the whitepaper, politely redirect to whitepaper-related topics
                3. Provide specific information from the whitepaper when possible
                4. Be helpful and informative while staying within the context of the whitepaper
                """
                
                # Create messages with system context
                messages = [
                    SystemMessage(content=system_message),
                    HumanMessage(content=user_message)
                ]
                
                # Stream the response
                for chunk in self.llm.stream(messages):
                    if hasattr(chunk, 'content') and chunk.content:
                        yield f"data: {json.dumps({'content': chunk.content, 'type': 'token'})}\n\n"
                    time.sleep(0.01)
                
                # Send end signal
                yield f"data: {json.dumps({'type': 'end'})}\n\n"
                
            except Exception as e:
                # Handle specific OpenAI errors
                error_message = str(e)
                
                if "429" in error_message or "Too Many Requests" in error_message:
                    error_message = "Rate limit exceeded. Please wait a moment and try again."
                elif "401" in error_message or "Unauthorized" in error_message:
                    error_message = "Invalid API key. Please check your OpenAI API key."
                elif "400" in error_message:
                    error_message = "Invalid request. Please check your input."
                elif "500" in error_message:
                    error_message = "OpenAI service is temporarily unavailable. Please try again later."
                else:
                    error_message = f"Error generating response: {error_message}"
                
                yield f"data: {json.dumps({'error': error_message, 'type': 'error'})}\n\n"
                yield f"data: {json.dumps({'type': 'end'})}\n\n"

        response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Cache-Control'
        return response

    def _create_documents_from_text(self) -> Tuple[List[Document], str]:

        def read_docx_file(file_path):
            doc = docx.Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return '\n'.join(full_text)

        file_path = "Whitepaper Tosi Growth Holding.docx"
        file_content = read_docx_file(file_path)
        metadata = {"file_id": 1, "source": "whitepaper", "file_name": file_path}

        texts = [Document(page_content=file_content, metadata=metadata)]
        text_splitter = RecursiveCharacterTextSplitter(
            separators=[
                s.replace(r"\,", ",")
                for s in re.split(r"(?<!\\),", " ")
            ],
            chunk_size=300,
            chunk_overlap=100,
            add_start_index=True,
        )   
        docs = text_splitter.split_documents(texts)
        create_document_embedding(docs)
        return docs, file_content
