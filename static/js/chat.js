/*
    ParksideAI Frontend Styles
    Phase 3 Upgrade

    Goals:
    - Production-ready visual polish
    - Hospitality-forward brand feel
    - Responsive chat UI
    - Clear official routing buttons
    - Better mobile support
    - Better loading/error states
*/


/* ============================================================
   1. ROOT VARIABLES
   ============================================================ */

:root {
    --bg-main: #0b0f14;
    --bg-panel: #111827;
    --bg-panel-soft: #17202c;
    --bg-card: #1f2937;

    --text-main: #f9fafb;
    --text-muted: #cbd5e1;
    --text-soft: #94a3b8;

    --brand-primary: #c59b5f;
    --brand-primary-dark: #9f7a43;
    --brand-blue: #2563eb;
    --brand-blue-dark: #1d4ed8;

    --border-soft: rgba(255, 255, 255, 0.12);
    --shadow-large: 0 24px 80px rgba(0, 0, 0, 0.55);
    --shadow-medium: 0 14px 40px rgba(0, 0, 0, 0.35);

    --radius-small: 8px;
    --radius-medium: 14px;
    --radius-large: 24px;

    --font-main: Arial, Helvetica, sans-serif;

    --chat-width: 390px;
    --chat-height: 580px;
}


/* ============================================================
   2. GLOBAL RESET
   ============================================================ */

* {
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    margin: 0;
    min-height: 100vh;
    font-family: var(--font-main);
    background:
        radial-gradient(circle at top left, rgba(197, 155, 95, 0.16), transparent 34%),
        radial-gradient(circle at bottom right, rgba(37, 99, 235, 0.16), transparent 32%),
        linear-gradient(135deg, #05070a 0%, var(--bg-main) 45%, #111827 100%);
    color: var(--text-main);
}


/* ============================================================
   3. MAIN HERO SECTION
   ============================================================ */

.hero {
    min-height: 100vh;
    width: 100%;
    padding: 80px 24px 120px;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    text-align: center;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: "";
    position: absolute;
    width: 520px;
    height: 520px;
    border-radius: 50%;
    background: rgba(197, 155, 95, 0.08);
    top: -160px;
    right: -140px;
    filter: blur(4px);
}

.hero::after {
    content: "";
    position: absolute;
    width: 420px;
    height: 420px;
    border-radius: 50%;
    background: rgba(37, 99, 235, 0.08);
    bottom: -120px;
    left: -100px;
    filter: blur(4px);
}

.hero h1 {
    position: relative;
    z-index: 1;

    margin: 0 0 16px;
    font-size: clamp(3rem, 8vw, 6.5rem);
    line-height: 0.95;
    letter-spacing: -0.06em;

    background: linear-gradient(135deg, #ffffff 0%, #f1d5a5 52%, #c59b5f 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.hero p {
    position: relative;
    z-index: 1;

    max-width: 720px;
    margin: 0 auto 22px;
    font-size: clamp(1.05rem, 2vw, 1.35rem);
    line-height: 1.6;
    color: var(--text-muted);
}

.hero .subtext {
    max-width: 640px;
    font-size: 0.98rem;
    color: var(--text-soft);
}


/* ============================================================
   4. BUTTONS
   ============================================================ */

button,
.button-like {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;

    min-height: 44px;
    padding: 12px 20px;

    border: none;
    border-radius: 999px;

    cursor: pointer;
    font-weight: 700;
    font-size: 0.95rem;
    text-decoration: none;

    background: linear-gradient(135deg, var(--brand-primary), #e6c98d);
    color: #111827;

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease,
        opacity 0.18s ease,
        background 0.18s ease;
}

button:hover,
.button-like:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 28px rgba(197, 155, 95, 0.26);
}

button:active,
.button-like:active {
    transform: translateY(0);
}

button:disabled {
    cursor: not-allowed;
    opacity: 0.65;
    transform: none;
    box-shadow: none;
}


/* ============================================================
   5. CHAT CONTAINER
   ============================================================ */

.chat-container {
    position: fixed;
    right: 24px;
    bottom: 24px;
    z-index: 50;

    width: var(--chat-width);
    height: var(--chat-height);
    max-height: calc(100vh - 48px);

    display: none;
    flex-direction: column;

    overflow: hidden;

    background:
        linear-gradient(180deg, rgba(31, 41, 55, 0.98), rgba(15, 23, 42, 0.98));
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-large);

    box-shadow: var(--shadow-large);
    backdrop-filter: blur(14px);
}


/* ============================================================
   6. CHAT HEADER
   ============================================================ */

.chat-header {
    padding: 16px 18px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    background:
        linear-gradient(135deg, rgba(197, 155, 95, 0.24), rgba(37, 99, 235, 0.18));
    border-bottom: 1px solid var(--border-soft);

    font-weight: 800;
    letter-spacing: -0.01em;
}

.chat-header::after {
    content: "Official routing assistant";
    display: block;
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--text-muted);
}


/* ============================================================
   7. CHAT MESSAGES
   ============================================================ */

