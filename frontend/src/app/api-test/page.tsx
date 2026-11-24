
"use client";

import { useState } from "react";
import { checkApiHealth } from "../../lib/api/health";

export default function ApiTestPage() {
  const [result, setResult] = useState("Not tested");
  const [loading, setLoading] = useState(false);

  async function testConnection() {
    setLoading(true);
    setResult("Connecting...");

    try {
      const response = await checkApiHealth();

      setResult(JSON.stringify(response, null, 2));
    } catch (error) {
      setResult(
        error instanceof Error
          ? error.message
          : "Connection failed"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-background p-10 text-foreground">
      <h1 className="mb-4 text-2xl font-bold">
        Backend Connection Test
      </h1>

      <p className="mb-6 text-sm text-muted">
        Test communication between Next.js and FastAPI.
      </p>

      <button
        onClick={testConnection}
        disabled={loading}
        className="rounded-lg bg-primary px-5 py-3 text-white disabled:opacity-50"
      >
        {loading ? "Connecting..." : "Test FastAPI Connection"}
      </button>

      <pre className="mt-6 whitespace-pre-wrap rounded-xl border border-border bg-surface p-5 text-sm">
        {result}
      </pre>
    </main>
  );
}
