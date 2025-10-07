/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable no-unused-vars */
import React, { useRef, useState, useEffect, useMemo } from "react";
import { useStreamingResponse } from "../hooks/useStreamingResponse";
import { useAuth } from "../hooks/useAuth";
import { chat } from "../api/chat.js";
import ReactMarkdown from "react-markdown";
import { Table, Button, Dialog, Flex, Inset } from "@radix-ui/themes";
import ApexCharts from "apexcharts";

const DelayedRender = ({ delay, children, spinnerClassName="", className="w-full" }) => {
  const [show, setShow] = useState(false);
  useEffect(() => {
    const timer = setTimeout(() => setShow(true), delay);
    return () => clearTimeout(timer);
  }, [delay]);
  return show ? (
    <div style={{ position: "relative", overflow: "hidden" }} className={className}>
      <div
        style={{
          position: "relative",
          zIndex: 1,
          // Ban đầu children bị che, sau đó hiển thị dần dần bằng mask
          WebkitMaskImage:
            "linear-gradient(to bottom, black 0%, black 0%, transparent 0%, transparent 100%)",
          maskImage:
            "linear-gradient(to bottom, black 0%, black 0%, transparent 0%, transparent 100%)",
          animation:
            "revealChildrenMaskDown 1.5s cubic-bezier(0.23, 1, 0.32, 1) forwards",
        }}
      >
        {children}
      </div>
      <style>
        {`
          @keyframes revealChildrenMaskDown {
            0%   {
              -webkit-mask-image: linear-gradient(to bottom, black 0%, black 0%, transparent 0%, transparent 100%);
              mask-image: linear-gradient(to bottom, black 0%, black 0%, transparent 0%, transparent 100%);
            }
            10%  {
              -webkit-mask-image: linear-gradient(to bottom, black 0%, black 10%, transparent 10%, transparent 100%);
              mask-image: linear-gradient(to bottom, black 0%, black 10%, transparent 10%, transparent 100%);
            }
            20%  {
              -webkit-mask-image: linear-gradient(to bottom, black 0%, black 20%, transparent 20%, transparent 100%);
              mask-image: linear-gradient(to bottom, black 0%, black 20%, transparent 20%, transparent 100%);
            }
            30%  {
              -webkit-mask-image: linear-gradient(to bottom, black 0%, black 30%, transparent 30%, transparent 100%);
              mask-image: linear-gradient(to bottom, black 0%, black 30%, transparent 30%, transparent 100%);
            }
            40%  {
              -webkit-mask-image: linear-gradient(to bottom, black 0%, black 40%, transparent 40%, transparent 100%);
              mask-image: linear-gradient(to bottom, black 0%, black 40%, transparent 40%, transparent 100%);
            }
            50%  {
              -webkit-mask-image: linear-gradient(to bottom, black 0%, black 50%, transparent 50%, transparent 100%);
              mask-image: linear-gradient(to bottom, black 0%, black 50%, transparent 50%, transparent 100%);
            }
            60%  {
              -webkit-mask-image: linear-gradient(to bottom, black 0%, black 60%, transparent 60%, transparent 100%);
              mask-image: linear-gradient(to bottom, black 0%, black 60%, transparent 60%, transparent 100%);
            }
            70%  {
              -webkit-mask-image: linear-gradient(to bottom, black 0%, black 70%, transparent 70%, transparent 100%);
              mask-image: linear-gradient(to bottom, black 0%, black 70%, transparent 70%, transparent 100%);
            }
            80%  {
              -webkit-mask-image: linear-gradient(to bottom, black 0%, black 80%, transparent 80%, transparent 100%);
              mask-image: linear-gradient(to bottom, black 0%, black 80%, transparent 80%, transparent 100%);
            }
            90%  {
              -webkit-mask-image: linear-gradient(to bottom, black 0%, black 90%, transparent 90%, transparent 100%);
              mask-image: linear-gradient(to bottom, black 0%, black 90%, transparent 90%, transparent 100%);
            }
            100% {
              -webkit-mask-image: linear-gradient(to bottom, black 0%, black 100%, transparent 100%, transparent 100%);
              mask-image: linear-gradient(to bottom, black 0%, black 100%, transparent 100%, transparent 100%);
            }
          }
        `}
      </style>
    </div>
  ) : (
    <div className={`my-4 p-4 rounded-lg shadow-md ${spinnerClassName}`}>
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
      <div className="flex items-end w-auto bg-blue-500 dark:bg-gray-800 my-2 rounded-xl rounded-br-none sm:w-3/4 md:w-auto">
        <div className="p-2">
          <div className="text-gray-200">
            <ReactMarkdown>{message}</ReactMarkdown>
          </div>
        </div>
      </div>
    </div>
  );
};

