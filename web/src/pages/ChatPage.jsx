import React, { useContext } from 'react';
import ChatBox from '../components/ChatBox';
import Navbar from '../components/Navbar';
import { ChatContext } from '../context/ChatContext';

const ChatPage = () => {
  const { clearMessages } = useContext(ChatContext);
  
  return (
    <div className="flex flex-col h-screen">
      <Navbar />
      <div className="container mx-auto flex-1 overflow-hidden">
        <div className="flex justify-between items-center p-4 border-b">
          <h2 className="text-xl font-semibold">HUST Assistant</h2>
          <button
            onClick={clearMessages}
            className="px-3 py-1 bg-red-500 text-white rounded-md hover:bg-red-600 transition duration-300 text-sm"
          >
            Clear Chat
          </button>
        </div>
        <ChatBox />
      </div>
    </div>
  );
};

export default ChatPage;