import React, { useState } from 'react';

interface ChatProps {
  messages: { sender: string; text: string }[];
  onSendMessage: (text: string) => void;
}

const Chat: React.FC<ChatProps> = ({ messages, onSendMessage }) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim()) {
      onSendMessage(input);
      setInput('');
    }
  };

  return (
    <div className="bg-gray-800 p-4 rounded-lg shadow-lg h-full flex flex-col">
      <h3 className="text-xl font-bold mb-4">Live Chat</h3>
      <div className="flex-grow overflow-y-auto mb-4 border-t border-b border-gray-700 p-2">
        {messages.map((msg, index) => (
          <div key={index} className="mb-2">
            <span className="font-semibold text-yellow-400">{msg.sender}: </span>
            <span>{msg.text}</span>
          </div>
        ))}
      </div>
      <div className="flex">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          className="flex-grow bg-gray-700 rounded-l p-2 focus:outline-none"
          placeholder="Say something..."
        />
        <button onClick={handleSend} className="bg-yellow-500 text-black px-4 rounded-r font-bold">
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;