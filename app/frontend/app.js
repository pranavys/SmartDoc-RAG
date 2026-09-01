let conversationId = null;


const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const chatBox = document.getElementById("chat-box");

const fileInput = document.getElementById("file-input");
const uploadButton = document.getElementById("upload-button");
const uploadStatus = document.getElementById("upload-status");


function addMessage(role, content) {
    const message = document.createElement("div");

    message.classList.add("message", role);
    message.textContent = content;

    chatBox.appendChild(message);

    chatBox.scrollTop = chatBox.scrollHeight;
}


uploadButton.addEventListener("click", async function () {

    const file = fileInput.files[0];

    if (!file) {
        uploadStatus.textContent = "Please select a PDF or DOCX file.";
        return;
    }

    const formData = new FormData();

    formData.append("file", file);

    uploadStatus.textContent = "Uploading and processing...";

    try {

        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });


        const data = await response.json();


        if (!response.ok) {
            throw new Error(data.detail || "Upload failed.");
        }


        uploadStatus.textContent = data.message;

        if (data.message === "Document uploaded and processed successfully.") {
            addMessage(
                "assistant",
                `Document "${data.filename}" is ready for questions.`
            );
        } else {
            addMessage(
                "assistant",
                `Document "${data.filename}" already exists and is ready for questions.`
            );
        }

        fileInput.value = "";

    } catch (error) {

        uploadStatus.textContent =
            error.message;

        console.error(error);
    }
});


chatForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    addMessage("user", message);

    messageInput.value = "";

    addMessage("assistant", "Thinking...");

    const thinkingMessage = chatBox.lastElementChild;

    try {

        const response = await fetch("/chat", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message,
                conversation_id: conversationId
            })
        });


        if (!response.ok) {
            throw new Error("Request failed.");
        }


        const data = await response.json();

        conversationId = data.conversation_id;

        thinkingMessage.textContent = data.answer;

    } catch (error) {

        thinkingMessage.textContent =
            "Sorry, something went wrong.";

        console.error(error);
    }
});