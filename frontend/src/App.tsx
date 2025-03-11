import { useState, useEffect } from "react";
import "./VictorianTheme.css";

interface Message {
  text: string;
  sender: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [currentMessage, setCurrentMessage] = useState("");
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isTyping, setIsTyping] = useState(false);

  useEffect(() => {
    async function initializeConversation() {
      const response = await fetch("https://sherlockbot.onrender.com/start");
      const data = await response.json();
      setConversationId(data.conversation_id);
    }
    initializeConversation(); 
  }, []);

  const sendMessage = async () => {
    if (input.trim() === "") return;

    const userMessage: Message = { text: input, sender: "You" };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsTyping(true);

    try {
      const response = await fetch("https://sherlockbot.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: input, conversation_id: conversationId }),
      });
      
      const data = await response.json();
      if (data.status === "success") {
        setConversationId(data.conversation_id);
        renderWordByWord(data.message, "Sherlock");
      }
    } catch (error) {
      console.error("Error fetching chatbot response:", error);
    }
  };

  const renderWordByWord = (message: string, sender: string) => {
    let words = message.split(" ");
    let index = 0;
    let tempMessage = "";  // Temporary variable to hold the accumulating message
    setCurrentMessage("");
  
    const interval = setInterval(() => {
      if (index < words.length) {
        tempMessage += words[index] + " ";
        setCurrentMessage(tempMessage);
        index++;
      } else {
        clearInterval(interval);
        setMessages((prev) => [...prev, { text: tempMessage.trim(), sender }]);  // Ensure full message is saved
        setCurrentMessage("");
        setIsTyping(false);
      }
    }, 100);
  };
  

  const resetChat = async () => {
    if (!conversationId) return;
    try {
      await fetch("https://sherlockbot.onrender.com/reset", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ conversation_id: conversationId }),
      });
      setMessages([]);
      setConversationId(null);
    } catch (error) {
      console.error("Error resetting chat:", error);
    }
  };

  return (
    <div className="victorian-container">
      <h1 className="victorian-title">🕵️ <span>Sherlock Chatbot</span></h1>
      <div className="victorian-chatbox">
        {messages.map((msg, index) => (
          <div key={index} className={`victorian-message ${msg.sender === "You" ? "text-right" : "text-left"} fade-in`}>
            <strong className="victorian-message-strong">{msg.sender}:</strong> {msg.text}
          </div>
        ))}
        {isTyping && <div className="victorian-message text-left fade-in">Sherlock: {currentMessage}</div>}
      </div>
      <div className="victorian-input-container">
        <input
          type="text"
          className="victorian-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask Sherlock..."
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
      </div>
      <div className="victorian-button-container">
        <button className="victorian-button" onClick={sendMessage}>Send</button>
        <button className="victorian-button victorian-reset-button" onClick={resetChat}>Reset Chat</button>
      </div>
    </div>
  );
}

export default App;
