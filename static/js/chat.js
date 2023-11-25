/*
    Course Name: CMSC495 7384
    Author: Eric Thomas
    Group: A
    Date: Nov 23'
    Project: CMSC495 Secure Chat Server
    Platform: Debian Linux

    Description:
    This JavaScript file contains client-side code for the Secure Chat Server chat page.
    It handles message input and message database display.
*/



// Retrieve the encryption key from sessionStorage
var encryptionKey = sessionStorage.getItem("encryptionKey");

// Check if encryptionKey exists
if (encryptionKey) {
    // Create a new paragraph element
    var para = document.createElement("p");
    para.textContent = "Encryption Key: " + encryptionKey;

    // Append the paragraph to the div with id 'encryptionKeyDisplay'
    document.getElementById("encryptionKeyDisplay").appendChild(para);
} else {

    // If encryptionKey doesn't exist, display a message
    var msg = "No encryption key found. This is a result of navigating to a new window. " +
        "You must login again at the user actions page.";
    document.getElementById("encryptionKeyDisplay").textContent = msg;
}

var username = document.body ? document.body.getAttribute("data-username") : null;

// Check if username exists
if (username) {
    // Create a new paragraph element
    var para = document.createElement("p");
    para.textContent = "Username: " + username;

    // Append the paragraph to the div with id 'usernameDisplay'
    document.getElementById("usernameDisplay").appendChild(para);
} else {

    // If username doesn't exist, display a message
    var msg = "No username found.";
    document.getElementById("usernameDisplay").textContent = msg;
}


function sendMessage() {
    var messageContent = document.getElementById("messageInput").value;

    // Send the message content to the server
    fetch('/submit_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: username, message_content: messageContent })
    })
        // Get the response from flask if available
        .then(response => response.json())

        // If successful print to console and reset input box, else error to console
        .then(data => {
            if (data.success) {
                console.log("Message sent successfully");
                document.getElementById("messageInput").value = '';
                refreshChat();
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function refreshChat() {
    fetch('/get_messages')
        .then(response => response.json())
        .then(messages => {
            // Display the messages
            var messageContainer = document.getElementById("messageContainer");
            // Clear existing messages from container
            messageContainer.innerHTML = '';

            messages.forEach((msg, index) => {
                // Create a message element with a class based on the user
                var messageElement = document.createElement("div");
                messageElement.classList.add("message", `user${index % 3 + 1}`);

                // Create user info element (username and date)
                var userInfoElement = document.createElement("div");
                userInfoElement.classList.add("user-info");
                userInfoElement.textContent = `${msg.user_id} (${msg.timestamp})`;

                // Create message content element
                var messageContentElement = document.createElement("div");
                messageContentElement.textContent = msg.message;

                // Append user info and message content to message element
                messageElement.appendChild(userInfoElement);
                messageElement.appendChild(messageContentElement);

                // Append message element to message container
                messageContainer.appendChild(messageElement);
            });

            // Scroll to the bottom of the messages container
            messageContainer.scrollTop = messageContainer.scrollHeight;
        });
}

// Refresh on page load
refreshChat();

// Refresh chat messages every 3 seconds
setInterval(refreshChat, 3000);



