import { useState } from "react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export const useStreamingResponse = () => {
  const [loading, setLoading] = useState(false);

  const streamResponse = async ({ user_input, chat_id, chat_history, apiUrl, onProgress, onFinish, onError, onGenerateImage = null, onGenerateExtraData = null }) => {
    setLoading(true);
    try {
      const response = await fetch(apiUrl || `${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({ 
          message: user_input, 
          chat_id: chat_id,
          chat_history: chat_history || []
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      let result = "";
      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      const processText = async ({ done, value }) => {
        if (done) {
          setLoading(false);
          return;
        }

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n").filter((line) => line.trim() !== "");

        for (const line of lines) {
          const json = JSON.parse(line.slice(6));
          if (json.type === "token") {
            result += json.content;
            await onProgress?.({ type: "token", content: result });
          } else if (json.type === "html") {
            await onProgress?.({ type: "html", content: json.content });
          } else if (json.type === "end") {
            await onFinish?.({ type: "end", content: result });
          } else if (json.type === "error") {
            onError?.(json.error || 'An error occurred');
          } else if (json.type === "image") {
            await onGenerateImage?.({ type: "image", content: json.content });
          } else if (json.type === "extra_data") {
            await onGenerateExtraData?.({ type: "extra_data", content: json.content });
          }
        }

        return reader.read().then(async (result) => {
          await processText(result);
        });
      };

      reader.read().then(async (result) => {
        await processText(result);
      }).catch(async (error) => {
        console.error("Error processing stream:", error);
        onError?.(error.message || 'Failed to process stream');
        setLoading(false);
      });
    } catch (error) {
      console.error("Error calling Chat API:", error);
      onError?.(error.message || 'Failed to connect to server');
      setLoading(false);
    }
  };

  return { streamResponse, loading };
};
