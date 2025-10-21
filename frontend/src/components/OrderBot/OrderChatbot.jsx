import { useState, useRef, useEffect } from "react";
import { useStreamingResponse } from "../../hooks/useStreamingResponse";
import { toast } from "react-toastify";

const OrderChatbot = ({ onClose }) => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { type: "bot", message: "Chào bạn! Tôi có thể giúp bạn đặt hàng quần áo. Bạn muốn tìm sản phẩm gì?" },
  ]);
  const [chatHistory, setChatHistory] = useState([]);
  const messagesEndRef = useRef(null);
  const { streamResponse, loading } = useStreamingResponse();

  // Auto scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load chat history from localStorage on mount
  useEffect(() => {
    const savedHistory = localStorage.getItem('order_chat_history');
    if (savedHistory) {
      try {
        const parsed = JSON.parse(savedHistory);
        setChatHistory(parsed);
        // Rebuild messages display from history
        const rebuiltMessages = [{ type: "bot", message: "Chào bạn! Tôi có thể giúp bạn đặt hàng quần áo. Bạn muốn tìm sản phẩm gì?" }];
        parsed.forEach(msg => {
          if (msg.role === 'user') {
            rebuiltMessages.push({ type: "human", message: msg.content });
          } else if (msg.role === 'assistant' || msg.role === 'bot') {
            rebuiltMessages.push({ type: "bot", message: msg.content });
          }
        });
        setMessages(rebuiltMessages);
      } catch (error) {
        console.error('Failed to parse chat history:', error);
      }
    }
  }, []);

  // Save chat history to localStorage whenever it changes
  useEffect(() => {
    if (chatHistory.length > 0) {
      localStorage.setItem('order_chat_history', JSON.stringify(chatHistory));
    }
  }, [chatHistory]);

  const handleSendMessage = async () => {
    if (!input.trim()) return;
    const userInput = input.trim();
    setInput("");

    // Add user message to chat history
    const newUserMessage = { role: "user", content: userInput };
    const updatedHistory = [...chatHistory, newUserMessage];
    setChatHistory(updatedHistory);

    // Add user message to chat display
    setMessages((prevMessages) => [
      ...prevMessages,
      { type: "human", message: userInput },
      { type: "bot", message: "" }, // Placeholder for bot response
    ]);

    await streamResponse({
      user_input: userInput,
      chat_history: updatedHistory, // Gửi lịch sử chat xuống backend
      // Sử dụng endpoint backend mới cho order bot
      apiUrl: "http://localhost:8000/api/order-bot/order-chat/",
      onProgress: (result) => {
        // result là object { type, content }, chỉ lấy content là chuỗi
        setMessages((prevMessages) => {
          const newMessages = [...prevMessages];
          const lastMessage = newMessages[newMessages.length - 1];
          if (lastMessage && lastMessage.type === "bot") {
            lastMessage.message = result.content;
            return newMessages;
          }
          return newMessages;
        });
      },
      onFinish: (result) => {
        const botMessage = result.content;
        setMessages((prevMessages) => {
          const newMessages = [...prevMessages];
          const lastMessage = newMessages[newMessages.length - 1];
          if (lastMessage && lastMessage.type === "bot") {
            lastMessage.message = botMessage;
          }
          return newMessages;
        });
        // Add bot message to chat history
        const newBotMessage = { role: "assistant", content: botMessage };
        setChatHistory(prev => [...prev, newBotMessage]);
      },
      onError: (error) => {
        toast.error(`Error: ${error}`);
        setMessages((prevMessages) => {
          const newMessages = [...prevMessages];
          const lastMessage = newMessages[newMessages.length - 1];
          if (lastMessage && lastMessage.type === "bot") {
            lastMessage.message = "Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại.";
          }
          return newMessages;
        });
      }
    });
  };

  const BotMessage = ({ message }) => (
    <div className="flex justify-start">
      <div className="max-w-[80%] bg-white rounded-lg px-4 py-3 shadow-sm">
        <div className="flex items-start space-x-2">
          <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
            <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
          </div>
          <div className="text-gray-700 text-sm whitespace-pre-wrap">{message}</div>
        </div>
      </div>
    </div>
  );

  const HumanMessage = ({ message }) => (
    <div className="flex justify-end">
      <div className="max-w-[80%] bg-purple-600 rounded-lg px-4 py-3 shadow-sm">
        <div className="text-white text-sm whitespace-pre-wrap">{message}</div>
      </div>
    </div>
  );

  return (
    <div className="fixed bottom-6 right-6 z-50 w-full max-w-md">
      <div className="bg-white rounded-lg shadow-2xl h-[600px] flex flex-col">
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-4 rounded-t-lg flex justify-between items-center">
          <div>
            <h2 className="text-xl font-bold">AI Shopping Assistant</h2>
            <p className="text-sm text-purple-100">Tôi sẽ giúp bạn đặt hàng quần áo</p>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:bg-white hover:bg-opacity-20 p-2 rounded-full transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Messages Area */}
        <div className="flex-grow overflow-y-auto p-6 space-y-4 bg-gray-50">
          {messages.map((message, index) => {
            if (message.type === "bot") {
              return <BotMessage key={index} message={message.message} />;
            } else {
              return <HumanMessage key={index} message={message.message} />;
            }
          })}
          {loading && messages[messages.length - 1]?.message === "" && (
            <BotMessage message="Đang suy nghĩ..." />
          )}
          <div ref={messagesEndRef}></div>
        </div>

        {/* Input Area */}
        <div className="p-4 border-t bg-white rounded-b-lg">
          <div className="flex items-center space-x-2">
            <input
              className="flex-grow border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent text-sm"
              type="text"
              placeholder="Nhập yêu cầu của bạn, ví dụ: 'Tôi muốn một chiếc áo thun size M màu đen'"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey && !loading) {
                  e.preventDefault();
                  handleSendMessage();
                }
              }}
              disabled={loading}
            />
            <button
              className={`p-3 rounded-lg text-white ${
                loading ? "bg-gray-400" : "bg-purple-600 hover:bg-purple-700"
              }`}
              onClick={handleSendMessage}
              disabled={loading}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 10l7-7m0 0l7 7m-7-7v18"
                />
              </svg>
            </button>
            <button
              className="p-3 rounded-lg text-white bg-red-500 hover:bg-red-600"
              onClick={() => {
                localStorage.removeItem('order_chat_history');
                setChatHistory([]);
                setMessages([{ type: 'bot', message: 'Chào bạn! Tôi có thể giúp bạn đặt hàng quần áo. Bạn muốn tìm sản phẩm gì?' }]);
              }}
              title="Xóa lịch sử chat"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OrderChatbot;
