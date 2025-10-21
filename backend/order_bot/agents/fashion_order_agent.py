from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from common.services.llm_service import get_llm_service, LLMProvider
from queue import Queue
from order_bot.agents.products import ProductsService
from order_bot.agents.orders import OrdersService
from datetime import datetime


class FashionOrderAgent:
    """AI Agent for fashion shop order management"""

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
            temperature=0.3,
            max_tokens=512,
            streaming=True,
            callbacks=self.callbacks,
        )

        # Initialize collected information tracking
        self.collected_info = {
            # Product search info
            'product_type': None,
            'size': None,
            'color': None,
            'min_price': None,
            'max_price': None,
            
            # Selected product info
            'selected_product_id': None,
            'selected_product_name': None,
            'selected_product_price': None,
            'quantity': 1,
            
            # Customer info
            'customer_name': None,
            'customer_phone': None,
            'customer_address': None,
            'customer_email': None,
            'notes': None,
        }

        # Initialize services
        self.products_service = ProductsService()
        self.orders_service = OrdersService()

        # Initialize tools
        self.tools = self._create_tools()

        # Create agent
        self.agent = self._create_agent()

    def _create_tools(self):
        """Create tools for the agent"""
        product_tools = self.products_service.create_tools()
        order_tools = self.orders_service.create_tools()
        
        return product_tools + order_tools

    def _create_agent(self):
        """Create the agent with tools and prompt"""

        # System prompt
        system_prompt = """
        Fashion Shop AI Assistant - Trợ lý đặt hàng thông minh

        QUAN TRỌNG - ĐỌC CONTEXT:
        • Mỗi tin nhắn có thể chứa [Thông tin đã có: ...] 
        • LUÔN kiểm tra context này trước khi hỏi
        • KHÔNG hỏi lại thông tin đã có trong context
        • Sử dụng thông tin trong context để gọi tools

        QUY TRÌNH ĐẶT HÀNG:

        GIAI ĐOẠN 1: TÌM KIẾM SẢN PHẨM
        Kiểm tra context:
        - Nếu THIẾU "Loại SP" → Hỏi: "Bạn muốn tìm loại sản phẩm gì? (áo thun, quần jean, váy...)"
        - Nếu CÓ "Loại SP" NHƯNG THIẾU "Size" → Hỏi: "Bạn muốn size nào? (XS, S, M, L, XL...)"
        - Nếu CÓ "Loại SP" và "Size" NHƯNG THIẾU "Màu" → Hỏi: "Bạn thích màu gì? (đen, trắng, xám...)"
        - Nếu ĐỦ CẢ 3 (Loại SP, Size, Màu) → GỌI NGAY tool search_products
        
        Sau khi gọi search_products:
        - Hiển thị danh sách sản phẩm tìm được
        - Hỏi khách chọn sản phẩm bằng ID

        GIAI ĐOẠN 2: CHỌN SẢN PHẨM
        - Khi khách chọn sản phẩm (ví dụ: "sản phẩm 1", "id 2", "cái thứ nhất")
        - Gọi get_product_detail(product_id) để xem chi tiết
        - Hỏi số lượng muốn mua (mặc định 1)
        - Gọi check_product_availability để kiểm tra tồn kho

        GIAI ĐOẠN 3: THÔNG TIN KHÁCH HÀNG
        Kiểm tra context và hỏi lần lượt những thông tin còn thiếu:
        - Nếu THIẾU "Tên" → Hỏi: "Anh/chị cho shop xin họ tên để ghi đơn hàng nhé?"
        - Nếu THIẾU "SĐT" → Hỏi: "Cho shop xin số điện thoại liên hệ ạ?"
        - Nếu THIẾU "Địa chỉ" → Hỏi: "Anh/chị giao hàng tới địa chỉ nào ạ?"
        - Email (tùy chọn): "Anh/chị có email để nhận xác nhận không ạ?"

        GIAI ĐOẠN 4: XÁC NHẬN VÀ TẠO ĐƠN
        - Khi ĐỦ thông tin (Tên, SĐT, Địa chỉ, Sản phẩm đã chọn)
        - Gọi summary_order_info để hiển thị tóm tắt
        - Hỏi xác nhận: "Anh/chị xác nhận đặt hàng nhé?"
        - Nếu khách nói "ok", "đồng ý", "xác nhận", "đặt hàng"
        - → GỌI create_order với đầy đủ thông tin từ context

        PHONG CÁCH GIAO TIẾP:
        • Thân thiện, tự nhiên, dùng "shop", "mình", "dạ"
        • Hỏi từng thông tin một, KHÔNG dồn dập
        • Câu trả lời ngắn gọn, rõ ràng
        • Nhiệt tình tư vấn như nhân viên bán hàng thật

        THÔNG TIN TOOLS:
        
        search_products(product_type, size=None, color=None, min_price=None, max_price=None)
        - product_type: T_SHIRT, SHIRT, DRESS, JEANS, PANTS, SHORTS, JACKET, SWEATER, HOODIE, SKIRT, SHOES, ACCESSORIES
        - size: XS, S, M, L, XL, XXL, XXXL, FREE_SIZE
        - color: BLACK, WHITE, GRAY, RED, BLUE, NAVY, GREEN, YELLOW, PINK, ORANGE, PURPLE, BROWN, BEIGE, MULTI
        
        get_product_detail(product_id)
        - Lấy chi tiết sản phẩm bằng ID
        
        check_product_availability(product_id, quantity)
        - Kiểm tra tồn kho
        
        create_order(customer_name, customer_phone, customer_address, product_id, quantity, customer_email=None, notes=None)
        - Tạo đơn hàng mới
        
        summary_order_info(product_id, quantity, customer_name, customer_phone, customer_address)
        - Tóm tắt đơn hàng trước khi tạo

        THÔNG TIN BỔ SUNG:
        - Ngày hôm nay: {0}
        - Thời gian giao hàng: 2-3 ngày
        - Phí vận chuyển: 30,000 VNĐ
        - Thanh toán: COD (Thanh toán khi nhận hàng)
        """
        
        today = datetime.now().strftime("%Y-%m-%d")

        # Create prompt template
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt.format(today)),
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

    def run(self, user_input: str) -> str:
        """Invoke the agent"""
        # Extract information from user input
        self._extract_info_from_input(user_input)
        
        print("===========================Collected Info:")
        print(self.collected_info)
        print("===========================Memory:")
        print(self.agent.memory.chat_memory.messages)
        
        # Build context string
        context = self._build_context_string()
        
        # Enhance input with context
        if context:
            enhanced_input = f"{user_input}\n\n[Thông tin đã có: {context}]"
        else:
            enhanced_input = user_input
        
        return self.agent.invoke({"input": enhanced_input})
    
    def _extract_info_from_input(self, user_input: str):
        """Extract structured information from user input"""
        user_lower = user_input.lower()
        
        # === EXTRACT PRODUCT TYPE ===
        product_type_map = {
            'áo thun': 'T_SHIRT',
            'ao thun': 'T_SHIRT',
            'thun': 'T_SHIRT',
            'áo sơ mi': 'SHIRT',
            'ao so mi': 'SHIRT',
            'sơ mi': 'SHIRT',
            'so mi': 'SHIRT',
            'áo khoác': 'JACKET',
            'ao khoac': 'JACKET',
            'khoác': 'JACKET',
            'khoac': 'JACKET',
            'hoodie': 'HOODIE',
            'áo len': 'SWEATER',
            'ao len': 'SWEATER',
            'quần jean': 'JEANS',
            'quan jean': 'JEANS',
            'jean': 'JEANS',
            'quần tây': 'PANTS',
            'quan tay': 'PANTS',
            'quần short': 'SHORTS',
            'quan short': 'SHORTS',
            'short': 'SHORTS',
            'váy': 'DRESS',
            'vay': 'DRESS',
            'đầm': 'DRESS',
            'dam': 'DRESS',
            'chân váy': 'SKIRT',
            'chan vay': 'SKIRT',
            'giày': 'SHOES',
            'giay': 'SHOES',
        }
        
        if not self.collected_info['product_type']:
            for keyword, ptype in product_type_map.items():
                if keyword in user_lower:
                    self.collected_info['product_type'] = ptype
                    break
        
        # === EXTRACT SIZE ===
        import re
        size_pattern = r'\b(xs|s|m|l|xl|xxl|xxxl|free[\s_-]?size)\b'
        size_match = re.search(size_pattern, user_lower)
        if size_match and not self.collected_info['size']:
            size = size_match.group(1).upper().replace(' ', '_').replace('-', '_')
            if 'FREE' in size:
                size = 'FREE_SIZE'
            self.collected_info['size'] = size
        
        # === EXTRACT COLOR ===
        color_map = {
            'đen': 'BLACK',
            'den': 'BLACK',
            'đen': 'BLACK',
            'trắng': 'WHITE',
            'trang': 'WHITE',
            'trắng': 'WHITE',
            'xám': 'GRAY',
            'xam': 'GRAY',
            'đỏ': 'RED',
            'do': 'RED',
            'đỏ': 'RED',
            'xanh dương': 'BLUE',
            'xanh duong': 'BLUE',
            'xanh': 'BLUE',
            'navy': 'NAVY',
            'xanh navy': 'NAVY',
            'xanh lá': 'GREEN',
            'xanh la': 'GREEN',
            'vàng': 'YELLOW',
            'vang': 'YELLOW',
            'hồng': 'PINK',
            'hong': 'PINK',
            'cam': 'ORANGE',
            'tím': 'PURPLE',
            'tim': 'PURPLE',
            'nâu': 'BROWN',
            'nau': 'BROWN',
            'be': 'BEIGE',
            'màu be': 'BEIGE',
        }
        
        if not self.collected_info['color']:
            for keyword, color in color_map.items():
                if keyword in user_lower:
                    self.collected_info['color'] = color
                    break
        
        # === EXTRACT QUANTITY ===
        quantity_pattern = r'(\d+)\s*(cái|chiếc|món|sản phẩm)?'
        quantity_match = re.search(quantity_pattern, user_lower)
        if quantity_match:
            try:
                qty = int(quantity_match.group(1))
                if 1 <= qty <= 100:  # Reasonable quantity
                    self.collected_info['quantity'] = qty
            except:
                pass
        
        # === EXTRACT PHONE NUMBER ===
        phone_pattern = r'0\d{9,10}|\+84\d{9,10}'
        phone_match = re.search(phone_pattern, user_input)
        if phone_match and not self.collected_info['customer_phone']:
            self.collected_info['customer_phone'] = phone_match.group(0)
        
        # === EXTRACT NAME ===
        # Nếu câu chứa "tên là" hoặc "tôi là" hoặc "mình là"
        name_patterns = [
            r'tên\s+(?:là\s+|:|)\s*([a-zA-ZÀ-ỹ\s]{2,50})',
            r'(?:tôi|mình)\s+là\s+([a-zA-ZÀ-ỹ\s]{2,50})',
            r'họ\s+tên\s+(?:là\s+|:|)\s*([a-zA-ZÀ-ỹ\s]{2,50})',
        ]
        
        if not self.collected_info['customer_name']:
            for pattern in name_patterns:
                match = re.search(pattern, user_input, re.IGNORECASE)
                if match:
                    name = match.group(1).strip()
                    # Clean up name (remove trailing words)
                    name = re.sub(r'\s+(ạ|nhé|nha|à|ơi)$', '', name, flags=re.IGNORECASE)
                    if len(name) >= 2:
                        self.collected_info['customer_name'] = name
                        break
        
        # === EXTRACT EMAIL ===
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, user_input)
        if email_match and not self.collected_info['customer_email']:
            self.collected_info['customer_email'] = email_match.group(0)
        
        # === EXTRACT ADDRESS ===
        # Nếu câu chứa "địa chỉ" hoặc patterns địa chỉ
        address_patterns = [
            r'địa\s+chỉ\s+(?:là\s+|:|)\s*(.+)',
            r'giao\s+(?:hàng\s+)?(?:tới|đến|về)\s+(.+)',
            r'(?:ở|tại)\s+(.{5,})',
        ]
        
        if not self.collected_info['customer_address']:
            for pattern in address_patterns:
                match = re.search(pattern, user_input, re.IGNORECASE)
                if match:
                    address = match.group(1).strip()
                    # Clean up address
                    address = re.sub(r'\s+(ạ|nhé|nha|à|ơi)$', '', address, flags=re.IGNORECASE)
                    if len(address) >= 5:
                        self.collected_info['customer_address'] = address
                        break
    
    def _build_context_string(self) -> str:
        """Build context string from collected info"""
        parts = []
        
        # Product search context
        if self.collected_info['product_type']:
            parts.append(f"Loại SP: {self.collected_info['product_type']}")
        if self.collected_info['size']:
            parts.append(f"Size: {self.collected_info['size']}")
        if self.collected_info['color']:
            parts.append(f"Màu: {self.collected_info['color']}")
        
        # Selected product context
        if self.collected_info['selected_product_id']:
            parts.append(f"Đã chọn SP ID: {self.collected_info['selected_product_id']}")
        if self.collected_info['quantity'] > 1:
            parts.append(f"SL: {self.collected_info['quantity']}")
        
        # Customer context
        if self.collected_info['customer_name']:
            parts.append(f"Tên: {self.collected_info['customer_name']}")
        if self.collected_info['customer_phone']:
            parts.append(f"SĐT: {self.collected_info['customer_phone']}")
        if self.collected_info['customer_address']:
            parts.append(f"Địa chỉ: {self.collected_info['customer_address'][:30]}...")
        
        return ', '.join(parts) if parts else ''
    
    def get_collected_info(self):
        """Get all collected information"""
        return self.collected_info.copy()
    
    def reset_collected_info(self):
        """Reset all collected information"""
        self.collected_info = {
            'product_type': None,
            'size': None,
            'color': None,
            'min_price': None,
            'max_price': None,
            'selected_product_id': None,
            'selected_product_name': None,
            'selected_product_price': None,
            'quantity': 1,
            'customer_name': None,
            'customer_phone': None,
            'customer_address': None,
            'customer_email': None,
            'notes': None,
        }
