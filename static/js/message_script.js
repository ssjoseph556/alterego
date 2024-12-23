async function sendMessage() {
    const userInput = document.getElementById("user-input");
    const chatWindow = document.getElementById("chat-window");

    const userMessage = userInput.value;
    if (!userMessage) return;

    // Display user message
    chatWindow.innerHTML += `<p><strong>You:</strong> ${userMessage}</p>`;

    // Send message to the backend
    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
    });

    const data = await response.json();

    try {
        const req = await fetch('/get_customizations');
        if (!req.ok) {
            throw new Error('Network response was not ok');
        }
        const customizations = await req.json();
        const choices = customizations["choices"]
        const bot_name = choices["name"].toString()
        chatWindow.innerHTML += `<p><strong>${bot_name}:</strong> ${data.reply}</p>`;
        chatWindow.scrollTop = chatWindow.scrollHeight;  // Auto-scroll to the bottom
        userInput.value = "";
    } catch (error) {
        console.error('Error fetching customizations:', error);
    }
}

async function fetchCustomizations() {

}



