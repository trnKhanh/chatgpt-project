messageBox = document.querySelector(".message-box");
inputBox = document.querySelector(".input-box");
formSelect = document.querySelector(".form-select");
form = document.querySelector("form");
micButton = document.querySelector(".mic-btn");
mic_on = false;
speakButton = document.querySelector(".speak-btn");
speak_on = false;
let utterance = new SpeechSynthesisUtterance();
utterance.rate = 1;
utterance.volume = 100;
speechSynthesis.addEventListener("voiceschanged", () => {
    let voices = speechSynthesis.getVoices();
    utterance.voice = voices.find(voice => voice.name === "Google US English");
});

if (navigator.mediaDevices.getUserMedia)
{
    let onSuccess = function(stream)
    {
        mediaRecorder = new MediaRecorder(stream, {mimeType: "audio/webm;codecs=opus"});
        micButton.addEventListener("click",(e) => {
            if (mic_on == false)
            {
                micButton.classList.remove("off-btn");
                micButton.classList.add("on-btn");
                mediaRecorder.start();
            }
            else
            {
                micButton.classList.remove("on-btn");
                micButton.classList.add("off-btn");
                mediaRecorder.stop();
            }
            mic_on = !mic_on;
        })
        let chunks = [];
        mediaRecorder.ondataavailable = async function(e){
            chunks.push(e.data);
        };
        mediaRecorder.onstop = async function(e){
            console.log(mediaRecorder.mimeType);
            let blob = new Blob(chunks, {type: mediaRecorder.mimeType});
            chunks = []
            let formData = new FormData();
            formData.append("audio_file", blob);
            response = await fetch("/whisper",{
                method: "POST",
                body: formData,
            }).then((re) => re.json());
            console.log(response);
            inputBox.value += response;
        };
    }
    let onError = function(stream)
    {
        console.log("Error");
    }
    navigator.mediaDevices.getUserMedia({audio: true}).then(onSuccess, onError);
}
speakButton.addEventListener("click",(e) => {
    if (speak_on == false)
    {
        speakButton.classList.remove("off-btn");
        speakButton.classList.add("on-btn");
    }
    else
    {
        speakButton.classList.remove("on-btn");
        speakButton.classList.add("off-btn");
    }
    speak_on = !speak_on;
})
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = inputBox.value;
    const chatbotType = formSelect.value;

    messageBox.innerHTML += `<div class="user-message">User: ${message}</div>`;

    const response = await fetch(`/response`, {
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
    utterance.text = response;
    if (speak_on) speechSynthesis.speak(utterance);
    inputBox.value = "";
})