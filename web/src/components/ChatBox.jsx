import React, { useContext, useRef, useEffect, useState } from 'react';
import { ChatContext } from '../context/ChatContext';
import MessageBubble from './MessageBubble';
import InputBox from './InputBox';
import DocumentPanel from './DocumentPanel';

const ChatBox = () => {
  const { messages } = useContext(ChatContext);
  const messagesEndRef = useRef(null);
  const [showDocs, setShowDocs] = useState(false);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  return (
    <div className="flex h-full">
      <div className={`flex-1 flex flex-col h-full ${showDocs ? 'w-2/3' : 'w-full'}`}>
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <EmptyState />
          ) : (
            messages.map((msg, index) => (
              <MessageBubble key={index} sender={msg.sender} text={msg.text} />
            ))
          )}
          <div ref={messagesEndRef} />
        </div>
        <div className="p-4 border-t bg-white">
          <div className="flex justify-end mb-3">
            <button
              onClick={() => setShowDocs(!showDocs)}
              className="px-3 py-1 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition duration-300 text-sm"
            >
              {showDocs ? 'Hide Sources' : 'Show Sources'}
            </button>
          </div>
          <InputBox />
        </div>
      </div>
      
      {showDocs && <DocumentPanel />}
    </div>
  );
};

const EmptyState = () => {
  return (
    <div className="flex flex-col items-center justify-center h-64 text-center p-6">
      <div className="bg-blue-100 p-5 rounded-full mb-4">
        <svg className="w-10 h-10 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
        </svg>
      </div>
      <h3 className="text-xl font-semibold mb-2">Welcome to HUST Assistant</h3>
      <p className="text-gray-600 mb-4 max-w-md">
        Ask questions about your documents and I'll help you find answers using relevant information from HUST knowledge base.
      </p>
    </div>
  );
};

export default ChatBox;