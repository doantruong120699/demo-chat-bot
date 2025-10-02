/* eslint-disable no-unused-vars */
import React, { useRef, useState, useEffect } from "react";
import { useStreamingResponse } from "../hooks/useStreamingResponse";
import { useAuth } from "../hooks/useAuth";
import { chat } from "../api/chat.js";
import ReactMarkdown from "react-markdown";

const HtmlMessage = ({ message }) => {
  return <div dangerouslySetInnerHTML={{ __html: message }} />;
};

// const HtmlMessage = ({ message }) => {
//   return (
//     <iframe
//       sandbox="allow-scripts"
//       srcDoc={message}
//       style={{ width: "100%", height: "300px", border: "none" }}
//     />
//   );
// };

const DelayedRender = ({ delay, children }) => {
  const [show, setShow] = useState(false);
  useEffect(() => {
    const timer = setTimeout(() => setShow(true), delay);
    return () => clearTimeout(timer);
  }, [delay]);
  return show ? children : (
    <div className="my-4 p-4 bg-gray-900 rounded-lg shadow-md">
      <div className="flex justify-center items-center h-32">
        <svg
          className="animate-spin h-6 w-6 text-gray-400"
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
            d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
            ></path>
          </svg>
        </div>
    </div>
  );
};

const HumanMessage = ({ message, userProfile }) => {
  return (
    <div className="flex justify-end">
      <div className="flex items-end w-auto bg-blue-500 dark:bg-gray-800 m-1 rounded-xl rounded-br-none sm:w-3/4 md:w-auto">
        <div className="p-2">
          <div className="text-gray-200">
            <ReactMarkdown>{message}</ReactMarkdown>
          </div>
        </div>
      </div>
    </div>
  );
};

