import { Loader2, Plus } from "lucide-react";

export function Button({ children, onClick, disabled }) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={`px-5 py-2.5 rounded-2xl text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200 ease-in-out flex items-center justify-center gap-2 text-sm font-medium`}
    >
      {children}
    </button>
  );
}