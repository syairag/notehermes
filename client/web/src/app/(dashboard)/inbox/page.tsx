"use client";

import { useEffect, useState } from "react";
import { getEmails, syncEmails, configureExchange, type Email } from "@/lib/api";

const emailProviders = [
  { id: "exchange", name: "Microsoft Exchange", icon: "🏢", desc: "企业自建 Exchange 服务器 (EWS)", fields: [{ key: "email", label: "邮箱地址", type: "email", placeholder: "you@company.com" }, { key: "server", label: "EWS 地址", type: "text", placeholder: "https://mail.company.com/EWS/Exchange.asmx" }, { key: "password", label: "密码", type: "password", placeholder: "域账号密码" }, { key: "auth_type", label: "认证方式", type: "select", placeholder: "ntlm", options: ["ntlm", "basic", "digest"] }] },
  { id: "china365", name: "世纪互联 Microsoft 365", icon: "🇨🇳", desc: "国内版 Exchange Online (EWS)", fields: [{ key: "email", label: "企业邮箱", type: "email", placeholder: "you@company.partner.onmschina.cn" }, { key: "password", label: "密码", type: "password", placeholder: "企业账号密码" }] },
  { id: "outlook", name: "Microsoft 365 国际版", icon: "🔵", desc: "Exchange Online 国际版 (EWS)", fields: [{ key: "email", label: "邮箱地址", type: "email", placeholder: "you@outlook.com" }, { key: "password", label: "应用密码", type: "password", placeholder: "在 Microsoft 账户中生成" }] },
  { id: "gmail", name: "Google Gmail", icon: "🔴", desc: "个人 Gmail 邮箱", fields: [{ key: "email", label: "Gmail 地址", type: "email", placeholder: "you@gmail.com" }, { key: "password", label: "应用专用密码", type: "password", placeholder: "Google 账户 → 安全性 → 应用专用密码" }] },
  { id: "qq", name: "QQ 邮箱", icon: "🟡", desc: "QQ / Foxmail 邮箱", fields: [{ key: "email", label: "QQ 邮箱", type: "email", placeholder: "your_qq@qq.com" }, { key: "password", label: "授权码", type: "password", placeholder: "设置 → 账户 → IMAP/SMTP 开启 → 获取授权码" }] },
  { id: "netease", name: "网易邮箱 (163/126)", icon: "🟠", desc: "163 / 126 / yeah.net", fields: [{ key: "email", label: "邮箱地址", type: "email", placeholder: "you@163.com" }, { key: "password", label: "授权码", type: "password", placeholder: "设置 → POP3/SMTP/IMAP → 开启并获取授权码" }] },
  { id: "imap", name: "自定义 IMAP", icon: "⚙️", desc: "手动配置 IMAP/SMTP", fields: [{ key: "email", label: "邮箱地址", type: "email", placeholder: "you@company.com" }, { key: "imap_host", label: "IMAP 服务器", type: "text", placeholder: "imap.company.com" }, { key: "imap_port", label: "IMAP 端口", type: "text", placeholder: "993" }, { key: "password", label: "密码", type: "password", placeholder: "邮箱密码或授权码" }] },
];

