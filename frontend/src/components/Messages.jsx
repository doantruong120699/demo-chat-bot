/* eslint-disable no-unused-vars */
import React, { useRef, useState, useEffect } from 'react';
import { useStreamingResponse } from '../hooks/useStreamingResponse';
import { useAuth } from '../hooks/useAuth';
import { chat } from '../api/chat.js';
import ReactMarkdown from 'react-markdown';

const HumanMessage = ({ message, userProfile }) => {
    return (
        <div className="flex justify-end">
            <div className="flex items-end w-auto bg-blue-500 dark:bg-gray-800 m-1 rounded-xl rounded-br-none sm:w-3/4 md:w-auto">
                <div className="p-2">
                    <div className="text-gray-200">
                        <ReactMarkdown>{message}</ReactMarkdown>
                    </div>
                </div>
            </div>
        </div>
    )
}

const BotMessage = ({ message, isError = false, isLoading = false }) => {
    if (isLoading) {
        return (
            <div className="flex items-end w-3/4" >
                <div className="w-8 m-3 rounded-full" />
                <div className="p-3 my-1 rounded-2xl rounded-bl-none sm:w-3/4 md:w-3/6 bg-purple-300 dark:bg-gray-800">
                    <div className="text-xs text-gray-600 dark:text-gray-200">
                        AI Assistant
                    </div>
                    <div className="text-gray-700 dark:text-gray-200">
                        <div className="flex items-center space-x-2">
                            <div className="flex space-x-1">
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                            </div>
                            <span className="text-sm text-gray-500">Đợi chút...</span>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    // Always render bot message container, even if empty (for streaming)
    return (
        <div className="flex items-end w-3/4" >
            <div className="w-8 m-3 rounded-full" />
            <div className={`p-3 my-1 rounded-2xl rounded-bl-none sm:w-3/4 md:w-3/6 ${
                isError 
                    ? 'bg-red-100 dark:bg-red-900 border border-red-200' 
                    : 'bg-purple-300 dark:bg-gray-800'
            }`}>
                <div className="text-xs text-gray-600 dark:text-gray-200">
                    AI Assistant
                </div>
                <div className={`${
                    isError 
                        ? 'text-red-700 dark:text-red-200' 
                        : 'text-gray-700 dark:text-gray-200'
                }`}>
                    <ReactMarkdown
                        children={message || (isError ? 'An error occurred' : '')}
                        skipHtml={false}
                    />
                </div>
            </div>
        </div>
    )
}

const Messages = ({ chatId }) => {
    const { currentUser } = useAuth();
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const messagesEndRef = useRef(null);
    const { streamResponse, loading } = useStreamingResponse();   

    useEffect(() => {
        const fetchChatDetail = async () => {
            if (!chatId) {
                setMessages([]);
                return;
            }
            
            try {
                const response = await chat.getChatDetail(chatId);
                console.log('Messages response', response);
                setMessages(response.data.messages || []);
            } catch (error) {
                console.error('Failed to fetch chat detail:', error);
                setMessages([]);
            }
        }
        fetchChatDetail();
    }, [chatId]);

    // Auto-scroll to bottom when new messages arrive
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Format timestamp
    const formatTime = (timestamp) => {
        return new Date(timestamp).toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    };

    const handleSendMessage = async () => {
        if (!input.trim() || loading) return;
    
        const userInput = input.trim();
        setInput('');
        
        // Add human message to the messages array
        const userMessage = {
            id: Date.now(),
            message: userInput,
            sender: 'HUMAN',
            timestamp: new Date().toISOString(),
        };
        
        setMessages(prevMessages => [...prevMessages, userMessage]);
        
        // Add placeholder for bot message
        const botMessageId = Date.now() + 1;
        const botMessage = {
            id: botMessageId,
            message: '',
            sender: 'BOT',
            timestamp: new Date().toISOString(),
        };
        
        setMessages(prevMessages => [...prevMessages, botMessage]);
        
        try {
            await streamResponse({
                user_input: userInput,
                chat_id: chatId,
                onProgress: (result) => {
                    // Update the bot message with streaming content
                    setMessages(prevMessages => 
                        prevMessages.map(msg => 
                            msg.id === botMessageId 
                                ? { ...msg, message: result }
                                : msg
                        )
                    );
                    scrollToBottom();
                },
                onFinish: (result) => {
                    // Final update to the bot message
                    setMessages(prevMessages => 
                        prevMessages.map(msg => 
                            msg.id === botMessageId 
                                ? { ...msg, message: result }
                                : msg
                        )
                    );
                    scrollToBottom();
                },
                onError: (error) => {
                    console.error('Streaming error:', error);
                    // Handle error by updating the bot message
                    setMessages(prevMessages => 
                        prevMessages.map(msg => 
                            msg.id === botMessageId 
                                ? { 
                                    ...msg, 
                                    message: 'Sorry, I encountered an error. Please try again.',
                                    isError: true 
                                }
                                : msg
                        )
                    );
                }
            });
        } catch (error) {
            console.error('Failed to stream response:', error);
            // Handle error by updating the bot message
            setMessages(prevMessages => 
                prevMessages.map(msg => 
                    msg.id === botMessageId 
                        ? { 
                            ...msg, 
                            message: 'Sorry, I encountered an error. Please try again.',
                            isError: true 
                        }
                        : msg
                )
            );
        }
    };

    return (
        <div className="flex-grow h-full flex flex-col">
            {/* Messages Container */}
            <div className="w-full flex-grow my-2 p-2 overflow-y-auto mb-[76px] mt-[73px]">
                {messages.length === 0 ? (
                    <div className="text-center py-12">
                        <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                            <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                            </svg>
                        </div>
                        <h3 className="text-lg font-medium text-gray-900 mb-2">
                            Start a conversation
                        </h3>
                        <p className="text-gray-500">
                            Ask me anything! I'm here to help.
                        </p>
                    </div>
                ) : (
                    messages.map((message) => {                        
                        // Handle different possible sender field names
                        const messageContent = message.message || message.content || '';
                        
                        if (message.sender === 'HUMAN') {
                            return (
                                <div key={message.id || `human-${Date.now()}`}>
                                    <HumanMessage message={messageContent} userProfile={currentUser} />
                                    <div className="text-xs text-gray-500 text-right mr-2 mb-2">
                                        {formatTime(message.created_at || Date.now())}
                                    </div>
                                </div>
                            );
                        } else if (message.sender === 'BOT') {
                            return (
                                <div key={message.id || `bot-${Date.now()}`}>
                                    <BotMessage 
                                        message={messageContent} 
                                        isError={message.isError} 
                                        isLoading={!messageContent && !message.isError && loading}
                                    />
                                    {messageContent && (
                                        <div className="text-xs text-gray-500 ml-14 mb-2">
                                            {formatTime(message.created_at || Date.now())}
                                        </div>
                                    )}
                                </div>
                            );
                        }
                        console.log('Unknown message.sender:', message.sender);
                        return null; // Handle any unexpected sender values
                    })
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input Form */}
            <div className="rounded-xl rounded-tr-none rounded-tl-none bg-gray-100 dark:bg-gray-800 fixed bottom-0 main-content">
                <div className="flex items-center">
                    <div className="p-2 text-gray-600 dark:text-gray-200">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                    <div className="search-chat flex flex-grow p-2">
                        <input 
                            className="input text-gray-700 dark:text-gray-200 text-sm p-5 focus:outline-none bg-gray-100 dark:bg-gray-800 flex-grow rounded-l-md" 
                            type="text" 
                            placeholder="Type your message..." 
                            value={input} 
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter' && !e.shiftKey && input.trim() && !loading) {
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
                            {loading ? (
                                <svg className="w-6 h-6 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                            ) : (
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 transform rotate-90" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                                </svg>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Messages;