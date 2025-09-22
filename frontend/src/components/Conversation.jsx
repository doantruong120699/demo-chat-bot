import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import ConversationItem from './ConversationItem';
import { chat } from '../api/chat.js';

const Conversation = ({ selectedChatId, onChatSelect, refreshTrigger }) => {
    const navigate = useNavigate();
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchChatHistoryList = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await chat.getHistory();
            console.log('Chat history response:', response);
            
            // Handle different response structures
            if (response.data?.data?.items) {
                setData(response.data.data.items);
            } else if (response.data?.results) {
                setData(response.data.results);
            } else if (Array.isArray(response.data)) {
                setData(response.data);
            } else {
                console.warn('Unexpected response structure:', response.data);
                setData([]);
            }
        } catch (error) {
            console.error('Failed to fetch chat history:', error);
            setError('Failed to load conversations');
            setData([]);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        fetchChatHistoryList();
    }, [refreshTrigger]); // Re-fetch when refreshTrigger changes

    const handleChatSelect = (chatId) => {
        console.log('chatId', chatId);
        if (chatId) {
            // Update URL with chat ID without page reload
            navigate(`/chat/${chatId}`, { replace: true });
            
            // Call parent callback to update chat state
            if (onChatSelect) {
                onChatSelect(chatId);
            }
        }
    }

    if (loading) {
        return (
            <div className="p-1">
                <div className="flex items-center justify-center py-4">
                    <svg className="animate-spin h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span className="ml-2 text-sm text-gray-500">Loading conversations...</span>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="p-1">
                <div className="text-center py-4">
                    <p className="text-sm text-red-600">{error}</p>
                    <button 
                        onClick={fetchChatHistoryList}
                        className="mt-2 text-sm text-blue-600 hover:text-blue-800"
                    >
                        Try again
                    </button>
                </div>
            </div>
        );
    }

    if (!data || data.length === 0) {
        return (
            <div className="p-1">
                <div className="text-center py-4">
                    <p className="text-sm text-gray-500">No conversations yet</p>
                    <p className="text-xs text-gray-400 mt-1">Start a new chat to begin</p>
                </div>
            </div>
        );
    }

    return (
        <div className="p-1">
            {data.map((item, index) => (
                <ConversationItem 
                    key={item.id || index}
                    id={item.id}
                    created_at={item.created_at}
                    title={item.title || item.message || `Chat ${item.id}`}
                    active={selectedChatId === item.id}
                    onClick={() => handleChatSelect(item.id)}
                />
            ))}
        </div>
    )
}

export default Conversation