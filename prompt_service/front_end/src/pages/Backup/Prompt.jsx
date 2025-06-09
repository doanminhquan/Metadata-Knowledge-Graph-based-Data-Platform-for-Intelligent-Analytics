import { useState } from "react";
import { Card, CardContent } from "@/components/card.jsx";
import { Button } from "@/components/button.jsx";
import ChatPromptInput from "@/components/textarea.jsx";
import { Loader2, Plus } from "lucide-react";
import { motion } from "framer-motion";

export default function PromptToDashboard() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [iframeUrl, setIframeUrl] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    setIframeUrl("");
    setError("");

    try {
      const response = await fetch("/api/generate-dashboard", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) throw new Error("Lỗi khi gọi API.");
      const data = await response.json();
      setIframeUrl(data.iframeUrl);
    } catch (err) {
      console.error("Lỗi tạo dashboard:", err);
      setError("Đã xảy ra lỗi khi tạo dashboard. Vui lòng thử lại.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-12 px-6 space-y-8">
      {/* <Card>
        <CardContent className="space-y-6">
            <div className="space-y-2">
                <h1 className="text-3xl font-bold text-gray-900">Tạo Dashboard từ Prompt</h1>
                <p className="text-gray-600 text-sm">
                Nhập prompt để tạo dashboard tự động từ dữ liệu. Hệ thống sẽ phân tích và hiển thị kết quả phù hợp.
                </p>
            </div>


            <div className="text-sm text-gray-500 space-y-1">
                <p className="font-medium">Gợi ý:</p>
                <ul className="list-disc pl-5 space-y-1">
                <li>Tổng số sinh viên theo khoa</li>
                <li>Tỷ lệ nam/nữ theo ngành học</li>
                <li>Số lượng sinh viên mỗi năm</li>
                </ul>
            </div>

          {error && <p className="text-sm text-red-600 font-medium">{error}</p>}

          <div className="flex justify-end">
            <Button onClick={handleSubmit} disabled={loading || !prompt.trim()}>
              {loading ? <><Loader2 className="h-4 w-4 animate-spin" /> Đang tạo...</> : <><Plus className="w-4 h-4" /> Tạo Dashboard</>}
            </Button>
          </div>
        </CardContent>
      </Card> */}

      
        <ChatPromptInput
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onSubmit={handleSubmit}
        />

        {/* {iframeUrl && (
            <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="rounded-2xl overflow-hidden shadow-xl"
            >
            <iframe
                src={iframeUrl}
                className="w-full h-[600px] border rounded-2xl"
                allowFullScreen
            ></iframe>
            </motion.div>
        )} */}
    </div>
  );
}