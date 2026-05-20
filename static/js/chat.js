const openChatButton = document.getElementById("open-chat");
const chatContainer = document.getElementById("chat-container");

const sendButton = document.getElementById("send-button");
const userInput = document.getElementById("user-input");

const chatMessages = document.getElementById("chat-messages");


openChatButton.addEventListener("click", () => {
    chatContainer.style.display = "flex";
});


sendButton.addEventListener("click", async () => {

    const message = userInput.value;

    if (message.trim() === "") return;

    addMessage(message, "user-message");

    userInput.value = "";

    const response = await fetch("/chat/", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: message
        })
    });

    const data = await response.json();

    addMessage(data.reply, "bot-message");

});


function addMessage(message, className) {

    const div = document.createElement("div");

    div.classList.add(className);

    div.innerText = message;

    chatMessages.appendChild(div);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}