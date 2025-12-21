// =====================
// Warehouse Page JS
// =====================

let refreshTimer = null;

function fmt(v) {
  return v === null || v === undefined ? "-" : v;
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

function setStatusLoading() {
  const status = document.getElementById("status");
  if (!status) return;
  status.className = "badge text-bg-secondary";
  status.textContent = "جاري التحميل...";
}

function setStatusOk() {
  const status = document.getElementById("status");
  if (!status) return;
  status.className = "badge text-bg-success";
  status.textContent = "متصل";
}

function setStatusError() {
  const status = document.getElementById("status");
  if (!status) return;
  status.className = "badge text-bg-danger";
  status.textContent = "خطأ في الاتصال";
}

function setAutoRefresh(ms) {
  if (refreshTimer) clearInterval(refreshTimer);
  refreshTimer = null;

  if (ms > 0) {
    refreshTimer = setInterval(loadWarehouse, ms);
  }
}

async function loadWarehouse() {
  setStatusLoading();

  try {
    const res = await fetch("/api/warehouse", { cache: "no-store" });
    const data = await res.json();

    if (!res.ok || !data.ok) {
      throw new Error("API error");
    }

    const rows = data.rows || [];

    // KPIs
    const kpiBoxes = document.getElementById("kpiBoxes");
    const kpiEmpty = document.getElementById("kpiEmpty");
    const kpiLastUpdate = document.getElementById("kpiLastUpdate");

    if (kpiBoxes) kpiBoxes.textContent = rows.length;

    const emptyCount = rows.filter((r) => !r.rfid).length;
    if (kpiEmpty) kpiEmpty.textContent = emptyCount;

    const last = rows
      .map((r) => r.updated_at)
      .filter(Boolean)
      .sort()
      .pop();
    if (kpiLastUpdate) kpiLastUpdate.textContent = fmtDate(last);

    // Table rows
    const tbody = document.getElementById("rows");
    if (!tbody) return;

    if (rows.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="8" class="text-muted">لا توجد بيانات</td>
        </tr>
      `;
    } else {
      tbody.innerHTML = rows
        .map((r) => {
          const hasRfid = !!r.rfid;
          const badgeClass = hasRfid ? "text-bg-success" : "text-bg-warning";
          const rfidCell = hasRfid
            ? `<span class="badge ${badgeClass}">${r.rfid}</span>`
            : `<span class="badge ${badgeClass}">بدون RFID</span>`;

          return `
            <tr>
              <td class="fw-semibold">${fmt(r.box_id)}</td>
              <td>${rfidCell}</td>
              <td>${fmt(r.product_name)}</td>
              <td>${fmt(r.product_type)}</td>
              <td>${fmt(r.unit_weight)}</td>
              <td>${fmt(r.total_weight)}</td>
              <td class="fw-bold">${fmt(r.quantity)}</td>
              <td class="text-muted small">${fmtDate(r.updated_at)}</td>
            </tr>
          `;
        })
        .join("");
    }

    setStatusOk();
  } catch (err) {
    console.error(err);
    setStatusError();
  }
}

function initWarehousePage() {
  // Auto-refresh selector
  const sel = document.getElementById("refreshRate");
  if (sel) {
    sel.addEventListener("change", () => {
      const ms = parseInt(sel.value, 10);
      setAutoRefresh(ms);
    });

    // initial
    setAutoRefresh(parseInt(sel.value, 10));
  }

  loadWarehouse();
}
