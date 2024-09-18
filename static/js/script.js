document.getElementById('send-btn').addEventListener('click', function() {
    let userInput = document.getElementById('user-input').value;

    if (userInput.trim() === '') {
        return;
    }

    // Add user message to chat box
    addUserMessage(userInput);

    // Send user input to Flask for response
    fetch('/get_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        botResponse(data.response);
    });

    // Clear input
    document.getElementById('user-input').value = '';
});

function addUserMessage(message) {
    let chatBox = document.getElementById('chat-box');
    let userMessageDiv = document.createElement('div');
    userMessageDiv.classList.add('user-message');
    userMessageDiv.innerText = message;
    chatBox.appendChild(userMessageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function botResponse(response) {
    let chatBox = document.getElementById('chat-box');
    let botMessageDiv = document.createElement('div');
    botMessageDiv.classList.add('bot-message');
    botMessageDiv.innerText = response;
    chatBox.appendChild(botMessageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
