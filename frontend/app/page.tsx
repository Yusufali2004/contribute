"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";

export default function Home() {
  const [repoUrl, setRepoUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  async function analyzeRepository() {
    if (!repoUrl.trim()) return;

    setLoading(true);
    setError("");
    setResult("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/repository/analyze?url=${encodeURIComponent(repoUrl)}`
      );

      if (!response.ok) {
        throw new Error("Unable to analyze repository");
      }

      const data = await response.json();
      setResult(data.analysis || data.result || JSON.stringify(data, null, 2));
    } catch (err) {
      setError(
        "Could not connect to the CONTribute backend. Make sure FastAPI is running."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#070707] text-white">
      <div className="mx-auto max-w-6xl px-6 py-10">
        {/* Header */}
        <nav className="flex items-center justify-between">
          <div className="text-xl font-bold tracking-tight">
            <span className="text-white">CON</span>
            <span className="text-emerald-400">Tribute</span>
          </div>

          <div className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-gray-400">
            Powered by Gemma 4
          </div>
        </nav>

        {/* Hero */}
        <section className="mx-auto max-w-4xl py-24 text-center">
          <div className="mb-6 inline-flex rounded-full border border-emerald-400/20 bg-emerald-400/5 px-4 py-2 text-sm text-emerald-300">
            Open-source contribution, simplified.
          </div>

          <h1 className="text-5xl font-black tracking-tight sm:text-7xl">
            Find your way into
            <br />
            <span className="text-emerald-400">any codebase.</span>
          </h1>

          <p className="mx-auto mt-7 max-w-2xl text-lg leading-8 text-gray-400">
            CONTribute turns an unfamiliar GitHub repository into a practical
            roadmap for your first contribution.
          </p>

          {/* Input */}
          <div className="mx-auto mt-10 flex max-w-3xl flex-col gap-3 rounded-2xl border border-white/10 bg-white/[0.04] p-3 shadow-2xl sm:flex-row">
            <input
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") analyzeRepository();
              }}
              placeholder="https://github.com/owner/repository"
              className="min-w-0 flex-1 rounded-xl bg-transparent px-4 py-4 text-white outline-none placeholder:text-gray-600"
            />

            <button
              onClick={analyzeRepository}
              disabled={loading}
              className="rounded-xl bg-emerald-400 px-7 py-4 font-semibold text-black transition hover:bg-emerald-300 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Analyzing..." : "Analyze repository →"}
            </button>
          </div>

          <p className="mt-4 text-sm text-gray-600">
            Try: github.com/Yusufali2004/smart-sort
          </p>
        </section>

        {/* Loading */}
        {loading && (
          <section className="mx-auto max-w-4xl rounded-2xl border border-white/10 bg-white/[0.03] p-8">
            <div className="flex items-center gap-4">
              <div className="h-3 w-3 animate-pulse rounded-full bg-emerald-400" />
              <div>
                <p className="font-medium">Understanding the repository...</p>
                <p className="mt-1 text-sm text-gray-500">
                  Crawling code → retrieving context → asking Gemma 4
                </p>
              </div>
            </div>
          </section>
        )}

        {/* Error */}
        {error && (
          <section className="mx-auto max-w-4xl rounded-2xl border border-red-400/20 bg-red-400/5 p-6 text-red-300">
            {error}
          </section>
        )}

        {/* Result */}
        {result && (
          <section className="mx-auto max-w-4xl pb-20">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-2xl font-bold">Repository Intelligence</h2>
              <span className="rounded-full border border-emerald-400/20 bg-emerald-400/5 px-3 py-1 text-xs text-emerald-300">
                Gemma 4 + RAG
              </span>
            </div>

            <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-7 text-gray-300">
              <ReactMarkdown
                components={{
                  h1: ({ children }) => (
                    <h1 className="mb-5 mt-2 text-2xl font-bold text-white">
                      {children}
                    </h1>
                  ),
                  h2: ({ children }) => (
                    <h2 className="mb-4 mt-8 text-xl font-bold text-white">
                      {children}
                    </h2>
                  ),
                  h3: ({ children }) => (
                    <h3 className="mb-3 mt-6 text-lg font-semibold text-emerald-400">
                      {children}
                    </h3>
                  ),
                  p: ({ children }) => (
                    <p className="mb-4 leading-7 text-gray-300">
                      {children}
                    </p>
                  ),
                  ul: ({ children }) => (
                    <ul className="mb-5 ml-6 list-disc space-y-2 text-gray-300">
                      {children}
                    </ul>
                  ),
                  ol: ({ children }) => (
                    <ol className="mb-5 ml-6 list-decimal space-y-2 text-gray-300">
                      {children}
                    </ol>
                  ),
                  li: ({ children }) => (
                    <li className="pl-1">{children}</li>
                  ),
                  code: ({ children }) => (
                    <code className="rounded bg-black/50 px-1.5 py-0.5 text-sm text-emerald-300">
                      {children}
                    </code>
                  ),
                }}
              >
                {result}
              </ReactMarkdown>
            </div>
          </section>
        )}

        {/* Feature cards */}
        {!result && !loading && (
          <section className="grid gap-4 pb-20 md:grid-cols-3">
            <Feature
              number="01"
              title="Understand"
              description="Get a grounded explanation of the repository architecture and important files."
            />

            <Feature
              number="02"
              title="Discover"
              description="Identify practical contribution opportunities instead of randomly exploring the codebase."
            />

            <Feature
              number="03"
              title="Contribute"
              description="Know what to inspect, what to change, and what you will learn."
            />
          </section>
        )}

        {/* Footer */}
        <footer className="border-t border-white/10 py-8 text-center text-sm text-gray-600">
          Built for Hacktoberfest Hack Day Bengaluru · Open Source AI
        </footer>
      </div>
    </main>
  );
}

function Feature({
  number,
  title,
  description,
}: {
  number: string;
  title: string;
  description: string;
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6 transition hover:border-emerald-400/30">
      <div className="mb-8 text-sm text-emerald-400">{number}</div>

      <h3 className="text-xl font-bold">{title}</h3>

      <p className="mt-3 leading-6 text-gray-500">{description}</p>
    </div>
  );
}