const ChatExtraData = ({ extraData }) => {
  const chartRef = useRef(null);

  // Memoize labels and series to avoid recalculating on every render
  const { labels, series } = useMemo(() => {
    if (
      Array.isArray(extraData) &&
      extraData.length > 1 &&
      extraData.every(row => Array.isArray(row))
    ) {
      return {
        labels: extraData.slice(1).map(row => row[0]),
        series: extraData.slice(1).map(row => Number(row[1]) || 0),
      };
    }
    return { labels: [], series: [] };
  }, [extraData]);

  useEffect(() => {
    let chart;
    const timeout = setTimeout(() => {
      if (chartRef.current && series.length && labels.length) {
        const options = {
          series,
          labels,
          colors: ["#1C64F2", "#16BDCA", "#9061F9"],
          chart: { type: "pie", height: 300, width: "100%" },
          stroke: { colors: ["white"] },
          plotOptions: { pie: { size: "100%" } },
          dataLabels: { enabled: true, style: { fontFamily: "Inter, sans-serif" } },
          legend: { position: "bottom", fontFamily: "Inter, sans-serif" },
        };

        chart = new ApexCharts(chartRef.current, options);
        chart.render();
      }
    }, 2000);

    return () => {
      clearTimeout(timeout);
      if (chart) {
        chart.destroy();
      }
    };
  }, [series, labels, chartRef.current]);

  return (
    <DelayedRender delay={1000} spinnerClassName="w-1/2 bg-white rounded-lg shadow-sm dark:bg-gray-800 p-1">
      <div className="rounded-lg shadow-sm p-1">
        <div className="flex justify-center items-center w-full">
          <h5 className="text-xl font-bold text-gray-900">
            Biểu đồ tổng quan
          </h5>
        </div>
        <div>
          <div ref={chartRef} />
        </div>
      </div>
    </DelayedRender>
  );
};

const TableExtraData = ({ extraData }) => {
  const [selectedRow, setSelectedRow] = useState(null);
  if (extraData && extraData.length > 0) {
    return (
      <DelayedRender delay={1000} spinnerClassName="w-1/2 bg-white rounded-lg shadow-sm dark:bg-gray-800 p-1">
        <Dialog.Root>
          <Table.Root variant="surface">
            <Table.Header>
              <Table.Row>
                {extraData[0].map((item, index) => (
                  <Table.ColumnHeaderCell key={index}>
                    {item}
                  </Table.ColumnHeaderCell>
                ))}
                {/* <Table.ColumnHeaderCell>Action</Table.ColumnHeaderCell> */}
              </Table.Row>
            </Table.Header>
            <Table.Body>
              {extraData.slice(1).map((item, index) => (
                <Table.Row key={index}>
                  {item.slice(0, -1).map((item, index) => (
                    <Table.Cell key={index}>{item}</Table.Cell>
                  ))}
                  <Table.Cell>
                    <Dialog.Trigger onClick={() => setSelectedRow(item)}>
                      <Button className="cursor-pointer">View</Button>
                    </Dialog.Trigger>
                  </Table.Cell>
                </Table.Row>
              ))}
            </Table.Body>
          </Table.Root>
          {selectedRow && (
            <Dialog.Content>
              <Dialog.Title>{selectedRow[0]}</Dialog.Title>
              <Dialog.Description>
                Thông tin chi tiết về thời gian làm việc ở các task
              </Dialog.Description>

              <Inset side="y" my="5">
                <Table.Root>
                  <Table.Header>
                    <Table.Row>
                      {selectedRow[selectedRow.length - 1][0].map(
                        (item, index) => (
                          <Table.ColumnHeaderCell key={index}>
                            {item}
                          </Table.ColumnHeaderCell>
                        )
                      )}
                    </Table.Row>
                  </Table.Header>

                  <Table.Body>
                    {selectedRow[selectedRow.length - 1]
                      .slice(1)
                      .map((item, index) => (
                        <Table.Row key={index}>
                          {item.map((item, index) => (
                            <Table.Cell key={index}>{item}</Table.Cell>
                          ))}
                        </Table.Row>
                      ))}
                  </Table.Body>
                </Table.Root>
              </Inset>

              <Flex gap="3" justify="end">
                <Dialog.Close>
                  <Button variant="soft" color="gray">
                    Close
                  </Button>
                </Dialog.Close>
              </Flex>
            </Dialog.Content>
          )}
        </Dialog.Root>
      </DelayedRender>
    );
  }
  return null;
};

