import { useState } from "react";
import "./VictorianTheme.css"; // Import your custom CSS

function App() {
  const [messages, setMessages] = useState<{ text: string; sender: string }[]>([]);
  const [input, setInput] = useState("");

  // Function to send a message
  const sendMessage = () => {
    if (input.trim() === "") return;

    setMessages((prevMessages) => [
      ...prevMessages,
      { text: input, sender: "You" },
      { text: `Ah, an interesting query: "${input}"! Let me investigate...`, sender: "Sherlock" },
    ]);

    setInput(""); // Clear input after sending
  };

  // Function to reset the chat
  const resetChat = () => {
    setMessages([]); // Clears all chat messages
  };

  return (
    <div className="victorian-container">
      {/* Title */}
      <h1 className="victorian-title">
        🕵️ <span>Sherlock Chatbot</span>
      </h1>

      {/* Chatbox */}
      <div className="victorian-chatbox">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`victorian-message ${msg.sender === "You" ? "text-right" : "text-left"} fade-in`}
          >
            <strong className="victorian-message-strong">{msg.sender}:</strong> {msg.text}
          </div>
        ))}
      </div>

      {/* Input Field */}
      <div className="victorian-input-container">
        <input
          type="text"
          className="victorian-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask Sherlock..."
          onKeyDown={(e) => e.key === "Enter" && sendMessage()} // Send on Enter key
        />
      </div>

      {/* Buttons Container */}
      <div className="victorian-button-container">
        <button className="victorian-button" onClick={sendMessage}>
          Send
        </button>
        <button className="victorian-button victorian-reset-button" onClick={resetChat}>
          Reset Chat
        </button>
      </div>
    </div>
  );
}

export default App;
