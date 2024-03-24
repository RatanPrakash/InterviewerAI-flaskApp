let recognition;
let transcriptionElement = document.getElementById('transcript');
let outputElement = document.getElementById('output');
let interimTranscriptElement = document.getElementById('interim-transcript');
var audioElement = document.getElementById("audio");

$(document).ready(function () {
    // Load chat history from localStorage when the page loads
    var chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
    displayChatHistory(chatHistory);
    $('#submit-response').click(function () {
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
            data: JSON.stringify({ 'user_response': userResponse }),
            success: function (response) {
                // Add AI response to chat history
                chatHistory.push({ role: 'assistant', content: response.ai_response });
                // Save updated chat history to localStorage
                localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
                // Display chat history including new messages
                displayChatHistory(chatHistory);
            },
            error: function (xhr, status, error) {
                alert('Error occurred while processing request. ajax request failed');
            }
        });
    });

    $('#clear-chat-history').click(function () {
        console.log("clearing chat history");
        $.ajax({
            url: '/save_chat_history',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'chat_history': chatHistory }),
            success: function (response) {
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
            error: function (xhr, status, error) { // throws error when the above ajax request fails
                alert('Error occurred while processing request.');
            }
        });
    });



    const startButton = document.getElementById('startRecording');
    startButton.addEventListener('click', startVoiceCommunication);

    async function startVoiceCommunication() {
        recognition = new webkitSpeechRecognition() || new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onresult = async function (event) {
            let interimTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    interimTranscriptElement.innerHTML = '';
                    transcriptionElement.innerHTML += event.results[i][0].transcript + '<br>';
                    // Send the final transcript to the backend for processing
                    recognition.stop();
                    const resp = await sendTextToBackend(event.results[i][0].transcript);
                    // sendTextToBackend(event.results[i][0].transcript);
                } else {
                    interimTranscriptElement.innerHTML = event.results[i][0].transcript;
                }
            }
        };
        recognition.start();
    }

    async function sendTextToBackend(text) {
        // simulate a button click to send the text to the backend for processing
        // document.getElementById('#submit-response').click();
        var chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
        chatHistory.push({ role: 'user', content: text });
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));

        const response = await fetch('/process_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });
        const data = await response.json();
        chatHistory.push({ role: 'assistant', content: data.output });
        // Save updated chat history to localStorage
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
        // Display chat history including new messages
        displayChatHistory(chatHistory);
        await fetchAudio();
    }

    // Function to fetch audio data from the server
    function fetchAudio() {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/audio', true);
        xhr.responseType = 'arraybuffer';

        xhr.onload = function () {
            if (xhr.status === 200) {
                var audioData = xhr.response;
                playAudio(audioData);
            }
        };
        xhr.send();
    }

    function playAudio(audioBlob) {
        var audio = document.getElementById("audioPlayer");
        var blob = new Blob([audioBlob], { type: 'audio/mpeg' });
        var url = window.URL.createObjectURL(blob);
        audio.src = url;
        audio.play();
        console.log('Playing audio');

        audio.onended = function () {
            // This function will be called when the audio has finished playing
            console.log('Audio playback finished');
            recognition.start();
        };
    }
});