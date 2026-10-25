// ═══════════════════════════════════════════════════════════════
// 🎫 Ticket System Frontend Controller
// مدیریت کامل تعاملات صفحه تیکت‌ها
//
// شامل:
// - باز کردن مودال جزئیات با کلیک روی عنوان تیکت
// - برداشتن تیکت
// - بستن تیکت
// - ارسال پیام
// - رفرش جدول
// - فیلتر جدول
// ═══════════════════════════════════════════════════════════════

// ═══════════════════════════════════════════════════════════════
// 🌍 State های سراسری سیستم
// ═══════════════════════════════════════════════════════════════

let ticketWithdrawn = false;
let currentTicketDetailUrl = null;

// ═══════════════════════════════════════════════════════════════
// 🚀 راه‌اندازی اولیه صفحه
// ═══════════════════════════════════════════════════════════════

document.addEventListener("DOMContentLoaded", function() {

    const modalElement = document.getElementById("ticketModal");

    if (modalElement) {
        // وقتی مودال بسته شد
        modalElement.addEventListener("hidden.bs.modal", function() {
            if (ticketWithdrawn) {
                console.log("🔄 Refreshing ticket table...");
                fetchNewTicketList();
            }
            ticketWithdrawn = false;
            currentTicketDetailUrl = null;
        });
    }

    initializeTicketRows();
    initializeTableFilter();

});

/* ═══════════════════════════════════════════════════════════════
   📂 باز کردن مودال جزئیات تیکت
═══════════════════════════════════════════════════════════════ */

