import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import AppRoutes from './routes';
import { ChatProvider } from './context/ChatContext';

function App() {
  return (
    <ChatProvider>
      <Router>
        <AppRoutes />
      </Router>
    </ChatProvider>
  );
}

export default App;