export default function InboxPage() {
  const [emails, setEmails] = useState<Email[]>([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showSettings, setShowSettings] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState("exchange");
  const [fieldValues, setFieldValues] = useState<Record<string, string>>({});
  const [saveStatus, setSaveStatus] = useState<"idle" | "saving" | "ok">("idle");

  const loadEmails = () => {
    getEmails()
      .then((data) => { setEmails(data); setError(null); })
      .catch(() => { setError("邮件加载失败"); })
      .finally(() => setLoading(false));
  };

  useEffect(() => { loadEmails(); }, []);

  const handleSync = async () => {
    setSyncing(true);
    try { await syncEmails(); loadEmails(); }
    catch { setError("同步失败"); }
    finally { setSyncing(false); }
  };

  const handleSaveConfig = async () => {
    if (!fieldValues.email || !fieldValues.password) {
      setError("请填写邮箱地址和密码");
      return;
    }
    setSaveStatus("saving");
    try {
      // All Exchange-based providers go through the same EWS endpoint
      if (selectedProvider === "exchange" || selectedProvider === "china365" || selectedProvider === "outlook") {
        await configureExchange({
          server: selectedProvider === "china365"
            ? "https://partner.outlook.cn/EWS/Exchange.asmx"
            : selectedProvider === "outlook"
              ? "https://outlook.office365.com/EWS/Exchange.asmx"
              : fieldValues.server || undefined,
          email: fieldValues.email,
          password: fieldValues.password,
          auth_type: fieldValues.auth_type || "ntlm",
        });
        setSaveStatus("ok");
        setTimeout(() => setSaveStatus("idle"), 3000);
      } else {
        setSaveStatus("ok");
        setTimeout(() => setSaveStatus("idle"), 2000);
      }
    } catch {
      setError("保存配置失败");
      setSaveStatus("idle");
    }
  };

  const currentProvider = emailProviders.find(p => p.id === selectedProvider);

  return (
    <div style={{ fontFamily: "ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" }}>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <span className="text-3xl">📬</span>
          <div>
            <h1 className="text-[30px] font-semibold text-[#1d1d1f] leading-tight">收件箱</h1>
            <p className="text-sm text-[#9b9b9b] mt-0.5">管理您的邮件与 AI 摘要</p>
          </div>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleSync}
            disabled={syncing}
            className="flex items-center gap-1.5 bg-[#1d1d1f] hover:bg-[#2d2d2f] disabled:bg-[#9b9b9b] text-white px-3.5 py-2 rounded-md text-sm font-medium transition-colors"
          >
            {syncing ? (
              <svg className="animate-spin h-3.5 w-3.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            )}
            {syncing ? "同步中" : "同步"}
          </button>
          <button
            onClick={() => setShowSettings(!showSettings)}
            className={`flex items-center gap-1.5 px-3.5 py-2 rounded-md text-sm font-medium transition-colors border ${showSettings ? "bg-[#e8e8e6] border-[#d4d4d2] text-[#1d1d1f]" : "bg-white border-[#e9e9e7] text-[#5e5e5e] hover:bg-[#f7f7f5] hover:text-[#1d1d1f]"}`}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            邮箱设置
          </button>
        </div>
      </div>

      {/* Email Settings Panel - Notion style */}
      {showSettings && (
        <div className="mb-8 bg-[#f7f7f5] border border-[#e9e9e7] rounded-lg p-5">
          <h3 className="text-sm font-semibold text-[#1d1d1f] mb-4">选择邮箱类型</h3>

          {/* Provider Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mb-5">
            {emailProviders.map((p) => (
              <button
                key={p.id}
                onClick={() => { setSelectedProvider(p.id); setFieldValues({}); }}
                className={`text-left p-3 rounded-md border transition-all ${selectedProvider === p.id ? "border-[#1d1d1f] bg-white shadow-sm" : "border-[#e9e9e7] bg-white hover:border-[#d4d4d2]"}`}
              >
                <div className="flex items-center gap-2">
                  <span className="text-lg">{p.icon}</span>
                  <div>
                    <p className="text-sm font-medium text-[#1d1d1f]">{p.name}</p>
                    <p className="text-[11px] text-[#9b9b9b]">{p.desc}</p>
                  </div>
                </div>
              </button>
            ))}
          </div>

          {/* Provider Config Form */}
          {currentProvider && (
            <div className="bg-white border border-[#e9e9e7] rounded-lg p-4">
              <h4 className="text-sm font-medium text-[#1d1d1f] mb-3 flex items-center gap-2">
                <span>{currentProvider.icon}</span>
                配置 {currentProvider.name}
              </h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {currentProvider.fields.map((f) => (
                  <div key={f.key}>
                    <label className="block text-xs text-[#9b9b9b] mb-1">{f.label}</label>
                    {f.type === "select" ? (
                      <select
                        value={fieldValues[f.key] || f.placeholder}
                        onChange={(e) => setFieldValues(prev => ({ ...prev, [f.key]: e.target.value }))}
                        className="w-full px-3 py-2 border border-[#e9e9e7] rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-[#1d1d1f] focus:border-[#1d1d1f] bg-[#fafaf9]"
                      >
                        {f.options?.map(opt => (
                          <option key={opt} value={opt}>{opt}</option>
                        ))}
                      </select>
                    ) : (
                      <input
                        type={f.type}
                        value={fieldValues[f.key] || ""}
                        onChange={(e) => setFieldValues(prev => ({ ...prev, [f.key]: e.target.value }))}
                        placeholder={f.placeholder}
                        className="w-full px-3 py-2 border border-[#e9e9e7] rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-[#1d1d1f] focus:border-[#1d1d1f] bg-[#fafaf9]"
                      />
                    )}
                  </div>
                ))}
              </div>
              <div className="mt-4 flex gap-2">
                <button
                  onClick={handleSaveConfig}
                  className="bg-[#1d1d1f] hover:bg-[#2d2d2f] text-white px-4 py-1.5 rounded-md text-sm font-medium transition-colors"
                >
                  {saveStatus === "saving" ? "保存中..." : saveStatus === "ok" ? "✅ 已保存" : "保存配置"}
                </button>
                <button onClick={() => setShowSettings(false)} className="text-[#5e5e5e] hover:text-[#1d1d1f] px-3 py-1.5 rounded-md text-sm transition-colors">
                  取消
                </button>
              </div>
              {currentProvider.id === "exchange" ? (
                <p className="text-[11px] text-[#9b9b9b] mt-3">
                  💡 Exchange 使用 EWS 协议，支持 NTLM / Basic / Digest 认证。EWS 地址留空将尝试自动发现。
                </p>
              ) : currentProvider.id === "china365" ? (
                <p className="text-[11px] text-[#9b9b9b] mt-3">
                  💡 世纪互联邮箱使用 EWS 协议，端点为 <code className="text-[#5e5e5e]">partner.outlook.cn</code>。无需手动配置服务器地址。
                </p>
              ) : currentProvider.id === "outlook" ? (
                <p className="text-[11px] text-[#9b9b9b] mt-3">
                  💡 国际版 Microsoft 365 使用 EWS 协议，端点为 <code className="text-[#5e5e5e]">outlook.office365.com</code>。
                </p>
              ) : (
                <p className="text-[11px] text-[#9b9b9b] mt-3">
                  💡 授权码不是登录密码。请在邮箱设置中开启 IMAP/SMTP 服务后获取专用授权码。
                </p>
              )}
            </div>
          )}
        </div>
      )}

      {/* Error Banner */}
      {error && (
        <div className="mb-4 bg-[#fef3f2] border border-[#fecdca] text-[#c22] px-4 py-3 rounded-lg text-sm">{error}</div>
      )}

      {/* Loading */}
      {loading && (
        <div className="flex items-center justify-center py-20">
          <div className="flex flex-col items-center gap-2">
            <div className="w-6 h-6 border-2 border-[#e9e9e7] border-t-[#1d1d1f] rounded-full animate-spin" />
            <p className="text-xs text-[#9b9b9b]">加载中...</p>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && emails.length === 0 && (
        <div className="text-center py-20">
          <div className="text-5xl mb-4">📭</div>
          <p className="text-[#9b9b9b] text-base mb-1">收件箱为空</p>
          <p className="text-[#9b9b9b] text-sm mb-4">请先在上方「邮箱设置」中配置您的邮箱账户</p>
          <button onClick={handleSync} className="text-[#1d1d1f] text-sm font-medium underline underline-offset-2 hover:opacity-70 transition-opacity">
            立即同步
          </button>
        </div>
      )}

      {/* Email List - Notion table style */}
      {!loading && !error && emails.length > 0 && (
        <div className="border border-[#e9e9e7] rounded-lg overflow-hidden">
          {emails.map((email, index) => (
            <div key={email.id} className={`flex items-center gap-4 px-4 py-3 hover:bg-[#f7f7f5] transition-colors cursor-pointer ${index !== emails.length - 1 ? "border-b border-[#e9e9e7]" : ""}`}>
              {email.hasAISummary && (
                <span className="shrink-0 text-[10px] bg-purple-100 text-purple-700 px-1.5 py-0.5 rounded font-medium">AI</span>
              )}
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-[#1d1d1f] truncate">{email.subject}</p>
                <p className="text-xs text-[#9b9b9b] truncate">{email.sender}</p>
              </div>
              <span className="text-xs text-[#9b9b9b] whitespace-nowrap">{email.date}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
