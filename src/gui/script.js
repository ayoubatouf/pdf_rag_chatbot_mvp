document.getElementById('userInput').addEventListener('keydown', function(event) {
  if (event.key === 'Enter') {
    event.preventDefault(); 
    sendMessage(); 
  }
});

function sendMessage() {
  const userInput = document.getElementById('userInput').value;

  if (userInput.trim() !== "") {
    displayMessage(userInput, 'user');
    document.getElementById('userInput').value = "";
    getBotResponse(userInput);
  }
}

function displayMessage(message, sender) {
  
  const messageContainer = document.createElement('div');
  messageContainer.classList.add('message-container', `${sender}-message`);

  if (sender === 'bot') {
    const avatar = document.createElement('img');
    avatar.classList.add('avatar');
    avatar.src = 'assets/image.png'; 
    avatar.alt = 'Bot Avatar';
    messageContainer.appendChild(avatar);
  }

  const messageDiv = document.createElement('div');
  messageDiv.classList.add('chat-message');

  const messageText = document.createElement('span');
  messageText.innerText = message;
  messageDiv.appendChild(messageText);

  messageContainer.appendChild(messageDiv);

  const chatBox = document.getElementById('chatBox');
  chatBox.appendChild(messageContainer);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function getBotResponse(userInput) {
  fetch('http://127.0.0.1:8000/chat/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query: userInput }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.response) {
        displayMessage(data.response, 'bot');
      } else if (data.error) {
        displayMessage(data.error, 'bot');
      }
    })
    .catch((error) => {
      displayMessage("Sorry, there was an error connecting to the server.", 'bot');
      console.error('Error:', error);
    });
}