const BotMessage = ({
  message,
  isError = false,
  isLoading = false,
  imageMessage = null,
  extraData = null,
  isFinishGenerateText = false,
}) => {
  if (isLoading) {
    return (
      <div className="flex flex-col ml-3">
        <div className="p-3 my-3 rounded-2xl rounded-bl-none w-1/5 bg-purple-300 dark:bg-gray-800">
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

  return (
    <div className="flex flex-col w-full">
      <div
        className={`p-3 my-3 rounded-2xl rounded-bl-none sm:w-3/4 md:w-3/4 ${
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
            children={
              message || (isError ? "An error occurred. Please try again." : "")
            }
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

      {(isFinishGenerateText === true || isFinishGenerateText === null) && (
        <>
          {imageMessage && (
            <div className="relative">
              <img src={imageMessage} alt="Image" className="w-3/4 h-auto" />
            </div>
          )}
          {extraData && (
            <div className="mt-2 flex flex-row gap-2 w-3/4 justify-between">
              <TableExtraData extraData={extraData} />
              <ChatExtraData extraData={extraData} />
            </div>
          )}
        </>
      )}
      
    </div>
  );
};

const Messages = ({ chatId }) => {
  const { currentUser } = useAuth();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);
  const [imageMessage, setImageMessage] = useState("");
  const { streamResponse, loading } = useStreamingResponse();
  const [isFinishGenerateText, setIsFinishGenerateText] = useState(null);

  useEffect(() => {
    const fetchChatDetail = async () => {
      if (!chatId) {
        setMessages([]);
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
        setMessages(cleanMessages || []);
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
    setIsFinishGenerateText(false);

    try {
      await streamResponse({
        user_input: userInput,
        chat_id: chatId,
        onProgress: (result) => {
          setMessages((prevMessages) =>
            prevMessages.map((msg) =>
              msg.id === botMessageId
                ? { ...msg, message: result.content }
                : msg
            )
          );
          scrollToBottom();
        },
        onGenerateImage: (result) => {
          setImageMessage("http://localhost:8000/media/" + result.content);
        },
        onGenerateExtraData: (result) => {
          const valid = result.content.replace(/'/g, '"');
          const data = JSON.parse(valid);
          // setExtraData(data);
          setMessages((prevMessages) =>
            prevMessages.map((msg) =>
              msg.id === botMessageId ? { ...msg, extra_data: data } : msg
            )
          );
        },
        onFinish: (result) => {
          setIsFinishGenerateText(true);
          setMessages((prevMessages) =>
            prevMessages.map((msg) =>
              msg.id === botMessageId ? { ...msg, message: result } : msg
            )
          );
          scrollToBottom();
        },
        onError: (error) => {
          console.error("Streaming error:", error);
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
                    &quot;Thống kê thời gian làm việc của dự án AI Chat Application&quot;
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
                    imageMessage={imageMessage}
                    extraData={message.extra_data}
                    isFinishGenerateText={isFinishGenerateText}
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
