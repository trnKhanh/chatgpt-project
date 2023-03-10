let form = document.querySelector("form");
let inputBox = document.querySelector(".input-classify-box")
let answerBox = document.querySelector(".answer-box")
form.addEventListener("submit", async (e) => {
    answerBox.classList.remove(`${answerBox.innerHTML}-box`);
    answerBox.innerHTML = "Loading...";
    e.preventDefault();
    let classify = await fetch("/classify", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            text: inputBox.value,
        })
    }).then((re) => re.json());
    classify = classify.trim();
    answerBox.innerHTML = classify;
    answerBox.classList.add(`${classify}-box`);
});