.chat-messages {
    flex: 1;
    padding: 16px;

    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: rgba(197, 155, 95, 0.5) transparent;
}

.chat-messages::-webkit-scrollbar {
    width: 8px;
}

.chat-messages::-webkit-scrollbar-track {
    background: transparent;
}

.chat-messages::-webkit-scrollbar-thumb {
    background: rgba(197, 155, 95, 0.35);
    border-radius: 999px;
}

.bot-message,
.user-message {
    width: fit-content;
    max-width: 88%;

    margin-bottom: 14px;
    padding: 11px 13px;

    border-radius: 16px;
    line-height: 1.45;
    font-size: 0.94rem;

    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

.bot-message {
    margin-right: auto;
    background: rgba(55, 65, 81, 0.92);
    color: var(--text-main);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-bottom-left-radius: 6px;
}

.user-message {
    margin-left: auto;
    background: linear-gradient(135deg, var(--brand-blue), var(--brand-blue-dark));
    color: white;
    border-bottom-right-radius: 6px;
}

.typing-indicator {
    color: var(--text-muted);
    font-style: italic;
    animation: pulseText 1.25s ease-in-out infinite;
}

@keyframes pulseText {
    0% {
        opacity: 0.55;
    }

    50% {
        opacity: 1;
    }

    100% {
        opacity: 0.55;
    }
}


/* ============================================================
   8. QUICK ACTION BUTTONS
   ============================================================ */

.quick-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;

    margin: 2px 0 14px;
}

.quick-action-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;

    padding: 9px 12px;

    border-radius: 999px;
    border: 1px solid rgba(197, 155, 95, 0.45);

    background: rgba(197, 155, 95, 0.12);
    color: #f5d69a;

    text-decoration: none;
    font-size: 0.82rem;
    font-weight: 700;

    transition:
        background 0.18s ease,
        transform 0.18s ease,
        border-color 0.18s ease;
}

.quick-action-button:hover {
    background: rgba(197, 155, 95, 0.22);
    border-color: rgba(197, 155, 95, 0.78);
    transform: translateY(-1px);
}


/* ============================================================
   9. CHAT INPUT AREA
   ============================================================ */

.chat-input-area {
    display: flex;
    gap: 10px;

    padding: 12px;

    background: rgba(3, 7, 18, 0.78);
    border-top: 1px solid var(--border-soft);
}

.chat-input-area input {
    flex: 1;
    min-width: 0;

    padding: 12px 13px;

    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 999px;

    outline: none;
    background: rgba(255, 255, 255, 0.08);
    color: var(--text-main);

    font-size: 0.92rem;
}

.chat-input-area input::placeholder {
    color: var(--text-soft);
}

.chat-input-area input:focus {
    border-color: rgba(197, 155, 95, 0.75);
    box-shadow: 0 0 0 3px rgba(197, 155, 95, 0.14);
}

.chat-input-area button {
    min-width: 78px;
    margin: 0;
    padding: 10px 14px;
}


/* ============================================================
   10. PRIVACY / ROUTING NOTE
   ============================================================ */

.chat-container::after {
    content: "ParksideAI routes guests to official Parkside Tavern links and does not take reservations directly.";
    display: block;

    padding: 8px 14px 11px;

    background: rgba(3, 7, 18, 0.86);
    border-top: 1px solid rgba(255, 255, 255, 0.06);

    color: var(--text-soft);
    font-size: 0.68rem;
    line-height: 1.35;
    text-align: center;
}


/* ============================================================
   11. RESPONSIVE DESIGN
   ============================================================ */

@media (max-width: 720px) {
    .hero {
        padding: 64px 18px 110px;
    }

    .hero h1 {
        font-size: clamp(3rem, 16vw, 4.8rem);
    }

    .hero p {
        font-size: 1rem;
    }

    .chat-container {
        right: 12px;
        bottom: 12px;

        width: calc(100vw - 24px);
        height: min(620px, calc(100vh - 24px));

        border-radius: 20px;
    }

    .bot-message,
    .user-message {
        max-width: 92%;
        font-size: 0.92rem;
    }

    .quick-actions {
        flex-direction: column;
        align-items: stretch;
    }

    .quick-action-button {
        width: 100%;
    }
}


@media (max-width: 420px) {
    .chat-input-area {
        gap: 7px;
    }

    .chat-input-area button {
        min-width: 68px;
        padding: 10px 12px;
    }

    .chat-header {
        font-size: 0.92rem;
    }

    .chat-header::after {
        font-size: 0.66rem;
    }
}


/* ============================================================
   12. ACCESSIBILITY
   ============================================================ */

@media (prefers-reduced-motion: reduce) {
    * {
        scroll-behavior: auto !important;
        transition: none !important;
        animation: none !important;
    }
}

button:focus-visible,
.quick-action-button:focus-visible,
.chat-input-area input:focus-visible {
    outline: 3px solid rgba(197, 155, 95, 0.55);
    outline-offset: 2px;
}