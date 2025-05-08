import React, { useState, useContext } from 'react';
import { ChatContext } from '../context/ChatContext';
import { fetchRelevantDocs } from '../services/backendService';
import { callGemini } from '../services/geminiService';

const InputBox = () => {
  const [input, setInput] = useState('');
  const { addMessage } = useContext(ChatContext);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMessage = { sender: 'user', text: input };
    addMessage(userMessage);

    try {
      const token = localStorage.getItem('token');
      const docs = await fetchRelevantDocs(input, token);
      const prompt = `Context:\n${docs.join('\n')}\n\nQuery:\n${input}`;
      const reply = await callGemini(prompt, token);

      addMessage({ sender: 'bot', text: reply });
    } catch (err) {
      addMessage({ sender: 'bot', text: 'Error processing your request.' });
    }

    setInput('');
  };

  return (
    <div style={{ display: 'flex', gap: '8px', marginTop: '10px' }}>
      <input
        type="text"
        placeholder="Ask something..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        style={{ flexGrow: 1 }}
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
};

export default InputBox;
