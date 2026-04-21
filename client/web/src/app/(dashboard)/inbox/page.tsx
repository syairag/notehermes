"use client";

import { useEffect, useState } from "react";
import { getEmails, type Email } from "@/lib/api";

export default function InboxPage() {
  const [emails, setEmails] = useState<Email[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getEmails()
      .then((data) => {
        setEmails(data);
        setError(null);
      })
      .catch((err) => {
        console.error("Failed to fetch emails:", err);
        setError("Failed to load emails");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">📧 Inbox</h1>
        <p className="text-sm text-gray-500 mt-1">
          Your emails with AI-powered summaries
        </p>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="flex items-center justify-center py-12">
          <p className="text-gray-500">Loading...</p>
        </div>
      )}

      {/* Error State */}
      {error && !loading && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-center">
          <p className="text-red-600 text-sm">{error}</p>
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && emails.length === 0 && (
        <div className="bg-white border border-gray-200 rounded-xl shadow-sm p-8 text-center">
          <p className="text-gray-500">Empty Inbox</p>
        </div>
      )}

      {/* Email List */}
      {!loading && !error && emails.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
          {emails.map((email, index) => (
            <div
              key={email.id}
              className={`flex flex-col sm:flex-row sm:items-center gap-2 px-5 py-4 hover:bg-gray-50 transition-colors cursor-pointer ${
                index !== emails.length - 1 ? "border-b border-gray-100" : ""
              }`}
            >
              {/* AI Summary Badge */}
              <div className="flex items-center gap-3 shrink-0 w-28">
                {email.hasAISummary && (
                  <span className="inline-flex items-center gap-1 bg-purple-100 text-purple-700 text-[10px] font-semibold px-2 py-0.5 rounded-full uppercase tracking-wide">
                    🤖 AI
                  </span>
                )}
              </div>

              {/* Subject */}
              <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold text-gray-900 truncate">
                  {email.subject}
                </p>
                <p className="text-xs text-gray-500 truncate">{email.sender}</p>
              </div>

              {/* Date */}
              <span className="text-xs text-gray-400 whitespace-nowrap shrink-0">
                {email.date}
              </span>
            </div>
          ))}

          {/* AI Summary Panel (shown for emails that have it) */}
          {emails
            .filter((e) => e.hasAISummary)
            .slice(0, 1)
            .map((email) => (
              <div
                key={`summary-${email.id}`}
                className="border-t border-purple-100 bg-purple-50/50 px-5 py-4"
              >
                <div className="flex items-start gap-3">
                  <span className="text-lg shrink-0 mt-0.5">🤖</span>
                  <div>
                    <p className="text-xs font-semibold text-purple-700 uppercase tracking-wide mb-1">
                      AI Summary
                    </p>
                    <p className="text-sm text-gray-700 leading-relaxed">
                      {email.summary}
                    </p>
                  </div>
                </div>
              </div>
            ))}
        </div>
      )}
    </div>
  );
}
