import json
from langchain.schema import SystemMessage, HumanMessage
from datetime import datetime, timedelta
from restaurant_booking.agents.time_processor import VietnameseTimeProcessor

class ConversationEntityExtractor:
    """
    A utility class to extract relevant booking entities from a conversation history.
    This class expects the conversation to be a list of message dicts:
      [{"role": "user"/"assistant", "content": "..."}]
    and will return a dict of extracted entities.
    """

    # The schema for entities
    ENTITY_KEYS = [
        'booking_date',
        'booking_time',
        'table_type',
        'party_size',
        'floor',
        'table_id',
        'guest_name',
        'guest_phone',
        'note'
    ]

    def __init__(self, llm, callbacks=None, queue=None):
        """
        llm: Language model instance with an 'invoke' method (similar to LangChain)
        callbacks: List of callbacks to be used for streaming
        queue: Queue for streaming
        """
        self.llm = llm
        # Ensure streaming is disabled for entity extraction (to get full JSON output in one go)
        # if hasattr(self.llm, "streaming"):
        self.llm.streaming = False
        self.llm.temperature = 0.0

        self.callbacks = callbacks
        self.queue = queue
        
        # Initialize time processor
        self.time_processor = VietnameseTimeProcessor()

    def extract(self, chat_history, user_input):
        """
        Extract entities from the entire conversation history.
        Args:
            chat_history (list[dict]): [{'role': ..., 'content': ...}, ...]

        Returns:
            dict: extracted entities (with correct keys), values or None if missing
        """
        # Concatenate history as a string (human readable)
        entity_extraction_system_prompt = """
                Bạn là một hệ thống trích xuất thông tin đặt bàn cho nhà hàng PSCD.

                Nhiệm vụ của bạn:
                - Đọc toàn bộ hội thoại giữa khách hàng và trợ lý đặt bàn.
                - Trích xuất các thông tin theo đúng schema bên dưới và chỉ trả về một đối tượng JSON duy nhất chứa các trường với giá trị cụ thể mà khách hàng đã cung cấp rõ ràng.

                Chú ý:
                - KHÔNG bịa hoặc tự suy diễn bất kỳ thông tin nào nếu khách chưa nói/không xác nhận trực tiếp.
                - Không đưa vào JSON các trường mà khách hàng chưa cung cấp hoặc thông tin không rõ ràng.
                - Tuyệt đối không trả về bất kỳ văn bản, giải thích, markdown, hoặc ký tự nào ngoài JSON hợp lệ.
                - Các từ như "Anh/chị", "mình", "tôi", "tớ" là đại từ nhân xưng, KHÔNG được ghi nhận vào trường tên khách hàng.

                Schema cần trích xuất (các trường hợp lệ):
                - booking_date: Ngày đặt bàn (định dạng: YYYY-MM-DD)
                - booking_time: Giờ đặt bàn (định dạng: HH:MM)
                - table_type: Loại bàn, chỉ lấy một trong các giá trị: "INDOOR" (Trong nhà), "OUTDOOR" (Ngoài trời), "PRIVATE" (Phòng riêng), "BAR" (Quầy bar), "CHAIR" (Ghế ngồi), "WINDOW" (Cửa sổ)
                - party_size: Số lượng người (số nguyên)
                - floor: Tầng (số nguyên)
                - table_id: ID bàn (số nguyên)
                - guest_name: Tên khách (dạng chuỗi)
                - guest_phone: Số điện thoại khách (dạng chuỗi)
                - note: Ghi chú của khách hàng (dạng chuỗi)

                QUY ĐỊNH:
                - Chỉ trả về đúng 1 JSON object với các trường hợp lệ KHÁCH ĐÃ CUNG CẤP.
                - Nếu trường nào chưa đủ thông tin hợp lệ thì KHÔNG ĐƯỢC đưa vào JSON (không cần đưa vào với giá trị null hay chuỗi rỗng).
                - Không viết lại yêu cầu, không thêm bất kỳ giải thích, văn bản, ký tự thừa nào khác dưới bất kỳ dạng nào (kể cả markdown).
                - TUYỆT ĐỐI không đoán giá trị, không tự tạo thông tin.

                Thông tin hỗ trợ về ngày tháng:
                - Hôm nay là ngày {0}
                - Giờ hiện tại là {1}
                - Ngày hôm qua là ngày {2}
                - Ngày mai là ngày {3}
                - Hôm nay là thứ {4}
            """

        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        today_weekday = datetime.now().weekday() + 2 
        today_time = datetime.now().strftime("%H:%M:%S")

        # Xử lý thời gian trước khi trích xuất entity
        processed_input = self._preprocess_time_expressions(user_input)
        
        system_message = SystemMessage(content=entity_extraction_system_prompt.format(today, today_time, yesterday, tomorrow, today_weekday))
        messages = [system_message] + chat_history + [HumanMessage(content=processed_input)]
        print(f"=========================== Entity extraction messages: {messages}")
        result = self.llm.invoke(messages)
        print(f"=========================== Entity extraction result: {result.content.strip()}")
        return self._parse_entity(result.content.strip())

    def _preprocess_time_expressions(self, user_input: str) -> str:
        """
        Xử lý các biểu thức thời gian trong input của user
        """
        # Kiểm tra xem có chứa biểu thức thời gian không
        if self.time_processor.is_time_expression(user_input):
            # Cải thiện khả năng hiểu thời gian
            enhanced_input = self.time_processor.enhance_time_understanding(user_input)
            print(f"=========================== Time processing in entity extraction:")
            print(f"Original input: {user_input}")
            print(f"Enhanced input: {enhanced_input}")
            return enhanced_input
        
        return user_input

    def _parse_entity(self, entity_text):
        """Parse the entity text into a dictionary"""
        return json.loads(entity_text)

