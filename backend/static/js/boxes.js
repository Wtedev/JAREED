// =====================
// Boxes Setup Page JS
// =====================

function setBStatus(text, variant = "secondary") {
    const el = document.getElementById("bStatus");
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
  
  function fmt(v) {
    return v === null || v === undefined ? "-" : v;
  }
  
  async function loadBoxes() {
    setBStatus("جاري التحميل...", "secondary");
  
    try {
      const res = await fetch("/api/boxes", { cache: "no-store" });
      const data = await res.json();
  
      if (!res.ok || !data.ok) throw new Error("API error");
  
      const rows = data.rows || [];
      const tbody = document.getElementById("bRows");
      if (!tbody) return;
  
      if (rows.length === 0) {
        tbody.innerHTML = `<tr><td colspan="9" class="text-muted">لا توجد بوكسات</td></tr>`;
        setBStatus("جاهز", "success");
        return;
      }
  
      tbody.innerHTML = rows
        .map((r) => {
          const currentRfid = r.rfid || "";
          const productName = r.product_name ? r.product_name : "غير مرتبط";
          const unitW = r.unit_weight ?? "-";
  
          return `
            <tr>
              <td class="fw-semibold">${fmt(r.box_id)}</td>
  
              <td style="min-width:220px;">
                <input
                  class="form-control form-control-sm"
                  id="rfid_${r.box_id}"
                  value="${currentRfid}"
                  placeholder="اكتب RFID أو اتركه فارغ"
                />
                <div class="text-muted small mt-1">${productName}</div>
              </td>
  
              <td>${fmt(r.product_name)}</td>
              <td>${fmt(unitW)}</td>
              <td>${fmt(r.total_weight)}</td>
              <td>${fmt(r.tare_weight)}</td>
              <td>${fmt(r.net_weight)}</td>
              <td class="fw-bold">${fmt(r.quantity)}</td>
  
              <td class="text-end" style="min-width:260px;">
                <div class="d-inline-flex gap-2">
                  <button class="btn btn-outline-primary btn-sm" onclick='assignRfid("${r.box_id}")'>تعيين</button>
                  <button class="btn btn-outline-secondary btn-sm" onclick='tareBox("${r.box_id}")'>Tare</button>
                  <button class="btn btn-outline-secondary btn-sm" onclick='resetBox("${r.box_id}")'>Reset</button>
                </div>
              </td>
            </tr>
          `;
        })
        .join("");
  
      setBStatus("جاهز", "success");
    } catch (err) {
      console.error(err);
      setBStatus("تعذر تحميل البوكسات", "danger");
    }
  }
  
  async function assignRfid(boxId) {
    const input = document.getElementById(`rfid_${boxId}`);
    const rfid = input ? input.value.trim() : "";
  
    setBStatus("جارٍ الحفظ...", "secondary");
  
    try {
      const res = await fetch(`/api/boxes/${encodeURIComponent(boxId)}/assign`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rfid: rfid || null }),
      });
  
      const j = await res.json().catch(() => ({}));
      if (!res.ok || !j.ok) {
        setBStatus(j.error || "فشل التعيين", "danger");
        return;
      }
  
      setBStatus("تم التعيين", "success");
      loadBoxes();
    } catch (err) {
      console.error(err);
      setBStatus("خطأ أثناء التعيين", "danger");
    }
  }
  
  async function tareBox(boxId) {
    const ok = confirm(`تعيين وزن العلبة (Tare) للبوكس ${boxId} باستخدام الوزن الحالي؟`);
    if (!ok) return;
  
    setBStatus("جارٍ تنفيذ Tare...", "secondary");
  
    try {
      const res = await fetch(`/api/boxes/${encodeURIComponent(boxId)}/tare`, {
        method: "POST",
      });
  
      const j = await res.json().catch(() => ({}));
      if (!res.ok || !j.ok) {
        setBStatus(j.error || "فشل Tare", "danger");
        return;
      }
  
      setBStatus("تم تنفيذ Tare", "success");
      loadBoxes();
    } catch (err) {
      console.error(err);
      setBStatus("خطأ أثناء Tare", "danger");
    }
  }
  
  async function resetBox(boxId) {
    const ok = confirm(`Reset للبوكس ${boxId}؟ سيتم تصفير الوزن والكمية.`);
    if (!ok) return;
  
    setBStatus("جارٍ تنفيذ Reset...", "secondary");
  
    try {
      const res = await fetch(`/api/boxes/${encodeURIComponent(boxId)}/reset`, {
        method: "POST",
      });
  
      const j = await res.json().catch(() => ({}));
      if (!res.ok || !j.ok) {
        setBStatus(j.error || "فشل Reset", "danger");
        return;
      }
  
      setBStatus("تم Reset", "success");
      loadBoxes();
    } catch (err) {
      console.error(err);
      setBStatus("خطأ أثناء Reset", "danger");
    }
  }
  
  function initBoxesPage() {
    loadBoxes();
  }
  