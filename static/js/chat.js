/*
========================================================
ParksideAI
Phase 5 Chat System
Scalable Section Architecture
========================================================
*/


/* ========================================================
   SECTION 1 — OFFICIAL LINKS
======================================================== */

const OFFICIAL_LINKS = {
    website: "https://parksidenj.com/",
    reservations: "https://www.opentable.com/r/parkside-tavern-morristown",
    privateEvents: "https://parksidetavern.tripleseat.com/party_request/45075",
    foodMenu: "https://parksidenj.com/morristown-morristown-parkside-tavern-food-menu",
    drinkMenu: "https://parksidenj.com/morristown-morristown-parkside-tavern-drink-menu"
};


/* ========================================================
   SECTION 2 — DOM ELEMENTS
======================================================== */

const chatWidget =
    document.getElementById(
        "parkside-chat-widget"
    );

const chatBody =
    document.getElementById(
        "parkside-chat-body"
    );

const chatMessages =
    document.getElementById(
        "chat-messages"
    );

const userInput =
    document.getElementById(
        "user-input"
    );

const sendButton =
    document.getElementById(
        "send-button"
    );

const openChatButton =
    document.getElementById(
        "open-chat"
    );

const minimizeButton =
    document.getElementById(
        "parkside-chat-toggle"
    );

const launcherButton =
    document.getElementById(
        "parkside-chat-launcher"
    );
/* ========================================================
   SECTION 3 — CHAT STATE
======================================================== */

const CHAT_STORAGE_KEYS = {

    minimized:
        "parkside_chat_minimized",

    session:
        "parkside_chat_session"
};


const CHAT_STATE = {

    isOpen: true,

    isSending: false,

    sessionId:
        getOrCreateSessionId(),

    conversationHistory: [],

    maxHistoryLength: 12,

    initialized: false
};

/* ========================================================
   SECTION 4 — INITIALIZATION
======================================================== */

document.addEventListener(
    "DOMContentLoaded",
    initializeChatSystem
);

function initializeChatSystem() {

    if (CHAT_STATE.initialized) {
        return;
    }

  bindCoreEvents();

restorePersistedChatState();

initializeWelcomeState();

    CHAT_STATE.initialized = true;
}


/* ========================================================
   SECTION 5 — EVENT BINDING
======================================================== */

function bindCoreEvents() {

    if (openChatButton) {

        openChatButton.addEventListener(
            "click",
            openChat
        );
    }

    if (minimizeButton) {

        minimizeButton.addEventListener(
            "click",
            minimizeChat
        );
    }

    if (launcherButton) {

        launcherButton.addEventListener(
            "click",
            maximizeChat
        );
    }

    if (sendButton) {

        sendButton.addEventListener(
            "click",
            handleSendMessage
        );
    }

    if (userInput) {

        userInput.addEventListener(
            "keydown",
            function(event) {

                if (event.key === "Enter") {

                    event.preventDefault();

                    handleSendMessage();
                }
            }
        );
    }
}

/* ========================================================
   SECTION 6 — CHAT OPEN/CLOSE
======================================================== */
/* ========================================================
   SECTION 6 — CHAT OPEN/CLOSE
======================================================== */

/* ========================================================
   SECTION 6 — FLOATING CHAT CONTROL
======================================================== */

function openChat() {

    maximizeChat();
}


function minimizeChat() {

    if (!chatWidget) {
        return;
    }

    chatWidget.classList.add(
        "minimized"
    );

    if (launcherButton) {

        launcherButton.classList.add(
            "visible"
        );
    }

    localStorage.setItem(
        CHAT_STORAGE_KEYS.minimized,
        "true"
    );
}


function maximizeChat() {

    if (!chatWidget) {
        return;
    }

    chatWidget.classList.remove(
        "minimized"
    );

    if (launcherButton) {

        launcherButton.classList.remove(
            "visible"
        );
    }

    localStorage.setItem(
        CHAT_STORAGE_KEYS.minimized,
        "false"
    );

    focusInput();

    scrollToBottom();
}