const BotMessage = ({ message, isError = false, isLoading = false, htmlMessage = null, imageMessage = null, tableMessage = null }) => {
  if (isLoading) {
    return (
      <div className="flex flex-col w-3/4 ml-3">
        <div className="p-3 my-1 rounded-2xl rounded-bl-none sm:w-3/4 md:w-3/6 bg-purple-300 dark:bg-gray-800">
          <div className="text-xs text-gray-600 dark:text-gray-200">
            AI Assistant
          </div>
          <div className="text-gray-700 dark:text-gray-200">
            <div className="flex items-center space-x-2">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div
                  className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                  style={{ animationDelay: "0.1s" }}
                ></div>
                <div
                  className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                  style={{ animationDelay: "0.2s" }}
                ></div>
              </div>
              <span className="text-sm text-gray-500">Đợi chút...</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const onSaveImage = async () => { 
    const { toPng } = await import('html-to-image');
    const htmlElement = document.querySelector('.html-message-container');
    if (htmlElement) {
      const dataUrl = await toPng(htmlElement);
      const link = document.createElement('a');
      link.download = 'html-message.png';
      link.href = dataUrl;
      link.click();
    } else {
      alert('Could not find HTML message to save.');
    }
  };

  const handleSaveImage = async () => {
    try {
      await onSaveImage();
    } catch (err) {
      alert('Failed to save image');
      console.error(err);
    }
  };

  return (
    <div className="flex flex-col w-3/4 ml-3">
      <div
        className={`p-3 my-1 rounded-2xl rounded-bl-none sm:w-3/4 md:w-3/6 ${
          isError
            ? "bg-red-100 dark:bg-red-900 border border-red-200"
            : "bg-purple-300 dark:bg-gray-800"
        }`}
      >
        <div className="text-xs text-gray-600 dark:text-gray-200">
          AI Assistant
        </div>
        <div
          className={`${
            isError
              ? "text-red-700 dark:text-red-200"
              : "text-gray-700 dark:text-gray-200"
          }`}
        >
          <ReactMarkdown
            children={message || (isError ? "An error occurred. Please try again." : "")}
            skipHtml={false}
            components={{
              p: ({ node, ...props }) => (
                <p className="mb-2 leading-relaxed" {...props} />
              ),
              a: ({ node, ...props }) => (
                <a
                  className="text-blue-200 underline hover:text-blue-400 transition-colors"
                  target="_blank"
                  rel="noopener noreferrer"
                  {...props}
                />
              ),
              code: ({ node, inline, ...props }) =>
                inline ? (
                  <code
                    className="bg-gray-700 rounded px-1 py-0.5 text-purple-200 text-xs"
                    {...props}
                  />
                ) : (
                  <pre className="bg-gray-900 rounded-lg p-3 overflow-x-auto my-2 text-xs">
                    <code {...props} />
                  </pre>
                ),
              ul: ({ node, ...props }) => (
                <ul className="list-disc ml-6 mb-2" {...props} />
              ),
              ol: ({ node, ...props }) => (
                <ol className="list-decimal ml-6 mb-2" {...props} />
              ),
              li: ({ node, ...props }) => <li className="mb-1" {...props} />,
              blockquote: ({ node, ...props }) => (
                <blockquote
                  className="border-l-4 border-blue-400 pl-4 italic text-blue-100 bg-blue-900/30 my-2 py-1 rounded"
                  {...props}
                />
              ),
              strong: ({ node, ...props }) => (
                <strong className="font-semibold" {...props} />
              ),
              em: ({ node, ...props }) => <em className="italic" {...props} />,
              hr: () => <hr className="my-3 border-gray-600" />,
              h1: ({ node, ...props }) => (
                <h1
                  className="text-xl font-bold mt-2 mb-1 text-blue-200"
                  {...props}
                />
              ),
              h2: ({ node, ...props }) => (
                <h2
                  className="text-lg font-semibold mt-2 mb-1 text-blue-100"
                  {...props}
                />
              ),
              h3: ({ node, ...props }) => (
                <h3
                  className="text-base font-semibold mt-2 mb-1 text-blue-100"
                  {...props}
                />
              ),
              table: ({ node, ...props }) => (
                <table
                  className="min-w-full border-collapse my-2 bg-gray-800 rounded"
                  {...props}
                />
              ),
              th: ({ node, ...props }) => (
                <th
                  className="border-b border-gray-600 px-2 py-1 text-left text-gray-200"
                  {...props}
                />
              ),
              td: ({ node, ...props }) => (
                <td
                  className="border-b border-gray-700 px-2 py-1 text-gray-100"
                  {...props}
                />
              ),
            }}
          />
        </div>
      </div>
      {htmlMessage && (
        <div className="relative">
          {htmlMessage && (
            <DelayedRender delay={1000}>
              <HtmlMessage message={htmlMessage} />
            </DelayedRender>
          )}
          <button
            className="absolute top-8 right-5 px-1 text-white rounded transition hover:scale-105 hover:bg-white hover:text-black cursor-pointer"
            onClick={handleSaveImage}
          >
          <span className="inline-flex items-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5 inline-block"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2M7 10l5 5m0 0l5-5m-5 5V4"
              />
            </svg>
          </span>
          </button>
        </div>
      )}
     
      {tableMessage && (
        <div className="relative overflow-x-auto my-4">
          <table className="min-w-[300px] border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm bg-white dark:bg-gray-900">
            <tbody>
              {tableMessage.map((row, rowIndex) => (
                <tr
                  key={rowIndex}
                  className={
                    rowIndex === 0
                      ? "bg-gray-100 dark:bg-gray-800 font-semibold"
                      : rowIndex % 2 === 0
                      ? "bg-gray-50 dark:bg-gray-800"
                      : "bg-white dark:bg-gray-900"
                  }
                >
                  {row.map((cell, cellIndex) =>
                    rowIndex === 0 ? (
                      <th
                        key={cellIndex}
                        className="px-4 py-2 border-b border-gray-300 dark:border-gray-700 text-left text-gray-700 dark:text-gray-200"
                      >
                        {cell}
                      </th>
                    ) : (
                      <td
                        key={cellIndex}
                        className="px-4 py-2 border-b border-gray-200 dark:border-gray-800 text-gray-800 dark:text-gray-100"
                      >
                        {cell}
                      </td>
                    )
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {imageMessage && (
        <div className="relative">
          <img src={imageMessage} alt="Image" className="w-full h-auto" />
        </div>
      )}
    </div>
  );
};

const Messages = ({ chatId }) => {
  const { currentUser } = useAuth();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);
  // const [htmlMessage, setHtmlMessage] = useState("");
  const [imageMessage, setImageMessage] = useState("");
  const [tableMessage, setTableMessage] = useState([]);
  const { streamResponse, loading } = useStreamingResponse();

  useEffect(() => {
    const fetchChatDetail = async () => {
      if (!chatId) {
        setMessages([]);
        return;
      }

      try {
        const response = await chat.getChatDetail(chatId);
        console.log("Messages response", response);
        setMessages(response.data.messages || []);
      } catch (error) {
        console.error("Failed to fetch chat detail:", error);
        setMessages([]);
      }
    };
    fetchChatDetail();
  }, [chatId]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (userInput = null) => {
    if (!userInput || loading) return;

    setInput("");

    const userMessage = {
      id: Date.now(),
      message: userInput,
      sender: "HUMAN",
      timestamp: new Date().toISOString(),
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);

    const botMessageId = Date.now() + 1;
    const botMessage = {
      id: botMessageId,
      message: "",
      sender: "BOT",
      timestamp: new Date().toISOString(),
    };

    setMessages((prevMessages) => [...prevMessages, botMessage]);

    try {
      await streamResponse({
        user_input: userInput,
        chat_id: chatId,
        onProgress: (result) => {
          // Update the bot message with streaming content
          setMessages((prevMessages) =>
            prevMessages.map((msg) =>
              msg.id === botMessageId ? { ...msg, message: result.content } : msg
            )
          );
          if (result.type === "html") {
            // setHtmlMessage(result.content);
            setMessages((prevMessages) =>
              prevMessages.map((msg) =>
                msg.id === botMessageId ? { ...msg, html_message: result.content } : msg
              )
            );
          }
          scrollToBottom();
        },
        onGenerateImage: (result) => {
          setImageMessage("http://localhost:8000/media/" + result.content);
        },
        onGenerateTable: (result) => {
          const valid = result.content.replace(/'/g, '"');
          const data = JSON.parse(valid);
          setTableMessage(data);
        },
        onFinish: (result) => {
          // Final update to the bot message
          setMessages((prevMessages) =>
            prevMessages.map((msg) =>
              msg.id === botMessageId ? { ...msg, message: result } : msg
            )
          );
          scrollToBottom();
        },
        onError: (error) => {
          console.error("Streaming error:", error);
          // Handle error by updating the bot message
          setMessages((prevMessages) =>
            prevMessages.map((msg) =>
              msg.id === botMessageId
                ? {
                    ...msg,
                    message: "Sorry, I encountered an error. Please try again.",
                    isError: true,
                  }
                : msg
            )
          );
        },
      });
    } catch (error) {
      console.error("Failed to stream response:", error);
      // Handle error by updating the bot message
      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
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

  console.log(tableMessage)

  const handleClickExampleQuestion = async (question) => {
    setInput(question);
    setTimeout(async () => {
      await handleSendMessage(question);
    }, 100);
  };

  return (
    <div className="flex-grow h-full flex flex-col">
      {/* Messages Container */}
      <div className="w-full flex-grow my-2 p-2 overflow-y-auto mb-[76px] mt-[73px]">
        {messages.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg
                className="w-8 h-8 text-purple-600"
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
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Start a conversation
            </h3>
            <p className="text-gray-500">Ask me anything! I'm here to help.</p>
            {/* Example starter questions for the user */}
            <div className="space-y-4 text-sm mx-20 my-20">
              <div className="grid grid-cols-2 gap-3">
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
                      "Dự án Trí Tuệ Siêu Việt đã hoàn thành chưa?"
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
                    &quot;Dự án Trí Tuệ Siêu Việt đã hoàn thành chưa?&quot;
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
                      "Thống kê dự án Tosi Grow Holding"
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
                    &quot;Thống kê dự án Tosi Grow Holding&quot;
                  </span>
                </button>
              </div>
            </div>
          </div>
        ) : (
          messages.map((message) => {
            // Handle different possible sender field names
            const messageContent = message.message || message.content || "";

            if (message.sender === "HUMAN") {
              return (
                <div key={message.id || `human-${Date.now()}`}>
                  <HumanMessage
                    message={messageContent}
                    userProfile={currentUser}
                  />
                </div>
              );
            } else if (message.sender === "BOT") {
              return (
                <div key={message.id || `bot-${Date.now()}`}>
                  <BotMessage
                    message={messageContent}
                    isError={message.isError}
                    isLoading={!messageContent && !message.isError && loading}
                    htmlMessage={message.html_message}
                    imageMessage={imageMessage}
                    tableMessage={tableMessage}
                  />
                </div>
              );
            }
            console.log("Unknown message.sender:", message.sender);
            return null; // Handle any unexpected sender values
          })
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <div className="rounded-xl rounded-tr-none rounded-tl-none bg-gray-100 dark:bg-gray-800 fixed bottom-0 main-content">
        <div className="flex items-center">
          <div className="p-2 text-gray-600 dark:text-gray-200">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
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
              className="input text-gray-700 dark:text-gray-200 text-sm p-5 focus:outline-none bg-gray-100 dark:bg-gray-800 flex-grow rounded-l-md"
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
              className={`bg-gray-100 dark:bg-gray-800 dark:text-gray-200 flex justify-center items-center pr-3 rounded-r-md cursor-pointer ${
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
                  className="w-6 h-6 animate-spin"
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
                  className="h-6 w-6 transform rotate-90"
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
