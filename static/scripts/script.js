let micOn = true; // Initial state of the microphone
let cameraOn = true; // Initial state of the camera

function toggleMic() {
    const toggleButton = document.getElementById("toggle-mic");
    if (micOn) {
        // Turn off microphone
        toggleButton.classList.add("off");
        toggleButton.textContent = "Mic";
    } else {
        // Turn on microphone
        toggleButton.classList.remove("off");
        toggleButton.textContent = "Mic";
    }
    micOn = !micOn; // Toggle microphone state
}

function toggleCamera() {
    const toggleButton = document.getElementById("toggle-camera");
    if (cameraOn) {
        // Turn off camera
        toggleButton.classList.add("off");
        toggleButton.textContent = "Camera";
    } else {
        // Turn on camera
        toggleButton.classList.remove("off");
        toggleButton.textContent = "Camera";
    }
    cameraOn = !cameraOn; // Toggle camera state
}


function displayChatHistory(history) {
    $('#chat-container').empty();
    history.forEach(function(message) {
        $('#chat-container').append('<p>' + message.role + ': ' + message.content + '</p>');
    });
    // startAudio();
}


function checkFileSelected() {
    var fileInput = document.getElementById('resume');
    if (fileInput.files.length === 0) {
        alert('Please select a file.');
        return false; // Prevent form submission
    }
    return true; // Allow form submission
}


