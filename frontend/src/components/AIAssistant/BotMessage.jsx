import React, { useRef, useState, useEffect, useMemo } from "react";
import ReactMarkdown from "react-markdown";
import { Table, Button, Dialog, Flex, Inset } from "@radix-ui/themes";
import ApexCharts from "apexcharts";

const DelayedRender = ({
  delay,
  children,
  spinnerClassName = "",
  className = "w-full",
}) => {
  const [show, setShow] = useState(false);
  useEffect(() => {
    const timer = setTimeout(() => setShow(true), delay);
    return () => clearTimeout(timer);
  }, [delay]);
  return show ? (
    <div
      style={{ position: "relative", overflow: "hidden" }}
      className={className}
    >
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

const ChatExtraData = ({ extraData }) => {
  const chartRef = useRef(null);

  const { labels, series } = useMemo(() => {
    if (
      Array.isArray(extraData) &&
      extraData.length > 1 &&
      extraData.every((row) => Array.isArray(row))
    ) {
      return {
        labels: extraData.slice(1).map((row) => row[0]),
        series: extraData.slice(1).map((row) => Number(row[1]) || 0),
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
          dataLabels: {
            enabled: true,
            style: { fontFamily: "Inter, sans-serif" },
          },
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
  }, [series, labels]);

  return (
    <DelayedRender
      delay={1000}
      spinnerClassName="w-1/2 bg-white rounded-lg shadow-sm dark:bg-gray-800 p-1"
    >
      <div className="rounded-lg shadow-sm p-1">
        <div className="flex justify-center items-center w-full">
          <h5 className="text-xl font-bold text-gray-900">Biểu đồ tổng quan</h5>
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
      <DelayedRender
        delay={1000}
        spinnerClassName="w-1/2 bg-white rounded-lg shadow-sm dark:bg-gray-800 p-1"
      >
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
      <div className="flex flex-col ml-2 sm:ml-3">
        <div className="p-3 my-3 rounded-2xl rounded-bl-none w-3/4 sm:w-2/3 md:w-1/2 lg:w-1/5 bg-purple-300 dark:bg-gray-800">
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
        className={`p-3 my-3 rounded-2xl rounded-bl-none w-3/4 sm:w-2/3 md:w-1/2 lg:w-3/4 ${
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
              p: ({ ...props }) => (
                <p className="mb-2 leading-relaxed" {...props} />
              ),
              a: ({ ...props }) => (
                <a
                  className="text-blue-200 underline hover:text-blue-400 transition-colors"
                  target="_blank"
                  rel="noopener noreferrer"
                  {...props}
                />
              ),
              code: ({ inline, ...props }) =>
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
              ul: ({ ...props }) => (
                <ul className="list-disc ml-6 mb-2" {...props} />
              ),
              ol: ({ ...props }) => (
                <ol className="list-decimal ml-6 mb-2" {...props} />
              ),
              li: ({ ...props }) => <li className="mb-1" {...props} />,
              blockquote: ({ ...props }) => (
                <blockquote
                  className="border-l-4 border-blue-400 pl-4 italic text-blue-100 bg-blue-900/30 my-2 py-1 rounded"
                  {...props}
                />
              ),
              strong: ({ ...props }) => (
                <strong className="font-semibold" {...props} />
              ),
              em: ({ ...props }) => <em className="italic" {...props} />,
              hr: () => <hr className="my-3 border-gray-600" />,
              h1: ({ ...props }) => (
                <h1
                  className="text-xl font-bold mt-2 mb-1 text-blue-200"
                  {...props}
                />
              ),
              h2: ({ ...props }) => (
                <h2
                  className="text-lg font-semibold mt-2 mb-1 text-blue-100"
                  {...props}
                />
              ),
              h3: ({ ...props }) => (
                <h3
                  className="text-base font-semibold mt-2 mb-1 text-blue-100"
                  {...props}
                />
              ),
              table: ({ ...props }) => (
                <table
                  className="min-w-full border-collapse my-2 bg-gray-800 rounded"
                  {...props}
                />
              ),
              th: ({ ...props }) => (
                <th
                  className="border-b border-gray-600 px-2 py-1 text-left text-gray-200"
                  {...props}
                />
              ),
              td: ({ ...props }) => (
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
              <img src={imageMessage} alt="Image" className="w-full max-w-md h-auto rounded-lg" />
            </div>
          )}
          {extraData && (
            <div className="mt-2 flex flex-col lg:flex-row gap-2 w-full max-w-4xl">
              <div className="flex-1">
                <TableExtraData extraData={extraData} />
              </div>
              <div className="flex-1">
                <ChatExtraData extraData={extraData} />
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default BotMessage;