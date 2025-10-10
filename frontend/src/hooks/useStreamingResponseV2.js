import { useState } from "react";

export async function* streamChatOutput({ reader }) {
  const decoder = new TextDecoder('utf-8');
  let line = '';

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        reader.releaseLock();
        break;
      }

      const tokenLines = decoder.decode(value, { stream: true });
      const tokens = tokenLines.split('\n');

      for (const token of tokens) {
        if (!token.trim()) {
          continue;
        }

        // Handle Server-Sent Events format
        if (token.startsWith('data: ')) {
          const jsonData = token.slice(6); // Remove "data: " prefix
          if (jsonData.trim()) {
            try {
              const result = JSON.parse(jsonData);
              yield result;
            } catch (error) {
              if (error instanceof SyntaxError) {
                console.warn('Failed to parse SSE data:', jsonData);
                continue;
              }
              throw error;
            }
          }
        } else {
          // Handle regular JSON streaming
          line += token;
          try {
            const result = JSON.parse(line);
            line = '';
            yield result;
          } catch (error) {
            if (error instanceof SyntaxError) {
              continue;
            }
            throw error;
          }
        }
      }
    }
  } catch (error) {
    console.error('[Stream Error]:', error);
    throw error;
  } finally {
    reader.releaseLock();
  }
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export const useStreamingResponseV2 = () => {
  const [loading, setLoading] = useState(false);
  const [thinking, setThinking] = useState(false);

  /**
   * 
   * @param {{
   *   user_input: string,
   *   chat_history?: array,
   *   onProgress?: function,
   *   onFinish?: function,
   *   onError?: function
   * }} params 
   */
  const streamResponse = async ({
    user_input,
    chat_history = [],
    onProgress,
    onFinish,
    onError
  }) => {
    setLoading(true);
    setThinking(true);
    try {
      // NOTE: Update this endpoint to your actual SSE endpoint!
      const response = await fetch(
        `${API_BASE_URL}/restaurant-booking/chat/stream/`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            // No auth assumed for restaurant-booking chat API, adjust if needed
          },
          body: JSON.stringify({
            user_input,
            chat_history
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      let accumulatedText = "";

      try {
        for await (const streamEvent of streamChatOutput({ reader })) {
          if (streamEvent.type === "start") {
            // setThinking(false);
          } else if (streamEvent.type === "token") {
            if (accumulatedText.length > 0) setThinking(false);
            accumulatedText += streamEvent.content || '';
            await onProgress?.({ type: "token", content: accumulatedText });
          } else if (streamEvent.type === "html") {
            await onProgress?.({ type: "html", content: streamEvent.content });
          } else if (streamEvent.type === "end") {
            await onFinish?.({ type: "end", content: accumulatedText });
          } else if (streamEvent.type === "error") {
            setThinking(false);
            await onError?.(streamEvent.error || 'An error occurred');
          }
          // Add any other type handling as required.
        }
      } catch (streamErr) {
        console.error("[Stream Iterate Error]:", streamErr);
        onError?.(streamErr.message || 'Failed to process stream');
      } finally {
        setLoading(false);
      }
    } catch (error) {
      console.error("Error calling Chat API:", error);
      onError?.(error.message || 'Failed to connect to server');
      setLoading(false);
      setThinking(false);
    }
  };

  return { streamResponse, loading, thinking };
};
