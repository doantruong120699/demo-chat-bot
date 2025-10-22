import React, { useRef, useState, useEffect } from "react";
import { useStreamingResponse } from "../../hooks/useStreamingResponse.js";
import { useAuth } from "../../hooks/useAuth.js";
import { chat } from "../../api/chat.js";
import HumanMessage from "./HumanMessage";
import BotMessage from "./BotMessage";

const Messages = ({ chatId }) => {
  const { currentUser } = useAuth();
  const [messages, setMessages] = useState([]); // Old messages from chat history
  const [newMessages, setNewMessages] = useState([]); // New messages during current session
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);
  const [imageMessage, setImageMessage] = useState("");
  const { streamResponse, loading } = useStreamingResponse();
  const [isFinishGenerateText, setIsFinishGenerateText] = useState(null);

  useEffect(() => {
    const fetchChatDetail = async () => {
      if (!chatId) {
        setMessages([]);
        setNewMessages([]);
        return;
      }

      try {
        const response = await chat.getChatDetail(chatId);
        const cleanMessages = response.data.messages.map((message) => {
          if (message.extra_data) {
            const valid = message.extra_data.replace(/'/g, '"');
            const data = JSON.parse(valid);
            return { ...message, extra_data: data };
          }
          return message;
        });
        setMessages(cleanMessages || []); // Set old messages from chat history
        setNewMessages([]); // Clear new messages when loading chat history
      } catch (error) {
        console.error("Failed to fetch chat detail:", error);
        setMessages([]);
        setNewMessages([]);
      }
    };
    fetchChatDetail();
  }, [chatId]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, newMessages]);


  const handleSendMessage = async (userInput = null) => {
    if (!userInput || loading) return;

    setInput("");

    let userMessage = {
      id: Date.now(),
      message: userInput,
      sender: "HUMAN",
      timestamp: new Date().toISOString(),
    };
    let botMessageId = Date.now() + 1;
    let botMessage = {
      id: botMessageId,
      message: "",
      sender: "BOT",
      timestamp: new Date().toISOString(),
      extra_data: null,
      isError: false,
    };

    setNewMessages((prevNewMessages) => [...prevNewMessages, userMessage, botMessage]);
    setIsFinishGenerateText(false);

    try {
      await streamResponse({
        user_input: userInput,
        chat_id: chatId,
        onProgress: (result) => {
          setNewMessages((prevNewMessages) => {
            return prevNewMessages.map((msg) =>
              msg.id === botMessageId
                ? { ...msg, message: result?.content ?? "" }
                : msg
            );
          });
          scrollToBottom();
        },
        onGenerateImage: (result) => {
          if (result && result.content) {
            setImageMessage(`http://localhost:8000/media/${result.content}`);
            setNewMessages((prevNewMessages) =>
              prevNewMessages.map((msg) =>
                msg.id === botMessageId
                  ? { ...msg, extra_data: result.content }
                  : msg
              )
            );
          }
        },
        onGenerateExtraData: (result) => {
          if (result && result.content) {
            try {
              const valid = result.content.replace(/'/g, '"');
              const data = JSON.parse(valid);
              botMessage.extra_data = data;
              setNewMessages((prevNewMessages) =>
                prevNewMessages.map((msg) =>
                  msg.id === botMessageId ? { ...msg, extra_data: data } : msg
                )
              );
            } catch (e) {
              console.error("Failed to parse extra data:", e);
            }
          }
        },
        onFinish: (result) => {
          botMessage.message = result.content;
          setIsFinishGenerateText(true);
          setMessages((prevMessages) => {
            return [...prevMessages, userMessage, botMessage]
          });
          setNewMessages([]);
          scrollToBottom();
        },
        onError: (error) => {
          console.error("Streaming error:", error);
          setNewMessages((prevNewMessages) =>
            prevNewMessages.map((msg) =>
              msg.id === botMessageId
                ? {
                    ...msg,
                    isError: true,
                    message: "Sorry, I encountered an error. Please try again.",
                  }
                : msg
            )
          );
        },
      });
    } catch (error) {
      console.error("Failed to stream response:", error);
      setNewMessages((prevNewMessages) =>
        prevNewMessages.map((msg) =>
          msg.id === botMessageId
            ? {
                ...msg,
                message: "Sorry, I encountered an error. Please try again.",
                isError: true,
              }
            : msg
        )
      );
    }
  };

  const handleClickExampleQuestion = async (question) => {
    setInput(question);
    setTimeout(async () => {
      await handleSendMessage(question);
    }, 100);
  };

  return (
    <div className="flex-grow h-full flex flex-col">
      {/* Messages Container */}
      <div className="w-full flex-grow my-2 pl-4 pr-4 overflow-y-auto mb-[76px] mt-[73px]">
        {messages.length === 0 && newMessages.length === 0 ? (
          <div className="text-center py-8 sm:py-12">
            <div className="w-12 h-12 sm:w-16 sm:h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg
                className="w-6 h-6 sm:w-8 sm:h-8 text-purple-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                />
              </svg>
            </div>
            <h3 className="text-base sm:text-lg font-medium text-gray-900 mb-2">
              Start a conversation
            </h3>
            <p className="text-sm sm:text-base text-gray-500">Ask me anything! I'm here to help.</p>
            {/* Example starter questions for the user */}
            <div className="space-y-4 text-sm mx-4 sm:mx-8 lg:mx-20 my-8 sm:my-12 lg:my-20">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <button
                  className="cursor-pointer group rounded-xl bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-100 px-4 py-3 text-left text-gray-700 transition-all duration-200 hover:from-blue-100 hover:to-indigo-100 hover:border-blue-200 hover:shadow-md hover:scale-[1.02] dark:from-blue-900/20 dark:to-indigo-900/20 dark:border-blue-800 dark:text-gray-300 dark:hover:from-blue-900/30 dark:hover:to-indigo-900/30"
                  onClick={async () =>
                    await handleClickExampleQuestion(
                      "Hôm nay có bao nhiêu yêu cầu xin nghỉ?"
                    )
                  }
                >
                  <span className="flex items-center gap-2">
                    <svg
                      className="h-4 w-4 text-blue-500 opacity-70 group-hover:opacity-100 transition-opacity"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                    &quot;Hôm nay có bao nhiêu yêu cầu xin nghỉ?&quot;
                  </span>
                </button>
                <button
                  className="cursor-pointer group rounded-xl bg-gradient-to-r from-emerald-50 to-green-50 border border-emerald-100 px-4 py-3 text-left text-gray-700 transition-all duration-200 hover:from-emerald-100 hover:to-green-100 hover:border-emerald-200 hover:shadow-md hover:scale-[1.02] dark:from-emerald-900/20 dark:to-green-900/20 dark:border-emerald-800 dark:text-gray-300 dark:hover:from-emerald-900/30 dark:hover:to-green-900/30"
                  onClick={async () =>
                    await handleClickExampleQuestion(
                      "Thống kê thời gian làm việc của dự án AI Chat Application"
                    )
                  }
                >
                  <span className="flex items-center gap-2">
                    <svg
                      className="h-4 w-4 text-emerald-500 opacity-70 group-hover:opacity-100 transition-opacity"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                      />
                    </svg>
                    &quot;Thống kê thời gian làm việc của dự án AI Chat
                    Application&quot;
                  </span>
                </button>
                <button
                  className="cursor-pointer group rounded-xl bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-100 px-4 py-3 text-left text-gray-700 transition-all duration-200 hover:from-purple-100 hover:to-pink-100 hover:border-purple-200 hover:shadow-md hover:scale-[1.02] dark:from-purple-900/20 dark:to-pink-900/20 dark:border-purple-800 dark:text-gray-300 dark:hover:from-purple-900/30 dark:hover:to-pink-900/30"
                  onClick={async () =>
                    await handleClickExampleQuestion(
                      "Tuần tới có yêu cầu xin nghỉ nào không?"
                    )
                  }
                >
                  <span className="flex items-center gap-2">
                    <svg
                      className="h-4 w-4 text-purple-500 opacity-70 group-hover:opacity-100 transition-opacity"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
                      />
                    </svg>
                    &quot;Tuần tới có yêu cầu xin nghỉ nào không?&quot;
                  </span>
                </button>
                <button
                  className="cursor-pointer group rounded-xl bg-gradient-to-r from-amber-50 to-yellow-50 border border-amber-100 px-4 py-3 text-left text-gray-700 transition-all duration-200 hover:from-amber-100 hover:to-yellow-100 hover:border-amber-200 hover:shadow-md hover:scale-[1.02] dark:from-amber-900/20 dark:to-yellow-900/20 dark:border-amber-800 dark:text-gray-300 dark:hover:from-amber-900/30 dark:hover:to-yellow-900/30"
                  onClick={async () =>
                    await handleClickExampleQuestion(
                      "Thống kê thời gian làm việc của dự án Tosi Grow Holding"
                    )
                  }
                >
                  <span className="flex items-center gap-2">
                    <svg
                      className="h-4 w-4 text-amber-500 opacity-70 group-hover:opacity-100 transition-opacity"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"
                      />
                    </svg>
                    &quot;Thống kê thời gian làm việc của dự án Tosi Grow
                    Holding&quot;
                  </span>
                </button>
              </div>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message) => {
              const messageContent = message.message || message.content || "";
              if (message.sender === "HUMAN") {
                return (
                  <div key={message.id || `human-${message.id || Date.now()}`}>
                    <HumanMessage
                      message={messageContent}
                      userProfile={currentUser}
                    />
                  </div>
                );
              } else if (message.sender === "BOT") {
                return (
                  <div key={message.id || `bot-${message.id || Date.now()}`}>
                    <BotMessage
                      message={messageContent}
                      isError={message.isError}
                      isLoading={false}
                      imageMessage={imageMessage}
                      extraData={message.extra_data}
                      isFinishGenerateText={true}
                    />
                  </div>
                );
              }
              return null;
            })}
            {newMessages.map((message) => {
              const messageContent = message.message || message.content || "";

              if (message.sender === "HUMAN") {
                return (
                  <div key={message.id || `human-${message.id || Date.now()}`}>
                    <HumanMessage
                      message={messageContent}
                      userProfile={currentUser}
                    />
                  </div>
                );
              } else if (message.sender === "BOT") {
                return (
                  <div key={message.id || `bot-${message.id || Date.now()}`}>
                    <BotMessage
                      message={messageContent}
                      isError={message.isError}
                      isLoading={!messageContent && !message.isError && loading}
                      imageMessage={imageMessage}
                      extraData={message.extra_data}
                      isFinishGenerateText={isFinishGenerateText}
                    />
                  </div>
                );
              }
              console.log("Unknown message.sender:", message.sender);
              return null; // Handle any unexpected sender values
            })}
          </>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <div className="rounded-xl rounded-tr-none rounded-tl-none bg-gray-100 dark:bg-gray-800 fixed bottom-0 left-0 right-0 lg:left-auto lg:right-auto main-content">
        <div className="flex items-center">
          <div className="p-2 text-gray-600 dark:text-gray-200 flex-shrink-0">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5 sm:h-6 sm:w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <div className="search-chat flex flex-grow p-2">
            <input
              className="input text-gray-700 dark:text-gray-200 text-sm p-3 sm:p-5 focus:outline-none bg-gray-100 dark:bg-gray-800 flex-grow rounded-l-md"
              type="text"
              placeholder="Type your message..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (
                  e.key === "Enter" &&
                  !e.shiftKey &&
                  input.trim() &&
                  !loading
                ) {
                  e.preventDefault();
                  handleSendMessage(input);
                }
              }}
              disabled={loading}
            />
            <div
              className={`bg-gray-100 dark:bg-gray-800 dark:text-gray-200 flex justify-center items-center px-2 sm:px-3 rounded-r-md cursor-pointer ${
                input.trim() && !loading
                  ? "text-gray-600 hover:text-gray-800"
                  : "text-gray-400 cursor-not-allowed"
              }`}
              onClick={() =>
                input.trim() && !loading && handleSendMessage(input)
              }
            >
              {loading ? (
                <svg
                  className="w-5 h-5 sm:w-6 sm:h-6 animate-spin"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
              ) : (
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-5 w-5 sm:h-6 sm:w-6 transform rotate-90"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                  />
                </svg>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Messages;
