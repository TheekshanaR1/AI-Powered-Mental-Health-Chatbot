const API_URL = "http://127.0.0.1:8001/chat"; // Local FastAPI endpoint

const session_id = "user_" + Math.floor(Math.random() * 10000); // Temporary user session

function toggleChat() {
    const chat = document.getElementById("chatContainer");
    chat.style.display = chat.style.display === "flex" ? "none" : "flex";
}

function appendMessage(role, text) {
    const box = document.getElementById("chatBox");

    const msg = document.createElement("div");
    msg.innerHTML = `<strong>${role}:</strong> ${text}`;

    box.appendChild(msg);
    box.scrollTop = box.scrollHeight; // Auto scroll
}
async function sendMessage() {
    const input = document.getElementById("userInput");
    const text = input.value.trim();

    if (!text) return;

    appendMessage("You", text);
    input.value = "";

    try {
        const res = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                session_id: session_id,
                query: text
            })
        });

        const data = await res.json();
        appendMessage("Bot", data.response);

    } catch (error) {
        appendMessage("Bot", "Error connecting to server.");
        console.error(error);
    }
}
