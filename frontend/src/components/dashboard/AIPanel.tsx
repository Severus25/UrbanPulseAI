"use client";

import { useState } from "react";

export function AIPanel() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      // TODO: Call orchestration API
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/query`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query, location: null }),
        }
      );
      const data = await res.json();
      setResponse(data.explanation || "No explanation available.");
    } catch {
      setResponse("Failed to get response. Check API connection.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 space-y-3">
      {response && (
        <div className="bg-gray-900 rounded-lg p-3 text-sm text-gray-300 max-h-40 overflow-y-auto">
          {response}
        </div>
      )}

      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about traffic, routes, or risks..."
          className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm 
                     text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
        />
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 
                     rounded-lg text-sm font-medium transition-colors"
        >
          {loading ? "..." : "Ask"}
        </button>
      </form>
    </div>
  );
}
