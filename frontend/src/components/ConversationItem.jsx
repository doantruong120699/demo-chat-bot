import React, { useState, useEffect, useRef } from 'react'

const ConversationItem = ({active, created_at, title, onClick, onDelete}) => {
    const [showMenu, setShowMenu] = useState(false);
    const [showConfirm, setShowConfirm] = useState(false);
    const menuRef = useRef(null);
    
    const _class = active ? 'bg-blue-100 border-blue-300' : 'bg-white hover:bg-gray-50';
    
    // Handle click outside to close menu
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (menuRef.current && !menuRef.current.contains(event.target)) {
                setShowMenu(false);
            }
        };

        if (showMenu) {
            document.addEventListener('mousedown', handleClickOutside);
        }

        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [showMenu]);

    const formatDate = (date) => {
        return new Date(date).toLocaleString('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    }

    const handleDelete = (e) => {
        e.stopPropagation();
        setShowConfirm(true);
        setShowMenu(false);
    }

    const confirmDelete = (e) => {
        e.stopPropagation();
        if (onDelete) {
            onDelete();
        }
        setShowConfirm(false);
    }

    const cancelDelete = (e) => {
        e.stopPropagation();
        setShowConfirm(false);
    }

    return (
        <div>
            <div 
                className={`conversation-item p-1 border hover:bg-gray-50 m-1 rounded-md cursor-pointer transition-colors ${_class}`}
                onClick={onClick}
            >
                <div className="flex items-center p-2">
                    {/* <div className="w-7 h-7 m-1">
                        <img className="rounded-full" src="https://cdn.pixabay.com/photo/2017/01/31/21/23/avatar-2027366_960_720.png" alt="avatar"/>
                    </div> */}
                    <div className="flex-grow">
                        <div className="flex justify-between text-md">
                            <div className="flex flex-col gap-1">
                                <div className="text-sm font-medium text-gray-700 dark:text-gray-200">{title}</div>
                                <div className="flex items-center">
                                    <div className="text-[11px] text-gray-400 dark:text-gray-300 mr-2">{formatDate(created_at)}</div>
                                </div>
                            </div>
                            <div className="relative" ref={menuRef}>
                                    <button
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            setShowMenu(!showMenu);
                                        }}
                                        className="p-1 hover:bg-gray-200 rounded-full transition-colors"
                                    >
                                        <svg className="w-4 h-4 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                                            <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                                        </svg>
                                    </button>
                                    
                                    {showMenu && (
                                        <div className="absolute right-0 top-8 bg-white border border-gray-200 rounded-md shadow-lg z-10 min-w-[120px]">
                                            <button
                                                onClick={handleDelete}
                                                className="w-full px-3 py-2 text-left text-sm text-red-600 hover:bg-red-50 rounded-md"
                                            >
                                                Delete
                                            </button>
                                        </div>
                                    )}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            {/* Confirmation Dialog */}
            {showConfirm && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-lg p-6 max-w-sm w-full mx-4">
                        <h3 className="text-lg font-medium text-gray-900 mb-2">Delete Conversation</h3>
                        <p className="text-sm text-gray-500 mb-4">
                            Are you sure you want to delete this conversation? This action cannot be undone.
                        </p>
                        <div className="flex justify-end space-x-3">
                            <button
                                onClick={cancelDelete}
                                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={confirmDelete}
                                className="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-md transition-colors"
                            >
                                Delete
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}

export default ConversationItem