export function Card({ children, className = "" }) {
  return <div className={`bg-white rounded-2xl border border-gray-200 shadow ${className}`}>{children}</div>;
}

export function CardContent({ children, className = "" }) {
  return <div className={`p-6 ${className}`}>{children}</div>;
}