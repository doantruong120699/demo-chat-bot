from agents.text2sql import Text2SQL
from common.tools.sql_tool import execute_sql_query, connect_to_db
import json
from openai import OpenAI
from api_chat_bot import settings

class ChatBot:
    def __init__(self, model="gpt-4o-mini"):
        self.text2sql = Text2SQL(model=model)
        self.conn = connect_to_db()
        self.model = model
        self.llm = OpenAI(api_key=settings.OPENAI_API_KEY)

    def chat_handler(self, text):
        """
        Chat handler that converts natural language queries into SQL queries.
        Returns a streaming response with only the answer.
        """

        # First, generate the SQL query
        sql_query = self.text2sql.convert_text_to_sql(text)
        print(
            "-------------------------------- SQL QUERY --------------------------------"
        )
        print(sql_query)
        print(
            "-------------------------------- END SQL QUERY --------------------------------"
        )

        # Execute the query and get results
        query_results = execute_sql_query(self.conn, sql_query)

        # Generate answer in streaming format
        answer_prompt = f"""
        Câu hỏi của người dùng: {text}
        
        Kết quả truy vấn:
        {query_results}

        Dựa trên kết quả truy vấn, hãy cung cấp một câu trả lời rõ ràng và ngắn gọn cho câu hỏi của người dùng.
        Tập trung vào việc trả lời trực tiếp những gì được hỏi, và bao gồm các con số hoặc sự kiện liên quan từ dữ liệu.
        Nếu kết quả không trả lời trực tiếp câu hỏi, hãy giải thích thông tin nào đã được tìm thấy.
        Hãy làm cho câu trả lời thân thiện và hấp dẫn hơn.
        """

        # Stream the answer generation
        answer_stream = self.llm.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": answer_prompt}],
            stream=True,
        )

        for chunk in answer_stream:
            if chunk.choices[0].delta.content:
                yield f"data: {json.dumps({'type': 'token', 'content': chunk.choices[0].delta.content})}\n\n"