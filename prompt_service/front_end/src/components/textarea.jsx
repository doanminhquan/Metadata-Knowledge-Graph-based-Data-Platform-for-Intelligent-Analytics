import { useRef } from "react";
import { Send } from "lucide-react";

export default function ChatPromptInput({ value, onChange, onSubmit, placeholder, disabled }) {
  const textareaRef = useRef(null);

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!disabled) onSubmit();
    }
  };

  return (
    <div className="relative">
      <textarea
        ref={textareaRef}
        rows={1}
        value={value}
        onChange={onChange}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={disabled}
        className="w-full resize-none rounded-xl border border-gray-300 bg-white py-3 pl-4 pr-12 text-sm text-gray-900 shadow-sm placeholder:text-gray-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 focus:outline-none disabled:opacity-50"
      />
      <button
        onClick={() => !disabled && onSubmit()}
        className="absolute right-2 top-2.5 p-1.5 rounded-full hover:bg-gray-100 transition"
        disabled={disabled}
      >
        <Send className="w-5 h-5 text-blue-600" />
      </button>
    </div>
  );
}
