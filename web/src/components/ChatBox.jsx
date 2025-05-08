import React, { useContext } from 'react';
import { ChatContext } from '../context/ChatContext';
import MessageBubble from './MessageBubble';
import InputBox from './InputBox';

const ChatBox = () => {
  const { messages } = useContext(ChatContext);

  return (
    <div className="chatbox-container">
      <div className="chat-messages" style={{ maxHeight: '400px', overflowY: 'auto' }}>
        {messages.map((msg, index) => (
          <MessageBubble key={index} sender={msg.sender} text={msg.text} />
        ))}
      </div>
      <InputBox />
    </div>
  );
};

export default ChatBox;
