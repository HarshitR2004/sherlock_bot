import { useState } from "react";

function App() {
  const [messages, setMessages] = useState<{ text: string; sender: string }[]>([]);
  const [input, setInput] = useState("");

  const sendMessage = () => {
    if (input.trim() === "") return;
    setMessages([...messages, { text: input, sender: "You" }, { text: `Ah, an interesting query: "${input}"! Let me investigate...`, sender: "Sherlock" }]);
    setInput("");
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-900 text-white">
      <h1 className="text-3xl font-bold mb-4">🕵️ Sherlock Chatbot</h1>
      <div className="w-full max-w-md bg-gray-800 p-4 rounded-lg h-80 overflow-y-auto">
        {messages.map((msg, index) => (
          <div key={index} className={`p-2 my-1 ${msg.sender === "You" ? "text-right" : "text-left"}`}>
            <strong>{msg.sender}: </strong>{msg.text}
          </div>
        ))}
      </div>
      <div className="mt-4 flex w-full max-w-md">
        <input
          type="text"
          className="flex-1 p-2 rounded-l bg-gray-700"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask Sherlock..."
        />
        <button onClick={sendMessage} className="bg-blue-500 px-4 py-2 rounded-r">Send</button>
      </div>
    </div>
  );
}

export default App;
