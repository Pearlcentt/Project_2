import React, { createContext, useState } from 'react';

export const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);
  const [retrievedDocs, setRetrievedDocs] = useState([]);
  
  const addMessage = (message) => {
    setMessages(prevMessages => [...prevMessages, message]);
  };
  
  const clearMessages = () => {
    setMessages([]);
    setRetrievedDocs([]);
  };
  
  return (
    <ChatContext.Provider value={{
      messages,
      retrievedDocs,
      setRetrievedDocs,
      addMessage,
      clearMessages
    }}>
      {children}
    </ChatContext.Provider>
  );
};