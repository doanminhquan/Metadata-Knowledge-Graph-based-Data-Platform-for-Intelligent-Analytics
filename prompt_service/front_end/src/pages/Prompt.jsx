import { useState } from "react";
import ChatPromptInput from "@/components/textarea.jsx";
import Navbar from "@/components/Navbar.jsx";
import logo from "../assets/Logo_HUET.png";

export default function PromptToDashboard() {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async () => {
    if (!prompt.trim() || isTyping) return;

    const newMessages = [...messages, { role: "user", content: prompt }];
    setMessages(newMessages);
    setPrompt("");
    setIsTyping(true);
    setErrorMessage("");

    try {
      const response = await fetch("http://127.0.0.1:5000/fetch-url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ body: prompt }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Something went wrong");
      }

      const data = await response.json();
      const content = data.content || "";

      let i = 0;
      let currentBotMsg = "";

      const typeOut = () => {
        if (i < content.length) {
          currentBotMsg += content.charAt(i);
          i++;
          setMessages([...newMessages, { role: "bot", content: currentBotMsg }]);
          setTimeout(typeOut, 20);
        } else {
          setIsTyping(false);
        }
      };

      typeOut();
    } catch (error) {
      console.error("Error sending prompt:", error.message);
      setErrorMessage(error.message);
      setIsTyping(false);
    }
  };

  return (
    <>
      <Navbar />
      <div className="max-w-3xl mx-auto py-10 px-6 space-y-6 text-gray-800">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-2xl font-semibold text-blue-800">🎓 UET Insight Assistant</h1>
          <img src={logo} alt="UET logo" className="h-20" />
        </div>

        {/* New chat button */}
        <div className="flex justify-end">
          <button
            onClick={() => {
              if (confirm("Bạn có chắc chắn muốn bắt đầu đoạn chat mới không?")) {
                setMessages([]);
                setPrompt("");
                setErrorMessage("");
              }
            }}
            className="text-sm text-blue-600 hover:underline"
          >
            ➕ Bắt đầu đoạn chat mới
          </button>
        </div>

        {/* Chat box */}
        <div className="bg-white shadow-md rounded-xl p-6 space-y-4 min-h-[300px]">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`rounded-xl px-4 py-2 text-sm break-words inline-block ${
                  msg.role === "user"
                    ? "bg-blue-100 text-gray-800 text-left max-w-[60%]"
                    : "bg-gray-100 text-gray-900 text-left max-w-[80%]"
                }`}
              >
                {msg.content.split("\n").map((line, i) => (
                  <p key={i}>{line}</p>
                ))}
              </div>
            </div>
          ))}
          {isTyping && (
            <div className="text-sm text-gray-400 animate-pulse">AI đang trả lời...</div>
          )}
        </div>

        {/* Input */}
        <ChatPromptInput
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onSubmit={handleSubmit}
          placeholder="Nhập yêu cầu tạo dashboard (VD: 'Thống kê số sinh viên theo khoa')..."
          disabled={isTyping}
        />

        {/* Error */}
        {errorMessage && (
          <div className="p-4 bg-red-100 border border-red-200 rounded-lg text-red-700 text-sm">
            {errorMessage}
          </div>
        )}
      </div>
    </>
  );
}
