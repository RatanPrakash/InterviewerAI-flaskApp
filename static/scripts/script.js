$(document).ready(function() {
    // Load chat history from localStorage when the page loads
    var chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
    displayChatHistory(chatHistory);
    $('#submit-response').click(function() {
        var userResponse = $('#user-response').val();
        document.getElementById("user-response").value = "";
        // Add user response to chat history
        chatHistory.push({ role: 'user', content: userResponse });
        // Save updated chat history to localStorage
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
        $.ajax({
            url: '/interview',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({'user_response': userResponse}),
            success: function(response) {
                // Add AI response to chat history
                chatHistory.push({ role: 'assistant', content: response.ai_response });
                // Save updated chat history to localStorage
                localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
                // Display chat history including new messages
                displayChatHistory(chatHistory);
                // Check if the response contains an audio URL
            },
            error: function(xhr, status, error) {
                alert('Error occurred while processing request.');
            }
        });
    });


    $('#clear-chat-history').click(function() {
        console.log("clearing chat history");
        $.ajax({
            url: '/save_chat_history',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'chat_history': chatHistory }),
            success: function(response) {
                if (response.success) {
                    localStorage.removeItem('chatHistory'); // Clear chat history data from localStorage
                    $('#chat-container').empty();  // Clear chat container on the page
                    // Reload the page
                    location.reload();
                    alert('Chat history saved successfully.');
                } else {
                    alert('Error occurred while saving chat history.');
                }
            },
            error: function(xhr, status, error) {
                alert('Error occurred while processing request.');
            }
        });
    });
});



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