function restorePersistedChatState() {

    const minimized =
        localStorage.getItem(
            CHAT_STORAGE_KEYS.minimized
        );

    if (minimized === "true") {

        minimizeChat();

    } else {

        maximizeChat();
    }
}


function focusInput() {

    if (!userInput) {
        return;
    }

    setTimeout(() => {

        userInput.focus();

    }, 100);
}


/* ========================================================
   SECTION 7 — WELCOME STATE
======================================================== */

function initializeWelcomeState() {

    if (!chatMessages) {
        return;
    }

    if (chatMessages.children.length > 0) {
        return;
    }

    addBotMessage(
        "Welcome to ParksideAI. I can help route you to official Parkside Tavern information for reservations, menus, private events, brunch, drinks, and more."
    );

    renderPrimaryQuickActions();
}


/* ========================================================
   SECTION 8 — MESSAGE HANDLING
======================================================== */

async function handleSendMessage() {

    if (CHAT_STATE.isSending) {
        return;
    }

    const message =
        userInput.value.trim();

    if (!message) {
        return;
    }

    addUserMessage(message);

    addConversationEntry(
        "user",
        message
    );

    userInput.value = "";

    setLoadingState(true);

    const typingIndicator =
        addTypingIndicator();

    try {

        const payload =
            await sendMessageToBackend(message);

        removeElement(typingIndicator);

        processBackendResponse(payload);

    } catch (error) {

        console.error(
            "ParksideAI frontend error:",
            error
        );

        removeElement(typingIndicator);

        renderConnectionFailure();

    } finally {

        setLoadingState(false);
    }
}


/* ========================================================
   SECTION 9 — BACKEND REQUEST
======================================================== */

async function sendMessageToBackend(message) {

    const response = await fetch(
        "/chat/",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                message: message,

                session_id:
                    CHAT_STATE.sessionId,

                page_url:
                    window.location.href,

                conversation_history:
                    CHAT_STATE.conversationHistory
            })
        }
    );

    let data = {};

    try {

        data =
            await response.json();

    } catch (error) {

        throw new Error(
            "Invalid backend JSON response."
        );
    }

    if (!response.ok) {

        throw new Error(
            data.reply ||
            "Backend request failed."
        );
    }

    return data;
}


/* ========================================================
   SECTION 10 — RESPONSE PROCESSING
======================================================== */

function processBackendResponse(payload) {

    const reply =
        payload.reply ||
        getFallbackReply();

    addBotMessage(reply);

    addConversationEntry(
        "assistant",
        reply
    );

    handleIntentQuickActions(payload);
}


/* ========================================================
   SECTION 11 — QUICK ACTIONS
======================================================== */

function handleIntentQuickActions(payload) {

    const metadata =
        payload.metadata || {};

    const intent =
        metadata.intent || "";

    if (intent === "reservation") {

        addQuickActionButton(
            "Book on OpenTable",
            OFFICIAL_LINKS.reservations
        );

        return;
    }

    if (intent === "private_event") {

        addQuickActionButton(
            "Private Event Inquiry",
            OFFICIAL_LINKS.privateEvents
        );

        return;
    }

    if (intent === "menu") {

        addQuickActionButton(
            "View Food Menu",
            OFFICIAL_LINKS.foodMenu
        );

        return;
    }

    if (intent === "drinks") {

        addQuickActionButton(
            "View Drink Menu",
            OFFICIAL_LINKS.drinkMenu
        );

        return;
    }
}

function renderPrimaryQuickActions() {

    const wrapper =
        createQuickActionsWrapper();

    wrapper.appendChild(
        createQuickActionButton(
            "Reservations",
            OFFICIAL_LINKS.reservations
        )
    );

    wrapper.appendChild(
        createQuickActionButton(
            "Private Events",
            OFFICIAL_LINKS.privateEvents
        )
    );

    wrapper.appendChild(
        createQuickActionButton(
            "Food Menu",
            OFFICIAL_LINKS.foodMenu
        )
    );

    wrapper.appendChild(
        createQuickActionButton(
            "Drink Menu",
            OFFICIAL_LINKS.drinkMenu
        )
    );

    chatMessages.appendChild(wrapper);

    scrollToBottom();
}


