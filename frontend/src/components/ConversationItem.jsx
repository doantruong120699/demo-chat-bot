import React from 'react'

const ConversationItem = ({active, created_at, title, onClick}) => {
    const _class = active ? 'bg-blue-100 border-blue-300' : 'bg-white hover:bg-gray-50';
    const formatDate = (date) => {
        return new Date(date).toLocaleString('vi-VN', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    }
    return (
        <div>
            <div 
                className={`conversation-item p-1 border hover:bg-gray-50 m-1 rounded-md cursor-pointer transition-colors ${_class}`}
                onClick={onClick}
            >
                <div className="flex items-center p-2">
                    <div className="w-7 h-7 m-1">
                        <img className="rounded-full" src="https://cdn.pixabay.com/photo/2017/01/31/21/23/avatar-2027366_960_720.png" alt="avatar"/>
                    </div>
                    <div className="flex-grow p-2">
                        <div className="flex justify-between text-md ">
                            <div className="text-sm font-medium text-gray-700 dark:text-gray-200">{title}</div>
                            <div className="text-xs text-gray-400 dark:text-gray-300">{formatDate(created_at)}</div>
                        </div>
                        {/* <div className="text-sm text-gray-500 dark:text-gray-400  w-40 truncate">
                        {message}
                        </div> */}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ConversationItem