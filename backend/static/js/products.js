// backend/static/js/products.js

const API_BASE = ""; // نفس الدومين
const PRODUCTS_API = `${API_BASE}/api/products`;

function setStatus(text, kind = "secondary") {
  const el = document.getElementById("pStatus");
  if (!el) return;
  el.className = `badge text-bg-${kind}`;
  el.textContent = text;
}

function escapeHtml(s) {
  return String(s ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function getFormValues() {
  return {
    rfid: (document.getElementById("rfid")?.value || "").trim(),
    name: (document.getElementById("name")?.value || "").trim(),
    type: (document.getElementById("type")?.value || "").trim(),
    unit_weight: Number(document.getElementById("unit_weight")?.value || 0),
  };
}

function clearForm() {
  const ids = ["rfid", "name", "type", "unit_weight"];
  ids.forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.value = "";
  });
  setStatus("تم المسح", "secondary");
}

async function loadProducts() {
  try {
    setStatus("جاري تحميل المنتجات...", "secondary");

    const res = await fetch(PRODUCTS_API);
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }

    const products = await res.json();
    renderProducts(products);

    setStatus(`تم التحميل (${products.length})`, "success");
  } catch (err) {
    console.error(err);
    setStatus("فشل تحميل المنتجات", "danger");
    document.getElementById("pRows").innerHTML = `
      <tr><td colspan="5" class="text-danger">فشل تحميل المنتجات</td></tr>
    `;
  }
}

function renderProducts(products) {
  const tbody = document.getElementById("pRows");
  if (!tbody) return;

  if (!Array.isArray(products) || products.length === 0) {
    tbody.innerHTML = `
      <tr><td colspan="5" class="text-muted">لا توجد منتجات بعد</td></tr>
    `;
    return;
  }

  tbody.innerHTML = products
    .map((p) => {
      const id = p.item_id;
      const rfid = ""; // مؤقتًا (غير موجود في DB)
      const type = ""; // مؤقتًا (غير موجود في DB)
      const name = p.product_name ?? "";
      const unit = p.unit_weight ?? "";

      return `
        <tr>
          <td class="text-muted">${escapeHtml(rfid)}</td>
          <td>${escapeHtml(name)}</td>
          <td class="text-muted">${escapeHtml(type)}</td>
          <td>${escapeHtml(unit)}</td>
          <td class="text-end">
            <button class="btn btn-sm btn-outline-secondary" onclick="fillFormFromRow(${id})">تعديل</button>
            <button class="btn btn-sm btn-outline-danger" onclick="deleteProduct(${id})">حذف</button>
          </td>
        </tr>
      `;
    })
    .join("");
}

async function saveProduct() {
  const { rfid, name, type, unit_weight } = getFormValues();

  // تحقق بسيط
  if (!name) {
    setStatus("اسم المنتج مطلوب", "warning");
    return;
  }
  if (!Number.isFinite(unit_weight) || unit_weight <= 0) {
    setStatus("وزن القطعة لازم يكون رقم أكبر من 0", "warning");
    return;
  }

  try {
    setStatus("جاري الحفظ...", "secondary");

    // ملاحظة: API عندك ما يدعم RFID/TYPE الآن
    // سنرسل فقط الحقول الموجودة في موديل InventoryItem
    const payload = {
      product_name: name,
      unit_weight: unit_weight,
      container_weight: 0,   // قيم افتراضية
      total_weight: unit_weight,
      quantity: 1,
      shelf_id: 1,
      status: "Normal",
    };

    const res = await fetch(PRODUCTS_API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const txt = await res.text();
      throw new Error(`HTTP ${res.status} - ${txt}`);
    }

    await res.json();
    setStatus("تم الحفظ ✅", "success");
    clearForm();
    await loadProducts();
  } catch (err) {
    console.error(err);
    setStatus("فشل الحفظ", "danger");
  }
}

// تعبئة الفورم من صف (نجيب المنتج من API ثم نحطه في الحقول)
async function fillFormFromRow(itemId) {
  try {
    setStatus("جاري جلب بيانات المنتج...", "secondary");
    const res = await fetch(`${PRODUCTS_API}/${itemId}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const p = await res.json();

    // نعبّي المتوفر فقط
    document.getElementById("name").value = p.product_name ?? "";
    document.getElementById("unit_weight").value = p.unit_weight ?? "";

    // هذه غير موجودة في DB حاليا
    document.getElementById("rfid").value = "";
    document.getElementById("type").value = "";

    // نخزن الـ id في عنصر مخفي داخل الصفحة (نضيفه ديناميكيًا)
    let hidden = document.getElementById("editing_id");
    if (!hidden) {
      hidden = document.createElement("input");
      hidden.type = "hidden";
      hidden.id = "editing_id";
      document.body.appendChild(hidden);
    }
    hidden.value = String(itemId);

    setStatus(`وضع التعديل (ID: ${itemId})`, "info");
  } catch (err) {
    console.error(err);
    setStatus("فشل جلب بيانات المنتج", "danger");
  }
}

async function deleteProduct(itemId) {
  if (!confirm("متأكدة تبين تحذفين المنتج؟")) return;

  try {
    setStatus("جاري الحذف...", "secondary");
    const res = await fetch(`${PRODUCTS_API}/${itemId}`, { method: "DELETE" });
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(`HTTP ${res.status} - ${txt}`);
    }
    setStatus("تم الحذف ✅", "success");
    await loadProducts();
  } catch (err) {
    console.error(err);
    setStatus("فشل الحذف", "danger");
  }
}

function initProductsPage() {
  // زر الحفظ في HTML يستدعي saveProduct() أصلاً
  loadProducts();
}
