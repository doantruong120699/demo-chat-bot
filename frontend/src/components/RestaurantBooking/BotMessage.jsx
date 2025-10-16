import { ChatBubbleLeftRightIcon } from "@heroicons/react/24/outline";
import React from 'react';
import ReactMarkdown from 'react-markdown';

const BotMessage = ({ message, index }) => {
  return (
    <div
      className={`flex justify-start animate-fadeIn`}
      style={{ animationDelay: `${index * 0.1}s` }}
    >
      <div className="max-w-full px-3 py-3 rounded-2xl shadow-sm transition-all duration-300 hover:scale-105 bg-white text-gray-900 border border-gray-200">
        <div className="flex items-start">
          <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center mr-3 mt-1 flex-shrink-0">
            <ChatBubbleLeftRightIcon className="w-4 h-4 text-white" />
          </div>
          <div className="flex-1">
            {/* <p className="text-sm leading-relaxed whitespace-pre-wrap"> */}
            <ReactMarkdown
            children={
              message.content
            }
            skipHtml={false}
            components={{
              p: ({ ...props }) => (
                <p className="mb-2 text-sm leading-relaxed" {...props} />
              ),
              a: ({ ...props }) => (
                <a
                  className="text-blue-500 text-sm underline hover:text-blue-800 transition-colors"
                  target="_blank"
                  rel="noopener noreferrer"
                  {...props}
                />
              ),
              code: ({ inline, ...props }) =>
                inline ? (
                  <code
                    className="bg-gray-700 rounded px-1 py-0.5 text-purple-200 text-sm"
                    {...props}
                  />
                ) : (
                  <pre className="bg-gray-900 rounded-lg p-3 overflow-x-auto my-2 text-sm">
                    <code {...props} />
                  </pre>
                ),
              ul: ({ ...props }) => (
                <ul className="list-disc ml-6 mb-2 text-sm" {...props} />
              ),
              ol: ({ ...props }) => (
                <ol className="list-decimal ml-6 mb-2 text-sm" {...props} />
              ),
              li: ({ ...props }) => <li className="mb-1 text-sm" {...props} />,
              blockquote: ({ ...props }) => (
                <blockquote
                  className="text-sm border-l-4 border-blue-400 pl-4 italic text-blue-100 bg-blue-900/30 my-2 py-1 rounded"
                  {...props}
                />
              ),
              strong: ({ ...props }) => (
                <strong className="font-semibold text-sm" {...props} />
              ),
              em: ({ ...props }) => <em className="italic text-sm" {...props} />,
              hr: () => <hr className="my-3 border-gray-600 text-sm" />,
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
            {/* </p> */}
            <p className="text-[10px] text-gray-500">
              {message.timestamp.toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              })}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BotMessage;
