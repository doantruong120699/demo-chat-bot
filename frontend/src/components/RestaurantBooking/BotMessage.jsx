import { ChatBubbleLeftRightIcon } from "@heroicons/react/24/outline";

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
            <p className="text-sm leading-relaxed whitespace-pre-wrap">
              {message.content}
            </p>
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
