import { UserIcon } from "@heroicons/react/24/outline";

const UserMessage = ({ message, index }) => {
  return (
    <div
      className={`flex justify-end animate-fadeIn`}
      style={{ animationDelay: `${index * 0.1}s` }}
    >
      <div className="max-w-xs lg:max-w-md px-3 py-3 rounded-2xl shadow-sm transition-all duration-300 hover:scale-105 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="flex items-start">
          <div className="flex-1">
            <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
            <p className="text-[10px] text-blue-100">
              {message.timestamp.toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              })}
            </p>
          </div>
          <div className="w-8 h-8 rounded-full border bg-white flex items-center justify-center ml-3 flex-shrink-0">
            <UserIcon className="w-4 h-4 text-blue-600" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserMessage;
