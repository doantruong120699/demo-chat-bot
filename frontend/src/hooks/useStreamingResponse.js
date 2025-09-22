import { useState } from "react";

export const useStreamingResponse = () => {
  const [loading, setLoading] = useState(false);

  const streamResponse = async ({ user_input, chat_id, onProgress, onFinish, onError }) => {
    setLoading(true);
    try {
      // Use fetch for streaming response since axios doesn't support streaming
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({ 
          message: user_input, 
          chat_id: chat_id 
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      let result = "";
      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      const processText = ({ done, value }) => {
        if (done) {
          onFinish?.(result);
          setLoading(false);
          return;
        }

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n").filter((line) => line.trim() !== "");

        lines.forEach((line) => {
          if (line.startsWith("data: ")) {
            const jsonString = line.slice(6);
            if (jsonString.trim() !== "[DONE]") {
              try {
                const json = JSON.parse(jsonString);
                // Handle new response format with token and type fields
                if (json.type === "token" && json.content) {
                  result += json.content;
                  onProgress?.(result);
                } else if (json.type === "end") {
                  // End of stream
                  onFinish?.(result);
                } else if (json.type === "error") {
                  // Handle error from stream
                  onError?.(json.error || 'An error occurred');
                }
              } catch (parseError) {
                console.error("Error parsing JSON:", parseError);
              }
            }
          }
        });

        return reader.read().then(processText);
      };

      reader.read().then(processText);
    } catch (error) {
      console.error("Error calling Chat API:", error);
      onError?.(error.message || 'Failed to connect to server');
      setLoading(false);
    }
  };

  return { streamResponse, loading };
};
