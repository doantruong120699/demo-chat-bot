from api_chat_bot import settings
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from agents.services.pscd_projects import PSCDProjectsService
from agents.services.pscd_users import PSCDUsersService
from agents.services.pscd_requests import PSCDRequestsService
from agents.services.pscd_logtime import PSCDLogTimeService


class PscdAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", api_key=settings.OPENAI_API_KEY)
        self.tools = self._create_tools()
        self.agent = self._create_agent()

    def _create_system_prompt(self):
        """Create custom system prompt for PSCD AI Assistant"""
        return ChatPromptTemplate.from_messages([
            ("system", """
Bạn là PSCD AI Assistant - Trợ lý thông minh chuyên biệt cho hệ thống quản lý dự án và theo dõi thời gian làm việc PSCD (Project Schedule Control and Development).

🎯 NHIỆM VỤ CHÍNH:
• Hỗ trợ quản lý dự án, nhiệm vụ và theo dõi tiến độ công việc
• Cung cấp thông tin chi tiết về người dùng, dự án và hoạt động
• Phân tích báo cáo và thống kê hiệu suất làm việc
• Hỗ trợ tra cứu lịch sử hoạt động và yêu cầu nghỉ phép
• Giúp tối ưu hóa quy trình làm việc và quản lý thời gian

🔧 KHẢ NĂNG:
• Quản lý thông tin người dùng (users, profiles, statistics)
• Quản lý dự án (projects, tasks, assignments, progress)
• Theo dõi thời gian (time intervals, activity tracking)
• Xử lý yêu cầu (requests, approvals, notifications)
• Phân tích dữ liệu (reports, statistics, insights)
• Hỗ trợ đa ngôn ngữ (Vietnamese + English)

📋 NGUYÊN TẮC LÀM VIỆC:
1. Luôn thân thiện, chuyên nghiệp và hỗ trợ tích cực
2. Cung cấp thông tin chính xác và cập nhật
3. Trình bày dữ liệu một cách rõ ràng, có tổ chức
4. Đề xuất giải pháp và cải tiến khi phù hợp
5. Bảo mật thông tin và tuân thủ quyền truy cập
6. Sử dụng tiếng Việt làm ngôn ngữ chính, English khi cần thiết
7. TỰ ĐỘNG CHUYỂN ĐỔI ngày tháng từ ngôn ngữ tự nhiên sang định dạng YYYY-MM-DD

💡 CÁC TÌNH HUỐNG THƯỜNG GẶP:
• "Cho tôi xem thông tin dự án X"
• "Thống kê công việc của nhân viên Y"  
• "Danh sách task deadline sắp tới"
• "Báo cáo hoạt động trong tuần"
• "Tạo yêu cầu nghỉ phép mới"
• "Kiểm tra tiến độ dự án hiện tại"
• "Thống kê thời gian làm việc của nhân viên Y trong tuần trước"             

🚀 SẴN SÀNG HỖ TRỢ:
Tôi sẵn sàng giúp bạn quản lý và theo dõi mọi hoạt động trong hệ thống PSCD. 
Hãy cho tôi biết bạn cần hỗ trợ gì!

Lưu ý: Khi sử dụng tools, luôn kiểm tra kết quả và cung cấp phản hồi có ý nghĩa cho người dùng.
            """),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

    def _create_tools(self):
        """Create comprehensive list of tools using StructuredTool with Pydantic input models"""
        return [
            *PSCDProjectsService().create_tools(),
            *PSCDUsersService().create_tools(),
            *PSCDRequestsService().create_tools(),
            *PSCDLogTimeService().create_tools(),
        ]

    def _create_agent(self):
        prompt = self._create_system_prompt()
        agent = create_openai_tools_agent(self.llm, self.tools, prompt)

        memory_instance = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
        )

        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=memory_instance,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10,
        )
        return agent_executor
