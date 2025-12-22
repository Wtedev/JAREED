// =====================
// Common Utilities
// =====================

function qs(sel, root = document) {
    return root.querySelector(sel);
  }
  
  function qsa(sel, root = document) {
    return Array.from(root.querySelectorAll(sel));
  }
  
  function fmt(v, fallback = "-") {
    return v === null || v === undefined || v === "" ? fallback : v;
  }
  
  function fmtDate(iso) {
    if (!iso) return "-";
    try {
      const d = new Date(iso);
      return d.toLocaleString();
    } catch {
      return iso;
    }
  }
  
  function setBadgeStatus(id, text, variant = "secondary") {
    const el = document.getElementById(id);
    if (!el) return;
  
    const map = {
      success: "badge text-bg-success",
      danger: "badge text-bg-danger",
      warning: "badge text-bg-warning",
      secondary: "badge text-bg-secondary",
    };
  
    el.className = map[variant] || map.secondary;
    el.textContent = text;
  }
  
  async function safeJson(res) {
    try {
      return await res.json();
    } catch {
      return null;
    }
  }
  
  /**
   * apiFetch(url, options)
   * Returns: { ok: boolean, status: number, data: any, error: string|null }
   */
  async function apiFetch(url, options = {}) {
    try {
      const res = await fetch(url, {
        cache: "no-store",
        ...options,
      });
  
      const data = await safeJson(res);
  
      // If backend uses {ok: true/false}
      if (res.ok) {
        if (data && typeof data === "object" && "ok" in data && data.ok === false) {
          return { ok: false, status: res.status, data, error: data.error || "Request failed" };
        }
        return { ok: true, status: res.status, data, error: null };
      }
  
      const errorMsg =
        (data && (data.error || data.message)) ||
        `HTTP Error ${res.status}`;
  
      return { ok: false, status: res.status, data, error: errorMsg };
    } catch (err) {
      console.error(err);
      return { ok: false, status: 0, data: null, error: "Network error" };
    }
  }
  
  /**
   * confirmAction(message)
   */
  function confirmAction(message) {
    return window.confirm(message);
  }
  