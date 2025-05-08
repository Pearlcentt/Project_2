import React from 'react';

const MessageBubble = ({ sender, text }) => {
  const isUser = sender === 'user';
  return (
    <div
      style={{
        textAlign: isUser ? 'right' : 'left',
        margin: '8px 0',
        padding: '8px',
        backgroundColor: isUser ? '#dcf8c6' : '#f1f0f0',
        borderRadius: '8px',
        maxWidth: '70%',
        alignSelf: isUser ? 'flex-end' : 'flex-start'
      }}
    >
      <strong>{isUser ? 'You' : 'AI'}:</strong> {text}
    </div>
  );
};

export default MessageBubble;
