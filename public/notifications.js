(function () {
  const STYLE_ID = "tracecrop-notification-styles";
  const CONTAINER_ID = "tracecrop-notification-container";
  const TRANSLATOR_LANGUAGE_CODES = new Set([
    "",
    "en",
    "bn",
    "gu",
    "hi",
    "kn",
    "ml",
    "mr",
    "ne",
    "pa",
    "ta",
    "te",
    "ur"
  ]);
  const TRANSLATOR_LANGUAGE_NAMES = new Set([
    "select language",
    "english",
    "bengali",
    "gujarati",
    "hindi",
    "kannada",
    "malayalam",
    "marathi",
    "nepali",
    "punjabi",
    "tamil",
    "telugu",
    "urdu"
  ]);

  function ensureStyles() {
    if (document.getElementById(STYLE_ID)) return;

    const style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent = `
      @keyframes tracecropToastIn {
        from { opacity: 0; transform: translateY(14px) scale(0.96); }
        to { opacity: 1; transform: translateY(0) scale(1); }
      }
      @keyframes tracecropToastOut {
        from { opacity: 1; transform: translateY(0) scale(1); }
        to { opacity: 0; transform: translateY(10px) scale(0.98); }
      }
      @keyframes tracecropToastPulse {
        0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(78, 222, 163, 0.35); }
        50% { transform: scale(1.05); box-shadow: 0 0 0 10px rgba(78, 222, 163, 0); }
      }
      #${CONTAINER_ID} {
        position: fixed;
        right: 24px;
        bottom: 24px;
        z-index: 5000;
        display: flex;
        flex-direction: column;
        gap: 10px;
        pointer-events: none;
      }
      .tracecrop-toast {
        width: min(380px, calc(100vw - 32px));
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 14px 16px;
        border-radius: 12px;
        border: 1px solid rgba(78, 222, 163, 0.35);
        background: rgba(18, 33, 49, 0.96);
        color: #d4e4fa;
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.38);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        pointer-events: auto;
        animation: tracecropToastIn 260ms cubic-bezier(0.19, 1, 0.22, 1) forwards;
      }
      .tracecrop-toast.is-hiding {
        animation: tracecropToastOut 220ms ease-in forwards;
      }
      .tracecrop-toast-icon {
        width: 38px;
        height: 38px;
        border-radius: 999px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        color: #4edea3;
        background: rgba(78, 222, 163, 0.12);
        border: 1px solid rgba(78, 222, 163, 0.35);
        animation: tracecropToastPulse 1200ms ease-out infinite;
      }
      .tracecrop-toast-title {
        margin: 0;
        font: 700 13px/18px Geist, Inter, system-ui, sans-serif;
        color: #d4e4fa;
      }
      .tracecrop-toast-message {
        margin: 1px 0 0;
        font: 500 12px/17px Geist, Inter, system-ui, sans-serif;
        color: rgba(212, 228, 250, 0.74);
        white-space: pre-line;
        overflow-wrap: anywhere;
      }
      @media (max-width: 640px) {
        #${CONTAINER_ID} {
          left: 16px;
          right: 16px;
          bottom: 76px;
        }
        .tracecrop-toast {
          width: 100%;
        }
      }
      #google_translate_element {
        display: flex !important;
        align-items: center;
        gap: 8px;
      }
      #google_translate_element::before {
        content: "Language";
        color: #4edea3;
        font: 700 10px/1 Geist, Inter, system-ui, sans-serif;
        text-transform: uppercase;
      }
      #google_translate_element select,
      #google_translate_element .goog-te-combo {
        width: auto !important;
        max-width: 150px;
        min-height: 28px;
        margin: 0 !important;
        padding: 4px 8px !important;
        border-radius: 8px !important;
        border: 1px solid rgba(212, 228, 250, 0.16) !important;
        background: rgba(5, 20, 36, 0.8) !important;
        color: #d4e4fa !important;
        font: 600 12px/1 Geist, Inter, system-ui, sans-serif !important;
        outline: none !important;
      }
      #google_translate_element span,
      #google_translate_element a {
        color: rgba(212, 228, 250, 0.55) !important;
        font-size: 10px !important;
      }
      #google_translate_element .goog-logo-link,
      #google_translate_element .goog-te-gadget > span {
        display: none !important;
      }
      #google_translate_element .goog-te-gadget {
        color: transparent !important;
        font-size: 0 !important;
      }
      @media (max-width: 640px) {
        #google_translate_element::before {
          display: none;
        }
        #google_translate_element select,
        #google_translate_element .goog-te-combo {
          max-width: 180px;
        }
      }
    `;
    document.head.appendChild(style);
  }

  function ensureContainer() {
    let container = document.getElementById(CONTAINER_ID);
    if (container) return container;

    container = document.createElement("div");
    container.id = CONTAINER_ID;
    document.body.appendChild(container);
    return container;
  }

  function showNotification(message, options = {}) {
    const run = () => {
      ensureStyles();
      const container = ensureContainer();
      const toast = document.createElement("div");
      const title = options.title || "TraceCrop";
      const duration = options.duration || 3200;

      toast.className = "tracecrop-toast";
      toast.innerHTML = `
        <div class="tracecrop-toast-icon">
          <span class="material-symbols-outlined" style="font-size: 22px;">notifications</span>
        </div>
        <div>
          <p class="tracecrop-toast-title"></p>
          <p class="tracecrop-toast-message"></p>
        </div>
      `;

      toast.querySelector(".tracecrop-toast-title").textContent = title;
      toast.querySelector(".tracecrop-toast-message").textContent = String(message || "");
      container.appendChild(toast);

      setTimeout(() => {
        toast.classList.add("is-hiding");
        toast.addEventListener("animationend", () => toast.remove(), { once: true });
      }, duration);
    };

    if (document.body) run();
    else window.addEventListener("DOMContentLoaded", run, { once: true });
  }

  function isAllowedTranslatorOption(option) {
    const value = String(option.value || "").trim().toLowerCase();
    const label = String(option.textContent || "").trim().toLowerCase();

    if (TRANSLATOR_LANGUAGE_CODES.has(value)) return true;
    if (TRANSLATOR_LANGUAGE_NAMES.has(label)) return true;
    return false;
  }

  function filterTranslatorLanguages() {
    const combo = document.querySelector("#google_translate_element select.goog-te-combo, .goog-te-combo");
    if (!combo) return false;

    Array.from(combo.options).forEach((option) => {
      if (!isAllowedTranslatorOption(option)) option.remove();
    });

    if (!isAllowedTranslatorOption(combo.options[combo.selectedIndex] || combo.options[0])) {
      combo.value = "";
    }

    combo.setAttribute("data-tracecrop-indian-languages", "true");
    return true;
  }

  function startTranslatorLanguageFilter() {
    let attempts = 0;
    const maxAttempts = 80;

    const timer = window.setInterval(() => {
      attempts += 1;
      const didFilter = filterTranslatorLanguages();
      if (didFilter || attempts >= maxAttempts) window.clearInterval(timer);
    }, 250);

    const observer = new MutationObserver(() => filterTranslatorLanguages());
    const watch = () => {
      const element = document.getElementById("google_translate_element");
      if (element) observer.observe(element, { childList: true, subtree: true });
    };

    if (document.body) watch();
    else window.addEventListener("DOMContentLoaded", watch, { once: true });
  }

  ensureStyles();
  startTranslatorLanguageFilter();
  window.showTraceCropNotification = showNotification;
  window.alert = function (message) {
    showNotification(message, { title: "Notification" });
  };
})();
