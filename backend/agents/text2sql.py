from common.tools.sql_tool import connect_to_db, execute_sql_query
from openai import OpenAI
from api_chat_bot import settings
import yaml
import json


class Text2SQL:
    """
    Text2SQL agent that converts natural language queries into SQL queries.
    """

    def __init__(self):
        self.conn = connect_to_db()
        self.database_metadata = self.load_database_metadata()
        self.SCHEMA = yaml.dump(
            {
                k: v
                for k, v in self.database_metadata.items()
                if k in ["database_description", "tables", "relationships"]
            },
            default_flow_style=False,
            sort_keys=False,
        )
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        self.llm = OpenAI(api_key=api_key)

    def chat_handler(self, text):
        """
        Chat handler that converts natural language queries into SQL queries.
        Returns a streaming response with only the answer.
        """

        # First, generate the SQL query
        sql_query = self.convert_text_to_sql(text)
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
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": answer_prompt}],
            stream=True,
        )

        for chunk in answer_stream:
            if chunk.choices[0].delta.content:
                yield f"data: {json.dumps({'type': 'token', 'content': chunk.choices[0].delta.content})}\n\n"

    def load_database_metadata(self):
        """
        Loads the database metadata from the database_metadata.yml file.
        """
        import os

        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        metadata_path = os.path.join(script_dir, "database_metadata.yml")

        with open(metadata_path, "r") as file:
            database_metadata = yaml.safe_load(file)
        return database_metadata

    def convert_text_to_sql(self, text):
        prompt = f"""
        Bạn là một agent SQL chuyển đổi các câu hỏi ngôn ngữ tự nhiên thành các câu truy vấn SQL.

        Đây là schema của cơ sở dữ liệu:
        {self.SCHEMA}

        Câu hỏi của người dùng:
        {text}

        Dựa trên schema cơ sở dữ liệu và câu hỏi của người dùng, hãy tạo một câu truy vấn SQL để trả lời câu hỏi.
        Chỉ trả về câu truy vấn SQL mà không có bất kỳ giải thích hay định dạng markdown nào.
        Câu truy vấn phải đúng cú pháp và tương thích với PostgreSQL.
        """

        sql_query = self.llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return sql_query.choices[0].message.content
