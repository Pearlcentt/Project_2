import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import AppRoutes from './routes';
import { ChatProvider } from './context/ChatContext';
import './index.css'; // Assuming you have Tailwind CSS set up

function App() {
  return (
    <Router>
      <ChatProvider>
        <AppRoutes />
      </ChatProvider>
    </Router>
  );
}

export default App;