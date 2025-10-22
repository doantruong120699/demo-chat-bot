import ReactMarkdown from "react-markdown";
const HumanMessage = ({ message }) => {
  return (
    <div className="flex justify-end">
      <div className="flex items-end w-3/4 sm:w-2/3 md:w-1/2 lg:w-auto bg-blue-500 dark:bg-gray-800 my-2 rounded-xl rounded-br-none">
        <div className="p-2 sm:p-3">
          <div className="text-gray-200 text-sm sm:text-base">
            <ReactMarkdown>{message}</ReactMarkdown>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HumanMessage;
