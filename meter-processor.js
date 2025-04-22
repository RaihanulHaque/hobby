// audio-worklet-processor.js
class AudioMeterProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this.smoothingTimeConstant = 0.8;
    this.fftSize = 1024;
    this.analyser = new AnalyserNode(this.context, {
      smoothingTimeConstant: this.smoothingTimeConstant,
      fftSize: this.fftSize,
    });
  }

  process(inputs, outputs, parameters) {
    const input = inputs[0];
    if (!input || input.length === 0) {
      return true;
    }

    this.analyser.getFloatTimeDomainData(this.inputBuffer);
    const array = new Uint8Array(this.analyser.frequencyBinCount);
    this.analyser.getByteFrequencyData(array);
    let values = 0;
    const length = array.length;

    for (let i = 0; i < length; i++) {
      values += array[i];
    }
    const average = values / length;

    // Send the average value to the main thread
    this.port.postMessage(average);

    return true;
  }

  static get parameterDescriptors() {
    return [];
  }
}

registerProcessor("audio-meter-processor", AudioMeterProcessor);
