/*
    Course Name: CMSC495 7384
    Author: Eric Thomas
    Group: A
    Date: Nov 23'
    Project: CMSC495 Secure Chat Server
    Platform: Debian Linux

    Description:
    This JavaScript file contains client-side code for the Secure Chat Server home page.
    It handles interactions with the SSH and encryption switches, shows confirmation dialogs,
    and sends requests to the server to update the switches.
*/

// Function to update the SSH switch state
function updateSSH() {
    const sshSwitch = document.getElementById('ssh-switch');
    const newSSHStatus = sshSwitch.checked;
    // Send a request to the server to update SSH switch
    fetch('/update_ssh', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ssh_enabled: newSSHStatus }),
    });
}

// Function to update the Encryption switch state
function updateEncryption() {
    const encryptionSwitch = document.getElementById('encryption-switch');
    const newEncryptionStatus = encryptionSwitch.checked;
    // Send a request to the server to update Encryption switch
    fetch('/update_encryption', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ encryption_enabled: newEncryptionStatus }),
    });
}

// Event listener to execute updateSSH and updateEncryption when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const sshSwitch = document.getElementById('ssh-switch');
    sshSwitch.addEventListener('change', updateSSH);

    const encryptionSwitch = document.getElementById('encryption-switch');
    encryptionSwitch.addEventListener('change', updateEncryption);
});

