import { useState } from "react";
import "./VictorianTheme.css"; // <-- Import your custom CSS

function App() {
  const [messages, setMessages] = useState<{ text: string; sender: string }[]>([]);
  const [input, setInput] = useState("");

  const sendMessage = () => {
    if (input.trim() === "") return;
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: input, sender: "You" },
      { text: `Ah, an interesting query: "${input}"! Let me investigate...`, sender: "Sherlock" },
    ]);
    setInput("");
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
            className={`victorian-message ${msg.sender === "You" ? "text-right" : "text-left"}`}
          >
            <strong className="victorian-message-strong">{msg.sender}:</strong> {msg.text}
          </div>
        ))}
      </div>

      {/* Input & Button */}
      <div className="victorian-input-container">
        <input
          type="text"
          className="victorian-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask Sherlock..."
        />
        <button className="victorian-button" onClick={sendMessage}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;
