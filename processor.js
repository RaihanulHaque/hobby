class MyAudioProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this.buffer = [];
    this.bufferSize = 4096;
    this.debugCounter = 0; // Add counter for debugging
  }

  process(inputs, outputs, parameters) {
    const input = inputs[0];
    const channel = input[0];

    if (channel) {
      // Log audio input occasionally
      if (this.debugCounter % 100 === 0) {
        console.log("Audio processing:", {
          inputLength: channel.length,
          maxValue: Math.max(...channel),
          minValue: Math.min(...channel),
        });
      }
      this.debugCounter++;

      // Convert Float32Array to Int16Array
      const pcmData = new Int16Array(channel.length);
      for (let i = 0; i < channel.length; i++) {
        pcmData[i] = Math.max(-32768, Math.min(32767, channel[i] * 32768));
      }

      this.buffer.push(...pcmData);

      if (this.buffer.length >= this.bufferSize) {
        this.port.postMessage({
          type: "audio",
          data: new Int16Array(this.buffer),
          bufferSize: this.buffer.length,
        });
        this.buffer = [];
      }
    }

    return true;
  }
}

registerProcessor("my-audio-processor", MyAudioProcessor);
