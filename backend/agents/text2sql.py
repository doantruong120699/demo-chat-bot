from common.tools.sql_tool import connect_to_db, execute_sql_query
from openai import OpenAI
from api_chat_bot import settings
import yaml
import json


class Text2SQL:
    """
    Text2SQL agent that converts natural language queries into SQL queries.
    """

    def __init__(self, model="gpt-4o-mini"):
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
        self.model = model
        self.llm = OpenAI(api_key=settings.OPENAI_API_KEY)

    def routing_prompt(self, histories, text):
        """
        Prompt hướng dẫn agent xác định xem câu hỏi của người dùng là câu hỏi truy vấn cơ sở dữ liệu thông thường hay là câu hỏi liên quan đến tính lương.
        """
        prompt = (
            "Bạn là một agent có nhiệm vụ xác định loại câu hỏi của người dùng để định tuyến đến agent phù hợp.\n"
            "Nếu câu hỏi liên quan đến lương, tiền lương, lương làm thêm giờ, tổng lương, lương trung bình, hoặc các phép tính về lương của nhân viên, trả về duy nhất: salary\n"
            "Nếu câu hỏi là truy vấn dữ liệu thông thường (không liên quan đến lương), trả về duy nhất: general\n"
            "Một số ví dụ:\n"
            "- 'Tính lương tháng này của nhân viên Nguyễn Văn A' → salary\n"
            "- 'Cho tôi biết danh sách nhân viên phòng IT' → general\n"
            "- 'Tổng lương làm thêm giờ của phòng Kế toán trong tháng 5' → salary\n"
            "- 'Có bao nhiêu nhân viên đang làm việc tại công ty?' → general\n"
            "Chỉ trả về duy nhất một từ: salary hoặc general."

            f"Câu hỏi của người dùng: {text}"
        )

        routing_query = self.llm.chat.completions.create(
            model=self.model,
            messages=[*histories, {"role": "user", "content": prompt}],
        )
        return routing_query.choices[0].message.content

    def load_database_metadata(self):
        """
        Loads the database metadata from the database_metadata.yml file.
        """
        import os

        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        metadata_path = os.path.join(script_dir, "config/database_metadata.json")

        with open(metadata_path, "r") as file:
            database_metadata = json.load(file)
        return database_metadata

    def convert_text_to_sql(self, histories, text):
        routing_query = self.routing_prompt(histories, text)

        prompt = f"""
        {self.calculate_salary_sql_prompt(text) if routing_query == "salary" else self.general_query_prompt(text)}
        {text}

        Dựa trên schema cơ sở dữ liệu và câu hỏi của người dùng, hãy tạo một câu truy vấn SQL để trả lời câu hỏi.
        Chỉ trả về câu truy vấn SQL mà không có bất kỳ giải thích hay định dạng markdown nào.
        Câu truy vấn phải đúng cú pháp và tương thích với PostgreSQL.
        """

        sql_query = self.llm.chat.completions.create(
            model=self.model,
            messages=[*histories, {"role": "user", "content": prompt}],
        )
        return sql_query.choices[0].message.content
    
    def general_query_prompt(self, text):
        """
        Chuyên biệt cho việc truy vấn dữ liệu thông thường
        """
        prompt = f"""
        Bạn là một agent SQL chuyên về truy vấn dữ liệu về thông tin của nhân viên. Bạn chuyển đổi các câu hỏi về thông tin của nhân viên thành các câu truy vấn SQL.

        Đây là schema của cơ sở dữ liệu:
        {self.SCHEMA}

        Câu hỏi của người dùng:
        {text}

        Dựa trên schema cơ sở dữ liệu và câu hỏi của người dùng, hãy tạo một câu truy vấn SQL để trả lời câu hỏi.
        Chỉ trả về câu truy vấn SQL mà không có bất kỳ giải thích hay định dạng markdown nào.
        Câu truy vấn phải đúng cú pháp và tương thích với PostgreSQL.
        """
        return prompt

    def calculate_salary_sql_prompt(self, text):
        """
        Chuyên biệt cho việc tính toán lương nhân viên
        """
        prompt = f"""
        Bạn là một agent SQL chuyên về tính toán lương nhân viên. Bạn chuyển đổi các câu hỏi về lương thành các câu truy vấn SQL.

        Đây là schema của cơ sở dữ liệu:
        {self.SCHEMA}

        QUY TẮC TÍNH LƯƠNG:
        1. Lương cơ bản được lưu trong bảng user_info.salary (VND/tháng)
        2. Thời gian làm việc được lưu trong bảng report_time với các trường:
           - user_id: id của nhân viên
           - start_time: thời gian bắt đầu làm việc
           - end_time: thời gian kết thúc làm việc  
           - duration: tổng số giờ làm việc trong ngày (giờ)
        3. Số giờ làm việc tiêu chuẩn trong tháng: 
           - Một ngày làm việc 8 giờ, Làm việc từ thứ Hai đến thứ Sáu (không tính T7, Chủ nhật)
        4. Số giờ làm việc thực tế của nhân viên trong tháng:
           - Tổng duration trong bảng report_time của nhân viên trong tháng đó
        5. Các công thức tính lương:
           Nếu số giờ làm việc thực tế của nhân viên trong tháng lớn hơn hoặc bằng số giờ làm việc tiêu chuẩn trong tháng thì tính thêm lương làm thêm giờ.
           - Lương tháng = Lương cơ bản
           - Lương làm thêm giờ = (Lương cơ bản / số giờ làm việc tiêu chuẩn trong tháng) * (số giờ làm việc thực tế của nhân viên trong tháng - số giờ làm việc tiêu chuẩn trong tháng) * hệ số 1.5
           - Tổng lương = Lương tháng + Lương làm thêm giờ
           Nếu số giờ làm việc thực tế của nhân viên trong tháng nhỏ hơn số giờ làm việc tiêu chuẩn trong tháng thì tính thêm lương làm thêm giờ.
           - Tổng lương = (Lương cơ bản / số giờ làm việc tiêu chuẩn trong tháng) * số giờ làm việc thực tế của nhân viên trong tháng

        5. Các trường hợp đặc biệt:
           - Tăng ca: hệ số 1.5

        Các loại câu hỏi thường gặp:
        - Tính lương tháng của nhân viên
        - Tính lương làm thêm giờ
        - Tính lương theo khoảng thời gian
        - Tính tổng lương của tất cả nhân viên
        - Tính lương trung bình
        - Tính số giờ làm việc của nhân viên

        Câu hỏi của người dùng:
        {text}

        Dựa trên quy tắc tính lương và schema cơ sở dữ liệu, hãy tạo một câu truy vấn SQL để tính toán lương theo yêu cầu.
        Chỉ trả về câu truy vấn SQL mà không có bất kỳ giải thích hay định dạng markdown nào.
        Câu truy vấn phải đúng cú pháp và tương thích với PostgreSQL.

        Khi hỏi tính lương, bạn phải trả về các thông tin sau:
        - Tổng số giờ làm việc thực tế của nhân viên trong tháng
        - Tổng số giờ làm việc tiêu chuẩn trong tháng
        - Tổng lương tháng
        - Tổng lương làm thêm giờ
        - Tổng lương
        """

        sql_query = self.llm.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return sql_query.choices[0].message.content