/* ========================================================
   SECTION 12 — MESSAGE UI HELPERS
======================================================== */

function addUserMessage(message) {

    addMessage(
        message,
        "user-message"
    );
}

function addBotMessage(message) {

    addMessage(
        message,
        "bot-message"
    );
}

function addMessage(
    message,
    className
) {

    const messageElement =
        document.createElement("div");

    messageElement.classList.add(className);

    messageElement.innerText =
        message;

    chatMessages.appendChild(messageElement);

    scrollToBottom();

    return messageElement;
}

function addTypingIndicator() {

    const typingElement =
        document.createElement("div");

    typingElement.classList.add(
        "bot-message",
        "typing-indicator"
    );

    typingElement.innerText =
        "ParksideAI is thinking...";

    chatMessages.appendChild(typingElement);

    scrollToBottom();

    return typingElement;
}


/* ========================================================
   SECTION 13 — QUICK ACTION UI HELPERS
======================================================== */

function createQuickActionsWrapper() {

    const wrapper =
        document.createElement("div");

    wrapper.classList.add(
        "quick-actions"
    );

    return wrapper;
}

function createQuickActionButton(
    label,
    url
) {

    const button =
        document.createElement("a");

    button.classList.add(
        "quick-action-button"
    );

    button.href = url;

    button.target = "_blank";

    button.rel =
        "noopener noreferrer";

    button.innerText = label;

    return button;
}

function addQuickActionButton(
    label,
    url
) {

    const wrapper =
        createQuickActionsWrapper();

    wrapper.appendChild(
        createQuickActionButton(
            label,
            url
        )
    );

    chatMessages.appendChild(wrapper);

    scrollToBottom();
}


/* ========================================================
   SECTION 14 — CONVERSATION HISTORY
======================================================== */

function addConversationEntry(
    role,
    content
) {

    CHAT_STATE.conversationHistory.push({
        role,
        content
    });

    if (
        CHAT_STATE.conversationHistory.length >
        CHAT_STATE.maxHistoryLength
    ) {

        CHAT_STATE.conversationHistory =
            CHAT_STATE.conversationHistory.slice(
                -CHAT_STATE.maxHistoryLength
            );
    }
}


/* ========================================================
   SECTION 15 — LOADING STATES
======================================================== */

function setLoadingState(isLoading) {

    CHAT_STATE.isSending =
        isLoading;

    if (sendButton) {

        sendButton.disabled =
            isLoading;

        sendButton.innerText =
            isLoading
                ? "Sending..."
                : "Send";
    }

    if (userInput) {

        userInput.disabled =
            isLoading;
    }
}


/* ========================================================
   SECTION 16 — ERROR HANDLING
======================================================== */

function renderConnectionFailure() {

    addBotMessage(
        "I’m having trouble connecting right now. Please use the official Parkside Tavern links below."
    );

    renderPrimaryQuickActions();
}

function getFallbackReply() {

    return (
        "For official Parkside Tavern information, please visit " +
        OFFICIAL_LINKS.website
    );
}


/* ========================================================
   SECTION 17 — GENERAL HELPERS
======================================================== */

function scrollToBottom() {

    if (!chatMessages) {
        return;
    }

    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}

function removeElement(element) {

    if (
        element &&
        element.parentNode
    ) {

        element.parentNode.removeChild(
            element
        );
    }
}

/* ========================================================
   SECTION 18 — SESSION STORAGE
======================================================== */

function getOrCreateSessionId() {

    const existingSession =
        localStorage.getItem(
            CHAT_STORAGE_KEYS.session
        );

    if (existingSession) {
        return existingSession;
    }

    const newSessionId =
        "parkside_" +
        Date.now() +
        "_" +
        Math.random()
            .toString(36)
            .substring(2, 10);

    localStorage.setItem(
        CHAT_STORAGE_KEYS.session,
        newSessionId
    );

    return newSessionId;
}