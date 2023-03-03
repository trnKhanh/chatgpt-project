messageBox = document.querySelector("#message-box")
inputBox = document.querySelector("#input-box")
form = document.querySelector("form")

form.addEventListener("submit",async (e) => {
    e.preventDefault();

    const message = inputBox.value;

    messageBox.innerHTML += `<li>User: ${message}</li>`;

    const response = await fetch("/completion", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            message: message,
        }),
    }).then((response) => response.json());

    messageBox.innerHTML += `<li>Chatbot: ${response}</li>`;
    inputBox.value = "";
})