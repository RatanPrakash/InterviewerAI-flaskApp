
let recognition;
let transcriptionElement = document.getElementById('transcript');
let outputElement = document.getElementById('output');
let interimTranscriptElement = document.getElementById('interim-transcript');
var audioElement = document.getElementById("audio");

const startButton = document.getElementById('startButton');
startButton.addEventListener('click', startVoiceCommunication);

function startVoiceCommunication() {
    recognition = new webkitSpeechRecognition() || new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = function(event) {
        let interimTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                interimTranscriptElement.innerHTML = '';
                transcriptionElement.innerHTML += event.results[i][0].transcript + '<br>';
                // Send the final transcript to the backend for processing
                sendTextToBackend(event.results[i][0].transcript);
            } else {
                interimTranscriptElement.innerHTML = event.results[i][0].transcript;
            }
        }
    };
    recognition.start();
}

async function sendTextToBackend(text) {
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

function playAudio(audioBlob) {
var audio = document.getElementById("audioPlayer");
  var blob = new Blob([audioBlob], { type: 'audio/mpeg' });
  var url = window.URL.createObjectURL(blob);
  audio.src = url;
  audio.play();
}

// Function to fetch audio data from the server
function fetchAudio() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/audio', true);
    xhr.responseType = 'arraybuffer';
  
    xhr.onload = function() {
      if (xhr.status === 200) {
        var audioData = xhr.response;
        playAudio(audioData);
      }
    };
  
    xhr.send();
  }
