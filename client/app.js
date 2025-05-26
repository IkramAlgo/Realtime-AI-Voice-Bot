let mediaRecorder;
let audioChunks = [];
let isProcessing = false;

async function startRecording() {
    if (isProcessing) {
        alert("Please wait for the current process to complete");
        return;
    }
    
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
                sampleRate: 16000,
                channelCount: 1,
                mimeType: 'audio/webm; codecs=opus'
            }
        });
        
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            console.log("Audio Blob Size:", audioBlob.size);
            
            await processAudio(audioBlob);
            stream.getTracks().forEach(track => track.stop());
        };

        mediaRecorder.start();
        document.getElementById("record-btn").classList.add("recording");
        document.getElementById("status").textContent = "Recording...";
    } catch (err) {
        console.error("Recording Error:", err);
        alert("Microphone access denied! Please enable permissions.");
    }
}

async function processAudio(audioBlob) {
    isProcessing = true;
    document.getElementById("status").textContent = "Processing...";
    
    try {
        const formData = new FormData();
        formData.append("audio", audioBlob, "recording.wav");

        const response = await fetch("http://localhost:8000/process", {
            method: "POST",
            body: formData,
            headers: {
                "Accept": "application/json"
            }
        });

        console.log("Response Status:", response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server Error: ${response.status} - ${errorText}`);
        }

        const data = await response.json();
        console.log("Server Response:", data);
        
        if (!data.audio || !data.text) {
            throw new Error("Invalid server response");
        }

        // Update response text
        document.getElementById("response-text").textContent = data.text;
        
        // Play audio
        const audio = new Audio(`data:audio/mpeg;base64,${data.audio}`);
        audio.play().catch(err => console.error("Audio playback error:", err));
        
    } catch (error) {
        console.error("Full Error:", error);
        alert(`Error: ${error.message}`);
    } finally {
        audioChunks = [];
        isProcessing = false;
        document.getElementById("record-btn").classList.remove("recording");
        document.getElementById("status").textContent = "Ready";
    }
}

// Event Listeners
document.getElementById("record-btn").addEventListener("mousedown", startRecording);
document.getElementById("record-btn").addEventListener("mouseup", () => {
    if (mediaRecorder?.state === "recording") {
        mediaRecorder.stop();
    }
});