
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


