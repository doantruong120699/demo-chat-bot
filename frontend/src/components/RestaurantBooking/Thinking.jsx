import { ChatBubbleLeftRightIcon } from "@heroicons/react/24/outline";

const Thinking = () => {
  return (
    <div className="flex justify-start">
      <div className="bg-white text-gray-900 max-w-xs px-4 py-3 rounded-2xl shadow-sm border border-gray-200">
        <div className="flex items-center">
          <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center mr-3 flex-shrink-0">
            <ChatBubbleLeftRightIcon className="w-4 h-4 text-white" />
          </div>
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
            <div
              className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"
              style={{ animationDelay: "0.1s" }}
            ></div>
            <div
              className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"
              style={{ animationDelay: "0.2s" }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Thinking;
