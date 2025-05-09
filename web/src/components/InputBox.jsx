import React, { useState, useContext } from 'react';
import { ChatContext } from '../context/ChatContext';
import { fetchRelevantDocs, callGemini } from '../services/backendService';

const InputBox = () => {
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { addMessage, setRetrievedDocs } = useContext(ChatContext);
  
  const handleSend = async () => {
    if (!input.trim() || isLoading) return;
    
    const userMessage = { sender: 'user', text: input.trim() };
    addMessage(userMessage);
    setIsLoading(true);
    
    try {
      // Get auth token if available
      const token = localStorage.getItem('token');
      
      // First, fetch relevant documents from backend
      const docs = await fetchRelevantDocs(input, token);
      setRetrievedDocs(docs);
      
      // Then send the query and context to Gemini
      const prompt = `Context:\n${docs.join('\n')}\n\nQuery:\n${input}`;
      const reply = await callGemini(prompt, token);
      
      // Add Gemini's response to the chat
      addMessage({ sender: 'bot', text: reply });
    } catch (err) {
      console.error('Error processing message:', err);
      addMessage({
        sender: 'bot',
        text: 'Sorry, I encountered an error processing your request. Please try again.'
      });
    } finally {
      setIsLoading(false);
      setInput('');
    }
  };
  
  return (
    <div className="flex space-x-2">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        placeholder="Ask me anything about your documents..."
        className="flex-1 py-2 px-4 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        disabled={isLoading}
      />
      <button
        onClick={handleSend}
        disabled={isLoading}
        className="bg-blue-600 text-white py-2 px-6 rounded-md hover:bg-blue-700 transition duration-300 disabled:opacity-50 flex items-center"
      >
        {isLoading ? (
          <>
            <LoadingSpinner />
            <span className="ml-2">Processing...</span>
          </>
        ) : (
          'Send'
        )}
      </button>
    </div>
  );
};

// Loading spinner component
const LoadingSpinner = () => {
  return (
    <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
  );
};

export default InputBox;