let audioContext;
let source;
let processor;
let mic_available = false;
let socket = new WebSocket("ws://localhost:8001");
let server_available = false;
let audioDebugInterval;

async function initAudio() {
  try {
    console.log("Initializing audio...");
    audioContext = new AudioContext();
    console.log("AudioContext created:", audioContext.state);

    console.log("Loading audio worklet...");
    await audioContext.audioWorklet.addModule("processor.js");
    console.log("Audio worklet loaded successfully");

    processor = new AudioWorkletNode(audioContext, "my-audio-processor");
    console.log("AudioWorkletNode created");

    // Debug audio processing
    processor.port.onmessage = (event) => {
      if (event.data.type === "audio") {
        // console.log("Received audio chunk:", {
        //   size: event.data.data.length,
        //   bufferSize: event.data.bufferSize,
        //   maxValue: Math.max(...event.data.data),
        //   minValue: Math.min(...event.data.data),
        // });
        sendAudioData(event.data.data);
      }
    };

    console.log("Requesting microphone access...");
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    console.log("Microphone access granted");

    source = audioContext.createMediaStreamSource(stream);
    source.connect(processor);

    // Add audio meter for visualization
    startAudioMeter(stream);

    mic_available = true;
    start_msg();
    console.log("Audio initialization complete");
  } catch (error) {
    console.error("Error initializing audio:", error);
  }
}

// Add audio meter visualization
function startAudioMeter(stream) {
  const audioContext = new AudioContext();
  const analyser = audioContext.createAnalyser();
  const microphone = audioContext.createMediaStreamSource(stream);
  const javascriptNode = audioContext.createScriptProcessor(2048, 1, 1);

  analyser.smoothingTimeConstant = 0.8;
  analyser.fftSize = 1024;

  microphone.connect(analyser);
  analyser.connect(javascriptNode);
  javascriptNode.connect(audioContext.destination);

  javascriptNode.onaudioprocess = function () {
    const array = new Uint8Array(analyser.frequencyBinCount);
    analyser.getByteFrequencyData(array);
    let values = 0;

    const length = array.length;
    for (let i = 0; i < length; i++) {
      values += array[i];
    }

    const average = values / length;
    updateAudioMeter(average);
  };
}

function updateAudioMeter(level) {
  const meter = document.getElementById("audioMeter");
  if (meter) {
    meter.style.width = level + "px";
    meter.style.backgroundColor = level > 50 ? "red" : "green";
  }
}

function sendAudioData(audioData) {
  if (socket.readyState === WebSocket.OPEN) {
    console.log("Sending audio data:", {
      size: audioData.length,
      sampleRate: audioContext.sampleRate,
    });

    let metadata = JSON.stringify({
      sampleRate: audioContext.sampleRate,
    });
    let metadataBytes = new TextEncoder().encode(metadata);
    let metadataLength = new ArrayBuffer(4);
    let metadataLengthView = new DataView(metadataLength);
    metadataLengthView.setInt32(0, metadataBytes.byteLength, true);

    let combinedData = new Blob([
      metadataLength,
      metadataBytes,
      audioData.buffer,
    ]);

    socket.send(combinedData);
  } else {
    console.warn("WebSocket not ready:", socket.readyState);
  }
}

// WebSocket setup with debugging
socket.onopen = function (event) {
  console.log("WebSocket connected");
  server_available = true;
  start_msg();
};

socket.onclose = function (event) {
  console.log("WebSocket disconnected", event);
  server_available = false;
  start_msg();
};

socket.onerror = function (error) {
  console.error("WebSocket error:", error);
};

socket.onmessage = function (event) {
  console.log("Received message from server:", event.data);
  try {
    const data = JSON.parse(event.data);
    if (data.type === "transcription") {
      displayTranscription(data.text);
    } else if (data.type === "error") {
      console.error("Server error:", data.message);
    }
  } catch (e) {
    console.error("Error parsing message:", e);
  }
};

// Update HTML to include audio meter
function start_msg() {
  const displayDiv = document.getElementById("textDisplay");
  let message = "";
  if (!mic_available) {
    message = "🎤 Please allow microphone access 🎤";
  } else if (!server_available) {
    message = "🖥️ Please start server 🖥️";
  } else {
    message = "👄 Start speaking 👄";
  }
  displayDiv.innerHTML = `
        ${message}
        <div id="audioMeterContainer" style="margin-top: 20px; background: #333; width: 200px; height: 20px;">
            <div id="audioMeter" style="height: 100%; width: 0px; background: green; transition: width 0.1s;"></div>
        </div>
    `;
}

// Initialize audio when the page loads
document.addEventListener("DOMContentLoaded", () => {
  initAudio();
});
