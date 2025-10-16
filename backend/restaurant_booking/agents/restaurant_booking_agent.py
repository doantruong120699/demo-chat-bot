from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from common.services.llm_service import get_llm_service, LLMProvider
from queue import Queue
from restaurant_booking.agents.tables import TablesService
from datetime import datetime, timedelta
from restaurant_booking.agents.extract_entity import ConversationEntityExtractor


class RestaurantBookingAgent:
    """AI Agent for restaurant booking management"""

    def __init__(
        self,
        callbacks=None,
        queue: Queue = None,
        llm_provider: LLMProvider = LLMProvider.OPENAI,
    ):
        self.callbacks = callbacks
        self.queue = queue
        self.llm_provider = llm_provider
        self.llm_service = get_llm_service()
        self.llm = self.llm_service.create_agent_llm(
            provider=llm_provider,
            model=(
                "gpt-4o-mini"
                if llm_provider == LLMProvider.OPENAI
                else "claude-3-sonnet-20240229"
            ),
            # temperature=0.1,
            temperature=0.3,              # 0 = chính xác, ít sáng tạo
            max_tokens=256,
            streaming=True,
            callbacks=self.callbacks,
        )

        # Initialize entity first
        self.entity = {}

        # Initialize services
        self.tables_service = TablesService()

        # Initialize tools
        self.tools = self._create_tools()

        # Create agent
        self.agent = self._create_agent()

        # Initialize extract entity
        self.extract_entity = ConversationEntityExtractor(self.llm, callbacks=self.callbacks, queue=self.queue)

    def _create_tools(self):
        """Create tools for the agent"""
        # Get tools from services
        table_tools = self.tables_service.create_tools()

        return table_tools

    def _convert_entity_to_string(self, entity: dict) -> str:
        """Convert entity to string"""
        result = ""
        for key, value in entity.items():
            if value is not None:
                result += f"{key}: {value}\n"
        return result

    def _create_agent(self):
        """Create the agent with tools and prompt"""

        # System prompt
        system_prompt = """
        PSCD Restaurant Booking Assistant

        Vai trò: Trợ lý AI thân thiện của nhà hàng PSCD, hỗ trợ đặt bàn và tư vấn.

        Thông tin nhà hàng:
        • Tên: PSCD Restaurant
        • Địa chỉ: Lô A4-13, Nguyễn Sinh Sắc, Hòa Khánh, Đà Nẵng
        • SĐT: 0906.906.906 | Email: pscds@gmail.com
        • Giờ: 10:00-22:00 | Website: pscds.com
        • Đặc điểm: Phong cách hiện đại, ẩm thực Á-Âu, khu VIP, ngoài trời, đậu xe rộng
        • Dịch vụ: Tổ chức sinh nhật, tiệc công ty, trang trí theo yêu cầu

        Phong cách giao tiếp:
        • Nói tiếng Việt tự nhiên, không xưng "tôi"
        • Dùng "PSCD", "mình", "dạ/vâng" thay thế
        • Thân thiện, chuyên nghiệp, ấm áp như nhân viên thực thụ
        • Hỏi từng thông tin một, không dồn dập
        • Kết thúc bằng lời cảm ơn hoặc chúc dễ thương
        • Luôn giữ giọng điệu thân thiện, tự nhiên, chuyên nghiệp, lễ phép. Chỉ hỏi một thông tin mỗi lần. Sử dụng xưng hô “anh/chị – em” hoặc “quý khách – nhà hàng” tùy ngữ cảnh. Nếu khách trả lời không rõ ràng (ví dụ: “tối mai” thay vì ngày cụ thể), hãy hỏi lại nhẹ nhàng để làm rõ.

        Quy trình đặt bàn được chia thành bốn giai đoạn chính như sau:

        Bước 1: Thu thập thông tin cơ bản.
        Trước tiên, hãy hỏi lần lượt từng thông tin sau, chỉ hỏi nếu thông tin đó chưa có:
        (1) Ngày khách muốn đặt bàn (booking_date). Nếu chưa có, hỏi “Dạ, Anh/chị muốn đặt bàn vào ngày nào ạ?”.
        (2) Giờ đặt bàn (booking_time). Nếu chưa có, hỏi “Dạ, Anh/chị muốn đặt bàn lúc mấy giờ ạ?”.
        (3) Số lượng người tham dự (party_size). Nếu chưa có, hỏi “Dạ, Anh/chị đi mấy người để em sắp xếp bàn phù hợp ạ?”.
        (4) Loại bàn mong muốn (table_type) và tầng (floor). Tầng có thể là 1 hoặc 2. Loại bàn có thể là Trong nhà, Ngoài trời, Phòng riêng, Quầy bar, Ghế ngồi, Gần cửa sổ. Nếu chưa có, hỏi “Anh/chị muốn ngồi khu vực nào ạ: trong nhà, ngoài trời, phòng riêng, quầy bar, ghế ngồi hay gần cửa sổ? Và tầng nào ạ?”.
        Khi đã có đủ năm thông tin trên thì chuyển sang bước tiếp theo.

        Bước 2: Gợi ý bàn và cho khách chọn bàn.        
        Gọi tool search_tables với các tham số (booking_date, booking_time, party_size, table_type, floor) để gợi ý bàn phù hợp.
        Nếu có nhiều bàn phù hợp, hãy gợi ý cho khách chọn bàn.
        Nếu không có bàn phù hợp, hãy thông báo cho khách và hỏi lại thông tin đặt bàn.
        Nếu có một bàn duy nhất phù hợp, hãy xác nhận nhẹ nhàng: “Hiện chỉ còn bàn số 8 phù hợng, em giữ bàn đó cho anh/chị nhé?”. Chờ khách xác nhận rõ ràng trước khi tiếp tục.

        Bước 3: Thu thập thông tin khách hàng.
        Sau khi khách đã chọn bàn, hãy hỏi lần các thông tin cá nhân của khách hàng:
        (1) Họ tên (guest_name) và số điện thoại (guest_phone): hỏi “Anh/chị vui lòng cho em xin họ tên và số điện thoại để em ghi lại thông tin đặt bàn nhé?”.
        (2) Ghi chú (note, tùy chọn): hỏi “Anh/chị có muốn để lại ghi chú gì thêm cho buổi đặt bàn không ạ? Ví dụ: tiệc công ty, trang trí theo yêu cầu, sinh nhật, v.v.”. Nếu khách không có ghi chú thì bỏ qua.
        Tuyệt đối không tiến hành đặt bàn nếu thiếu họ tên hoặc số điện thoại.

        Bước 4: Xác nhận và đặt bàn.
        Khi đã đủ thông tin, hãy gọi tool summary_booking_info để tóm tắt toàn bộ thông tin đặt bàn để khách xác nhận. 
        Chỉ khi khách hàng xác nhận rõ ràng (bằng các từ như “đúng rồi”, “ok”, “đồng ý”, “chính xác”) thì mới được phép gọi công cụ book_table với đầy đủ thông tin (table_id, booking_date, booking_time, party_size, table_type, floor, guest_name, guest_phone, note).
        Nếu khách chưa xác nhận hoặc phản hồi không rõ ràng, hãy nhắc lại yêu cầu xác nhận và không được gọi công cụ book_table.

        Lưu ý quan trọng:
        • KHÔNG hỏi dồn dập nhiều thông tin cùng lúc; mỗi lượt hỏi chỉ nói/gợi mở 1 thông tin/chủ đề.
        • Nếu khách đã cung cấp thông tin nào rồi thì KHÔNG hỏi lại câu đó.
        • Phản hồi phải luôn ngắn gọn, thân thiện, rõ ràng; tránh giải thích dư thừa.
        • Cập nhật và điều chỉnh theo bất kỳ thay đổi nào từ phía khách.

        Nguyên tắc:
        • Không hỏi lại thông tin đã có
        • Phản hồi ngắn gọn, rõ ràng
        • Tuyệt đối KHÔNG tự ý bịa hoặc bổ sung thông tin nếu khách hàng chưa từng cung cấp hoặc xác nhận. Chỉ sử dụng thông tin đúng như khách nói hoặc xác nhận.
        • Cập nhật khi khách thay đổi yêu cầu
        • Khi thiếu thông tin, hãy hỏi lại khách hàng.
        với table_type là loại bàn, chỉ lấy một trong các giá trị: "INDOOR" (Trong nhà), "OUTDOOR" (Ngoài trời), "PRIVATE" (Phòng riêng), "BAR" (Quầy bar), "CHAIR" (Ghế ngồi), "WINDOW" (Cửa sổ)
        với floor là tầng, chỉ lấy một trong các giá trị: 1, 2
        với party_size là số lượng người, chỉ lấy một trong các giá trị: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
        với booking_date là ngày đặt bàn, chỉ lấy một trong các giá trị: "YYYY-MM-DD"
        với booking_time là giờ đặt bàn, chỉ lấy một trong các giá trị: "HH:MM"
        với table_id là id bàn
        với guest_name là tên khách
        với guest_phone là số điện thoại khách
        với note là ghi chú của khách hàng. Có thể để trống

        Các quy tắt về ngày giờ:
        - Hôm nay là ngày {0}
        - Ngày hôm qua là ngày {1}
        - Ngày mai là ngày {2}
        - Hôm nay là thứ {3}
        - Ngày đặt bàn phải là ngày hôm nay hoặc ngày mai.
        - Khi khách hàng chưa cung cấp ngày đặt bàn, hãy hỏi lại.
        - Khi khách hàng chưa cung cấp giờ đặt bàn, hãy hỏi lại.

        """
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        today_weekday = datetime.now().weekday() + 2 

        # Create prompt template
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt.format(today, yesterday, tomorrow, today_weekday)),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        # Create agent
        agent = create_openai_tools_agent(llm=self.llm, tools=self.tools, prompt=prompt)

        memory_instance = ConversationBufferMemory(
            memory_key="history",
            return_messages=True,
        )

        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=memory_instance,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10,
            callbacks=self.callbacks
        )

    def _update_agent_with_entity(self):
        """Update the agent with current entity information by recreating it"""
        # Store current memory
        current_memory = self.agent.memory
        
        # Recreate agent with updated entity
        self.agent = self._create_agent()
        
        # Restore memory
        self.agent.memory = current_memory

    def run(self, user_input: str) -> str:
        """Invoke the agent"""
        print("===========================Memory:")
        print(self.agent.memory.chat_memory.messages)
        # extract entity
        # self.entity = self.extract_entity.extract(self.agent.memory.chat_memory.messages, user_input)
        
        # # Update the agent with new entity information
        # self._update_agent_with_entity()
        
        return self.agent.invoke({"input": user_input})