function openTicketModal(url, rowElement) {

    const modalElement = document.getElementById("ticketModal");
    const modalBody = document.getElementById("ticketModalBody");

    if (!modalElement || !modalBody) return;

    const ticketModal = bootstrap.Modal.getOrCreateInstance(modalElement);

    currentTicketDetailUrl = url;

    // حذف active از همه ردیف‌ها و اضافه کردن به ردیف جاری
    document.querySelectorAll(".ticket-row").forEach(r => r.classList.remove("active"));
    if (rowElement) rowElement.classList.add("active");

    // نمایش loading
    modalBody.innerHTML = `
        <div class="text-center p-4">
            <div class="spinner-border text-primary" role="status"></div>
            <div class="small text-muted mt-2">در حال بارگذاری اطلاعات تیکت...</div>
        </div>
    `;

    ticketModal.show();

    fetch(url, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(res => {
            if (!res.ok) throw new Error("خطا در دریافت اطلاعات تیکت");
            return res.text();
        })
        .then(html => {
            modalBody.innerHTML = html;

            // فعال‌سازی popover ها
            modalBody
                .querySelectorAll('[data-bs-toggle="popover"]')
                .forEach(el => new bootstrap.Popover(el));
        })
        .catch(err => {
            modalBody.innerHTML = `
            <div class="alert alert-danger my-3">
                ${err.message}
            </div>
        `;
        });

}

/* ═══════════════════════════════════════════════════════════════
   🔄 رفرش محتوای مودال
═══════════════════════════════════════════════════════════════ */

function refreshModalContent() {

    const modalBody = document.getElementById("ticketModalBody");
    if (!currentTicketDetailUrl || !modalBody) return;

    modalBody.innerHTML = `
        <div class="text-center p-4">
            <div class="spinner-border text-primary" role="status"></div>
        </div>
    `;

    fetch(currentTicketDetailUrl, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(r => r.text())
        .then(html => {
            modalBody.innerHTML = html;
            modalBody
                .querySelectorAll('[data-bs-toggle="popover"]')
                .forEach(el => new bootstrap.Popover(el));
        });

}

/* ═══════════════════════════════════════════════════════════════
   📋 فعال کردن کلیک روی عنوان تیکت‌ها (اصلاح شده)
═══════════════════════════════════════════════════════════════ */

function initializeTicketRows() {
    // از Event Delegation تمیز استفاده می‌کنیم تا حتی پس از رفرش با AJAX
    // نیاز به بایند مجدد نباشد و با کلیک روی هر بخش از عنوان اجرا شود.
    document.removeEventListener("click", handleTicketTitleClick);
    document.addEventListener("click", handleTicketTitleClick);
}

function handleTicketTitleClick(event) {
    const titleLink = event.target.closest(".ticket-title-link");

    if (titleLink) {
        event.preventDefault();
        event.stopPropagation(); // جلوگیری از انتخاب سطر یا عملکردهای ناخواسته

        const url = titleLink.dataset.url;
        const row = titleLink.closest(".ticket-row");

        if (url) {
            openTicketModal(url, row);
        }
    }
}

/* ═══════════════════════════════════════════════════════════════
   ⚙️ تابع مشترک برای عملیات AJAX دکمه‌ها
═══════════════════════════════════════════════════════════════ */

function handleTicketAction(button, successConfig) {

    const url = button.dataset.url;
    const csrf = button.dataset.csrf;
    const original = button.innerHTML;

    button.disabled = true;

    fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrf,
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(r => r.json())
        .then(data => {

            if (data.status !== "success") throw new Error(data.message);

            if (typeof showToast === "function") {
                showToast(data.message, "success");
            }

            button.className = successConfig.class;
            button.innerHTML = successConfig.html;

            ticketWithdrawn = true;

            const row = button.closest(".ticket-row");
            if (row) {
                const cell = row.children[3]; // ستون وضعیت
                if (cell) cell.innerHTML = successConfig.statusHTML;
            }

            const modal = document.getElementById("ticketModal");
            if (modal && modal.classList.contains("show")) {
                refreshModalContent();
            }

        })
        .catch(err => {
            if (typeof showToast === "function") {
                showToast(err.message || "خطا در ارتباط با سرور", "danger");
            }
            button.disabled = false;
            button.innerHTML = original;
        });

}

/* ═══════════════════════════════════════════════════════════════
   🎯 Event Delegation برای دکمه‌ها
═══════════════════════════════════════════════════════════════ */

document.addEventListener("click", function(event) {

    const withdrawBtn = event.target.closest(".withdrawal-ticket-btn");
    if (withdrawBtn) {
        event.stopPropagation();
        handleTicketAction(withdrawBtn, {
            class: "btn btn-success btn-sm",
            html: '<i class="bi bi-check-lg"></i> برداشته شد',
            statusHTML: '<span class="status-dot bg-info"></span> در حال بررسی'
        });
        return;
    }

    const closeBtn = event.target.closest(".close-ticket-btn");
    if (closeBtn) {
        event.stopPropagation();
        handleTicketAction(closeBtn, {
            class: "btn btn-secondary btn-sm",
            html: '<i class="bi bi-check-lg"></i> بسته شد',
            statusHTML: '<span class="status-dot bg-danger"></span> بسته'
        });
    }

});

/* ═══════════════════════════════════════════════════════════════
   🔍 فیلتر جدول
═══════════════════════════════════════════════════════════════ */
function initializeTableFilter() {
    const table = document.getElementById("ticketTable");
    if (!table) return;

    const filters = table.querySelectorAll(".column-filter");
    filters.forEach(input => {
        input.addEventListener("input", filterTicketTable);
        input.addEventListener("change", filterTicketTable); // برای select ها
    });
}

function filterTicketTable() {
    const table = document.getElementById("ticketTable");
    if (!table) return;

    const filters = table.querySelectorAll(".column-filter");
    const rows = table.querySelectorAll("tbody tr");

    rows.forEach(row => {
        let show = true;

        filters.forEach(input => {
            const index = input.dataset.column;
            const value = input.value.trim().toLowerCase();

            if (!value) return;

            const cell = row.children[index];
            if (!cell) return;

            // اگر فیلتر ستون ۱ (عنوان تیکت) بود، هم متن سلول و هم محتوای مخفی را بررسی کن
            if (index === "1") {
                const cellText = cell.textContent.toLowerCase();
                const ticketBody = (row.dataset.content || "").toLowerCase();

                // اگر نه در عنوان بود و نه در محتوا، سطر مخفی شود
                if (!cellText.includes(value) && !ticketBody.includes(value)) {
                    show = false;
                }
            } else {
                // رفتار عادی برای بقیه ستون‌ها (شماره، اولویت، وضعیت، واحد و...)
                if (!cell.textContent.toLowerCase().includes(value)) {
                    show = false;
                }
            }
        });

        row.style.display = show ? "" : "none";
    });
}

/* ═══════════════════════════════════════════════════════════════
   🔄 دریافت مجدد جدول از سرور
═══════════════════════════════════════════════════════════════ */

function fetchNewTicketList() {
    const tbody = document.querySelector("#ticketTable tbody");

    fetch(window.location.href, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(r => r.text())
        .then(html => {
            const doc = new DOMParser().parseFromString(html, "text/html");
            const newBody = doc.querySelector("#ticketTable tbody");
            if (newBody && tbody) {
                tbody.innerHTML = newBody.innerHTML;
            }
        })
        .catch(() => location.reload());
}

/* ═══════════════════════════════════════════════════════════════
   📨 ارسال پیام
═══════════════════════════════════════════════════════════════ */

document.addEventListener("submit", function(event) {
    const form = event.target.closest("#sendMessageForm");
    if (!form) return;

    event.preventDefault();
    const formData = new FormData(form);

    fetch(form.action, {
            method: "POST",
            body: formData,
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(r => r.json())
        .then(data => {
            if (data.status !== "success") throw new Error(data.message);
            if (typeof showToast === "function") {
                showToast(data.message, "success");
            }
            form.reset();
            refreshMessagesHistory();
        })
        .catch(err => {
            if (typeof showToast === "function") {
                showToast(err.message, "danger");
            }
        });
});

/* ═══════════════════════════════════════════════════════════════
   💬 رفرش فقط تاریخچه پیام‌ها
═══════════════════════════════════════════════════════════════ */

function refreshMessagesHistory() {
    const container = document.getElementById("messagesHistory");
    if (!currentTicketDetailUrl || !container) return;

    fetch(currentTicketDetailUrl, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(r => r.text())
        .then(html => {
            const doc = new DOMParser().parseFromString(html, "text/html");
            const newMessages = doc.querySelector("#messagesHistory");
            if (newMessages) {
                container.innerHTML = newMessages.innerHTML;
            }
        });
}