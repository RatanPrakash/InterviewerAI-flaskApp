const videoElement = document.getElementById('video');
const startRecordingButton = document.getElementById('startRecording');
const hangupButton = document.getElementById('hangup');

let mediaRecorder;
let recordedChunks = [];

startRecordingButton.addEventListener('click', startRecording);
hangupButton.addEventListener('click', hangup);

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true , audio: true});
        videoElement.srcObject = stream;
        mediaRecorder = new MediaRecorder(stream);
        
        mediaRecorder.ondataavailable = function(event) {
            recordedChunks.push(event.data);
        };
        
        mediaRecorder.onstop = function() {
            const blob = new Blob(recordedChunks, { type: 'video/webm' });
            sendVideo(blob);
        };
        
        mediaRecorder.start();
    } catch (error) {
        console.error('Error accessing webcam:', error);
    }
}

function hangup() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
    }
    if (videoElement.srcObject) {
        const tracks = videoElement.srcObject.getTracks();
        tracks.forEach(track => track.stop());
        videoElement.srcObject = null;
    }
}

function sendVideo(blob) {
    const formData = new FormData();
    formData.append('video', blob);
    
    fetch('/save_video', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            console.log('Video saved successfully');
        } else {
            console.error('Failed to save video');
        }
    })
    .catch(error => {
        console.error('Error saving video:', error);
    });
}

