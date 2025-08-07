/* eslint-disable no-unused-vars */
import React, { useRef, useState } from 'react'
import { useStreamingResponse } from '../hooks/useStreamingResponse'

const HumanMessage = ({ message }) => {
    return (
        <div className="flex justify-end">
            <div className="flex items-end w-auto bg-purple-500 dark:bg-gray-800 m-1 rounded-xl rounded-br-none sm:w-3/4 md:w-auto">
                <div className="p-2">
                    <div className="text-gray-200">
                        {message}
                    </div>
                </div>
            </div>
        </div>
    )
}

const BotMessage = ({ message }) => {
    return (
        <div className="flex items-end w-3/4" >
            <div className="w-8 m-3 rounded-full" />
            <div className="p-3 bg-purple-300 dark:bg-gray-800 mx-3 my-1 rounded-2xl rounded-bl-none sm:w-3/4 md:w-3/6">
                <div className="text-xs text-gray-600 dark:text-gray-200">
                    Bot
                </div>
                <div className="text-gray-700 dark:text-gray-200 whitespace-pre-wrap">
                    {message}
                </div>
            </div>
        </div>
    )
}

const Messages = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const refineInputRef = useRef(null);
    const { streamResponse, loading } = useStreamingResponse();

    const scrollToBottom = () => {
        if (refineInputRef.current) {
          refineInputRef.current.scrollIntoView({ behavior: "smooth" });
        }
      };

    // const handleSendMessage = async () => {
    //     if (!input.trim()) return;
        
    //     const userInput = input.trim();
    //     setIsLoading(true);
    //     setHumanMessage(userInput);
    //     setBotReply('');
        
    //     try {
    //         const response = await fetch('http://localhost:8000/api/chat', {
    //             method: 'POST',
    //             headers: {
    //                 'Accept': '*/*',
    //                 'Content-Type': 'application/json',
    //             },
    //             body: JSON.stringify({ message: userInput }),
    //         });

    //         if (!response.ok) {
    //             throw new Error(`HTTP error! status: ${response.status}`);
    //         }

    //         if (!response.body) {
    //             throw new Error('No response body');
    //         }

    //         const reader = response.body.getReader();
    //         let botMessage = '';
    //         let textEffectTimeout = null;

    //         function updateTypingEffect(fullText) {
    //             let i = 0;
    //             function typeNext() {
    //                 setBotReply(fullText.slice(0, i));
    //                 i++;
    //                 if (i <= fullText.length) {
    //                     textEffectTimeout = setTimeout(typeNext, 12);
    //                 }
    //             }
    //             typeNext();
    //         }

    //         function read() {
    //             reader.read().then(({ done, value }) => {
    //                 if (done) {
    //                     if (botMessage.trim() !== '') {
    //                         performTypewriterEffect(botMessage, () => {
    //                             setMessages(prevMessages => [...prevMessages, { type: 'bot', message: botMessage }]);
    //                             setIsLoading(false);
    //                             setHumanMessage('');
    //                             setBotReply('');
    //                         });
    //                     } else {
    //                         setIsLoading(false);
    //                         setHumanMessage('');
    //                         setBotReply('');
    //                     }
    //                     return;
    //                 }

    //                 try {
    //                     const chunk = new TextDecoder().decode(value);
    //                     const events = chunk.split('\n\n').filter(event => event.trim());
                        
    //                     events.forEach(eventStr => {
    //                         if (eventStr.startsWith('data:')) {
    //                             try {
    //                                 const data = JSON.parse(eventStr.replace('data: ', '').replace('data:', ''));
    //                                 handleStreamEvent(data);
    //                             } catch (parseError) {
    //                                 console.warn('Failed to parse SSE data:', parseError);
    //                             }
    //                         }
    //                     });
                        
    //                     read();
    //                 } catch (decodeError) {
    //                     console.error('Failed to decode stream chunk:', decodeError);
    //                     setBotReply('Error processing server response.');
    //                     setIsLoading(false);
    //                     setHumanMessage('');
    //                 }
    //             }).catch((readError) => {
    //                 console.error('Error reading stream:', readError);
    //                 setBotReply('Error reading server response.');
    //                 setIsLoading(false);
    //                 setHumanMessage('');
    //             });
    //         }

    //         function handleStreamEvent(data) {
    //             switch (data.type) {
    //                 case 'token':
    //                     if (data.token) {
    //                         botMessage += data.token;
    //                         if (textEffectTimeout) {
    //                             clearTimeout(textEffectTimeout);
    //                         }
    //                         updateTypingEffect(botMessage);
    //                     }
    //                     break;
    //                 case 'end':
    //                     setBotReply(botMessage);
    //                     break;
    //                 case 'error':
    //                     if (data.error) {
    //                         setBotReply(`Error: ${data.error}`);
    //                         setIsLoading(false);
    //                         setHumanMessage('');
    //                     }
    //                     break;
    //                 default:
    //                     console.warn('Unknown event type:', data.type);
    //             }
    //         }

    //         function performTypewriterEffect(fullText, onComplete) {
    //             let i = 0;
    //             const typeSpeed = 12;
                
    //             function typeNext() {
    //                 setBotReply(fullText.slice(0, i));
    //                 i++;
                    
    //                 if (i <= fullText.length) {
    //                     textEffectTimeout = setTimeout(typeNext, typeSpeed);
    //                 } else if (onComplete) {
    //                     onComplete();
    //                 }
    //             }
                
    //             typeNext();
    //         }

    //         setMessages(prevMessages => [...prevMessages, { type: 'human', message: userInput }]);
            
    //         read();
            
    //         setInput('');
    //     } catch (err) {
    //         console.error('Error in handleSendMessage:', err);
    //         setBotReply('Error connecting to server.');
    //         setIsLoading(false);
    //     }
    // }

    const handleSendMessage = async () => {
        if (!input.trim()) return;
    
        const userInput = input.trim();
        setInput('');
        
        // Add human message to the messages array
        setMessages(prevMessages => [...prevMessages, { type: 'human', message: userInput }]);
        
        await streamResponse({
            user_input: userInput,
            onProgress: (result) => {
                // Update the last bot message or create a new one
                setMessages(prevMessages => {
                    const newMessages = [...prevMessages];
                    const lastMessage = newMessages[newMessages.length - 1];
                    
                    if (lastMessage && lastMessage.type === 'bot') {
                        // Update existing bot message
                        lastMessage.message = result;
                        return newMessages;
                    } else {
                        // Create new bot message
                        return [...newMessages, { type: 'bot', message: result }];
                    }
                });
                scrollToBottom();
            },
            onFinish: async (result) => {
            },
        });
      };
    
    return (
        <div className="flex-grow h-full flex flex-col">
            <div className="w-full h-15 p-1 bg-purple-600 dark:bg-gray-800 shadow-md rounded-xl rounded-bl-none rounded-br-none">
                <div className="flex p-2 align-middle items-center">
                    <div className="p-2 md:hidden rounded-full mr-1 hover:bg-purple-500 text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                        </svg>
                    </div>
                    <div className="border rounded-full border-white p-1/2">
                        <img className="w-14 h-14 rounded-full" src="https://cdn.pixabay.com/photo/2017/01/31/21/23/avatar-2027366_960_720.png" alt="avatar" />
                    </div>
                    <div className="flex-grow p-2">
                        <div className="text-md text-gray-50 font-semibold">Rey Jhon A. Baquirin </div>
                        <div className="flex items-center">
                            <div className="w-2 h-2 bg-green-300 rounded-full"></div>
                            <div className="text-xs text-gray-50 ml-1">
                                Online
                            </div>
                        </div>
                    </div>
                    <div className="p-2 text-white cursor-pointer hover:bg-purple-500 rounded-full">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                        </svg>
                    </div>
                </div>
            </div>
            <div className="w-full flex-grow bg-gray-100 dark:bg-gray-900 my-2 p-2 overflow-y-auto">
                {messages.map((message, index) => {
                    if (message.type === 'bot') {
                        return <BotMessage key={index} message={message.message} />
                    } else {
                        return <HumanMessage key={index} message={message.message} />
                    }
                })}
                {loading && (
                    <div className="flex items-end w-3/4">
                        <div className="w-8 m-3 rounded-full" />
                        <div className="p-3 bg-purple-300 dark:bg-gray-800 mx-3 my-1 rounded-2xl rounded-bl-none sm:w-3/4 md:w-3/6">
                            <div className="text-xs text-gray-600 dark:text-gray-200">
                                Bot
                            </div>
                            <div className="text-gray-700 dark:text-gray-200">
                                <div className="flex items-center space-x-2">
                                    <div className="flex space-x-1">
                                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                                    </div>
                                    <span className="text-sm text-gray-500">Thinking...</span>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

            </div>
            <div className="h-15  p-3 rounded-xl rounded-tr-none rounded-tl-none bg-gray-100 dark:bg-gray-800">
                <div className="flex items-center">
                    <div className="p-2 text-gray-600 dark:text-gray-200 ">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                    <div className="search-chat flex flex-grow p-2">
                        <input 
                            className="input text-gray-700 dark:text-gray-200 text-sm p-5 focus:outline-none bg-gray-100 dark:bg-gray-800 flex-grow rounded-l-md" 
                            type="text" 
                            placeholder="Type your message ..." 
                            value={input} 
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter' && !e.shiftKey && input.trim()) {
                                    e.preventDefault();
                                    handleSendMessage();
                                }
                            }}
                            disabled={loading}
                        />
                        <div 
                            className={`bg-gray-100 dark:bg-gray-800 dark:text-gray-200 flex justify-center items-center pr-3 rounded-r-md cursor-pointer ${
                                input.trim() && !loading ? 'text-gray-600 hover:text-gray-800' : 'text-gray-400 cursor-not-allowed'
                            }`} 
                            onClick={() => input.trim() && !loading && handleSendMessage()} 
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                            </svg>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Messages