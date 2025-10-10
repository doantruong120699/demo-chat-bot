import { useState, useRef, useEffect } from "react";
import {
  XMarkIcon,
  PaperAirplaneIcon,
  ChatBubbleLeftRightIcon,
} from "@heroicons/react/24/outline";
import { useStreamingResponseV2 } from "../../hooks/useStreamingResponseV2";
import UserMessage from "./UserMessage";
import BotMessage from "./BotMessage";
import Thinking from "./Thinking";

const BookingChatbot = ({ onClose, restaurant }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [hasStartedChat, setHasStartedChat] = useState(false);
  const [isClosing, setIsClosing] = useState(false);
  const messagesEndRef = useRef(null);
  const { streamResponse, thinking } = useStreamingResponseV2();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleClose = () => {
    setIsClosing(true);
    setTimeout(() => {
      onClose();
    }, 300);
  };

  const findAndUpdateMessagesState = (id, data) => {
    setMessages((prev) =>
      prev.map((msg) => (msg.id === id ? { ...msg, ...data } : msg))
    );
  };

  const handleSendMessage = async (e, text = null) => {
    e.preventDefault();
    const userInput = text || inputMessage;

    if (!userInput.trim()) return;

    if (!hasStartedChat) {
      setHasStartedChat(true);
    }

    const userMessage = {
      id: Date.now(),
      type: "user",
      content: userInput,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    const currentMessage = userInput;
    setInputMessage("");

    const botMessageId = Date.now() + 1;
    const botMessage = {
      id: botMessageId,
      type: "bot",
      content: "",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, botMessage]);

    try {
      const chatHistory = messages.map((msg) => ({
        role: msg.type === "user" ? "user" : "assistant",
        content: msg.content,
      }));

      await streamResponse({
        user_input: currentMessage,
        chat_history: chatHistory,
        onProgress: ({ type, content }) => {
          if (type === "token") {
            findAndUpdateMessagesState(botMessageId, { content: content });
          }
        },
        onFinish: ({ content }) => {
          findAndUpdateMessagesState(botMessageId, { content: content });
        },
        onError: (error) => {
          console.error("Streaming error:", error);
          findAndUpdateMessagesState(botMessageId, {
            content: "Sorry, I encountered an error. Please try again: ",
          });
        },
      });
    } catch (error) {
      console.error("Error sending message:", error);
      findAndUpdateMessagesState(botMessageId, {
        content: "Xin lỗi đã xảy ra lỗi. Vui lòng thử lại sau",
      });
    }
  };

  const quickActions = [
    "Hôm nay có bàn trống không?",
    "Tôi tìm bàn cho 2 người",
    "Tôi tìm bàn cho 4 người",
    "Giờ hoạt động của bạn là bao nhiêu?",
  ];

  return (
    <div
      className={`fixed inset-0 flex items-end justify-end z-50 ${
        isClosing ? "animate-fadeOut" : "animate-fadeIn"
      }`}
    >
      <div
        className={`bg-white rounded-t-2xl shadow-2xl w-full max-w-xl h-[800px] flex flex-col transform transition-all duration-500 ease-in-out ${
          isClosing ? "animate-slideDown" : "animate-slideUp"
        }`}
      >
        {/* Header */}
        <div
          className={`flex items-center justify-between p-2 border-b bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-t-2xl ${
            isClosing ? "animate-slideDown" : "animate-bounceIn"
          }`}
        >
          <div className="flex items-center">
            <div className="w-10 h-10 rounded-xl flex items-center justify-center mr-3 animate-pulse">
              <ChatBubbleLeftRightIcon className="w-6 h-6" />
            </div>
            <div>
              <span className="font-bold text-lg">PSCD Booking Assistant</span>
              <p className="text-blue-100 text-sm">Online now</p>
            </div>
          </div>
          <button
            onClick={handleClose}
            className="text-white hover:text-gray-200 transition-all duration-200 p-2 hover:bg-white hover:bg-opacity-20 rounded-lg hover:scale-110"
          >
            <XMarkIcon className="w-6 h-6" />
          </button>
        </div>

        {/* Messages */}
        <div
          className={`flex-1 p-6 space-y-4 bg-gray-50 ${
            hasStartedChat ? "overflow-y-auto" : "overflow-hidden"
          } ${isClosing ? "animate-fadeOut" : ""}`}
        >
          {!hasStartedChat ? (
            <div className="flex items-center justify-center h-full overflow-hidden">
              <div className="text-center px-4 w-full animate-bounceIn">
                <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4 animate-pulse">
                  <ChatBubbleLeftRightIcon className="w-8 h-8 text-white" />
                </div>
                <h3
                  className="text-xl font-semibold text-gray-700 mb-2 animate-fadeIn"
                  style={{ animationDelay: "0.3s" }}
                >
                  Hello! I'm your dining assistant for {restaurant.name}{" "}
                </h3>
                <p
                  className="text-gray-500 text-sm animate-fadeIn"
                  style={{ animationDelay: "0.6s" }}
                >
                  Start a conversation with our AI assistant
                </p>
              </div>
            </div>
          ) : (
            <>
              {messages.map((message, index) => {
                if (message.type === "user") {
                  return (
                    <UserMessage
                      key={message.id}
                      message={message}
                      index={index}
                    />
                  );
                } else if (message.type === "bot") {
                  if (index === messages.length - 1 && thinking) {
                    return <Thinking key={message.id} />;
                  }
                  return (
                    <BotMessage
                      key={message.id}
                      message={message}
                      index={index}
                    />
                  );
                }
                return null;
              })}
            </>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="px-6 py-4 bg-white animate-slideUp">
          <p className="text-sm font-semibold text-gray-700 mb-3">
            Lựa chọn nhanh:
          </p>
          <div className="flex flex-wrap gap-2">
            {quickActions.map((action, index) => (
              <button
                key={index}
                onClick={(e) => handleSendMessage(e, action)}
                className="text-sm bg-gradient-to-r from-blue-50 to-purple-50 text-blue-700 px-4 py-2 rounded-xl hover:from-blue-100 hover:to-purple-100 transition-all duration-200 border border-blue-200 hover:border-blue-300 hover:shadow-sm hover:scale-105 animate-bounceIn"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                {action}
              </button>
            ))}
          </div>
        </div>

        <form
          onSubmit={handleSendMessage}
          className="px-6 pb-6 bg-white animate-slideUp"
        >
          <div className="flex space-x-3">
            <div className="flex-1 relative">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Type your message..."
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm transition-all duration-200 hover:border-blue-400 focus:scale-105 resize-none"
                rows={1}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    if (inputMessage.trim()) {
                      // trigger submit form
                      e.target.form && e.target.form.requestSubmit();
                    }
                  }
                  // If Shift+Enter, allow to add line break (default browser behavior)
                }}
              />
            </div>
            <button
              type="submit"
              disabled={!inputMessage.trim()}
              className={`p-3 rounded-xl transition-all duration-200 transform hover:scale-110 ${
                !inputMessage.trim()
                  ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                  : "bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 shadow-lg hover:shadow-xl animate-pulse"
              }`}
            >
              <PaperAirplaneIcon className="w-5 h-5" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default BookingChatbot;
