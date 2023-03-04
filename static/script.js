messageBox = document.querySelector(".message-box");
inputBox = document.querySelector(".input-box");
formSelect = document.querySelector(".form-select");
form = document.querySelector("form");

form.addEventListener("submit",async (e) => {
    e.preventDefault();
    const message = inputBox.value;
    const chatbotType = formSelect.value;

    messageBox.innerHTML += `<div class="user-message">User: ${message}</div>`;

    const response = await fetch(`/completion`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            message: message,
            type: chatbotType,
        }),
    }).then((response) => response.json());

    messageBox.innerHTML += `<div class="chatbot-message">Chatbot: ${response}</div>`;
    inputBox.value = "";
})