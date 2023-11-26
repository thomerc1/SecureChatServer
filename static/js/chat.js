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

// Check if encryptionKey exists and log it to the console
if (encryptionKey) {
    console.log("Encryption Key:", encryptionKey);
} else {
    console.log("No encryption key found.");
}

var username = document.body ? document.body.getAttribute("data-username") : null;
// Sets var to false unles it matches the string
var encryptionEnabled = document.body.getAttribute("data-encryption-enabled") === 'True'; 

// Log username and encryptionEnabled to the console
console.log("Username:", username);
console.log("Encryption Enabled:", encryptionEnabled);

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

// Function from https://github.com/brix/crypto-js
function encryptMessage(message) {
    return CryptoJS.AES.encrypt(message, encryptionKey).toString();
}

// Function from https://github.com/brix/crypto-js
function decryptMessage(encryptedMessage) {
    const bytes = CryptoJS.AES.decrypt(encryptedMessage, encryptionKey);
    return bytes.toString(CryptoJS.enc.Utf8);
}

function sendMessage() {
    var messageContent = document.getElementById("messageInput").value;

    // Encrypt if encryption enabled and a key is provided
    if (encryptionEnabled && encryptionKey){
        messageContent = encryptMessage(messageContent)
    }

    // Send the message content to the server
    fetch('/submit_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: username, message_content: messageContent, message_encrypted: encryptionEnabled })
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
                var messageText = msg.message;
                var messageEnc = msg.encrypted === true

                // If the database message attribute states it has an encrypted message and the decryption key is available
                if (messageEnc) {
                    try {
                        messageText = decryptMessage(messageText);
                    } catch (error) {
                        console.error('Error decrypting message:', error);
                        messageText = "Error decrypting message";
                    }
                }
                else{
                    console.log('Decrypting:', 'False');
                }

                // Create a message element with a class based on the user
                var messageElement = document.createElement("div");
                messageElement.classList.add("message", `user${index % 3 + 1}`);

                // Create user info element (username and date)
                var userInfoElement = document.createElement("div");
                userInfoElement.classList.add("user-info");
                userInfoElement.textContent = `${msg.user_id} (${msg.timestamp})`;

                // Create message content element
                var messageContentElement = document.createElement("div");
                messageContentElement.textContent = messageText;

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

