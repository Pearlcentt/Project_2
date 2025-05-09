import React from 'react';

const MessageBubble = ({ sender, text }) => {
  const isUser = sender === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-3/4 p-3 rounded-lg ${
          isUser
            ? 'bg-blue-600 text-white rounded-br-none'
            : 'bg-gray-200 text-gray-800 rounded-bl-none'
        }`}
      >
        <p className="text-sm font-bold mb-1">{isUser ? 'You' : 'HUST Assistant'}</p>
        <p className="whitespace-pre-wrap">{text}</p>
      </div>
    </div>
  );
};

export default MessageBubble;