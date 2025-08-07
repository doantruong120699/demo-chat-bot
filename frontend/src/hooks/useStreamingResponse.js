import { useState } from "react";

export const useStreamingResponse = () => {
  const [loading, setLoading] = useState(false);

  const streamResponse = async ({ user_input, onProgress, onFinish }) => {
    setLoading(true);
    try {
    const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
            'Accept': '*/*',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: user_input }),
    });

      let result = "";
      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      reader.read().then(function processText({ done, value }) {
        if (done) {
          onFinish?.(result);
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
                }
              } catch (parseError) {
                console.error("Error parsing JSON:", parseError);
              }
            }
          }
        });

        return reader.read().then(processText);
      });
    } catch (error) {
      console.error("Error calling Chat API:", error);
    } finally {
      setLoading(false);
    }
  };

  return { streamResponse, loading };
};
