import ReactMarkdown from "react-markdown";
const HumanMessage = ({ message }) => {
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

export default HumanMessage;
