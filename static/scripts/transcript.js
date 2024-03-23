let recognition;
let transcriptionElement = document.getElementById('transcript');
let outputElement = document.getElementById('output');
let interimTranscriptElement = document.getElementById('interim-transcript');
var audioElement = document.getElementById("audio");

const startButton = document.getElementById('startButton');
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
    const response = await fetch('/process_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text })
    });
    const data = await response.json();
    outputElement.innerHTML = data.output;
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

    audio.onended = function() {
        // This function will be called when the audio has finished playing
        console.log('Audio playback finished');
        recognition.start();
    };
}
