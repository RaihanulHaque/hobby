import asyncio
import websockets
import numpy as np
from scipy.signal import resample
import json
from RealtimeSTT import AudioToTextRecorder


# Global variables
recorder = None
client_websocket = None

# Recorder ready event
recorder_ready = asyncio.Event()

async def send_to_client(message):
    if client_websocket:
        await client_websocket.send(message)

def text_detected(text):
    asyncio.create_task(
        send_to_client(
            json.dumps({
                'type': 'realtime',
                'text': text
            })
        )
    )
    print(f"\r{text}", flush=True, end='')

# Recorder config
# recorder_config = {
#     'spinner': False,
#     'use_microphone': False,
#     'model': 'large-v2',
#     'language': 'en',
#     'silero_sensitivity': 0.4,
#     'webrtc_sensitivity': 2,
#     'post_speech_silence_duration': 0.7,
#     'min_length_of_recording': 0,
#     'min_gap_between_recordings': 0,
#     'enable_realtime_transcription': True,
#     'realtime_processing_pause': 0,
#     'realtime_model_type': 'tiny.en',
#     'on_realtime_transcription_stabilized': text_detected,
# }
recorder_config = {
        'spinner': False,
        'model': 'tiny.en',
        'language': 'en',
        'silero_sensitivity': 0.01,
        'webrtc_sensitivity': 3,
        'silero_use_onnx': False,
        'post_speech_silence_duration': 1.2,
        'min_length_of_recording': 0.2,
        'min_gap_between_recordings': 0,
        'enable_realtime_transcription': True,
        'realtime_processing_pause': 0,
        'realtime_model_type': 'tiny.en',
        'on_realtime_transcription_stabilized': text_detected,
    }

async def recorder_thread():
    global recorder
    print("Initializing RealtimeSTT...")
    recorder = AudioToTextRecorder(**recorder_config)
    print("RealtimeSTT initialized")
    recorder_ready.set()  # Indicate that the recorder is ready

    while True:
        full_sentence = recorder.text()
        await send_to_client(
            json.dumps({
                'type': 'fullSentence',
                'text': full_sentence
            })
        )
        print(f"\rSentence: {full_sentence}")

def decode_and_resample(audio_data, original_sample_rate, target_sample_rate):
    # Decode 16-bit PCM data to numpy array
    audio_np = np.frombuffer(audio_data, dtype=np.int16)

    # Calculate the number of samples after resampling
    num_original_samples = len(audio_np)
    num_target_samples = int(num_original_samples * target_sample_rate / original_sample_rate)

    # Resample the audio
    resampled_audio = resample(audio_np, num_target_samples)

    return resampled_audio.astype(np.int16).tobytes()

async def echo(websocket, path):
    print("Client connected")
    global client_websocket
    client_websocket = websocket

    async for message in websocket:
        if not recorder_ready.is_set():
            print("Recorder not ready")
            continue

        # Parse the metadata and audio chunk from the WebSocket message
        metadata_length = int.from_bytes(message[:4], byteorder='little')
        metadata_json = message[4:4+metadata_length].decode('utf-8')
        metadata = json.loads(metadata_json)
        sample_rate = metadata['sampleRate']
        chunk = message[4+metadata_length:]

        # Resample and feed the audio data to the recorder
        resampled_chunk = decode_and_resample(chunk, sample_rate, 16000)
        recorder.feed_audio(resampled_chunk)

async def main():
    # Start the recorder in a background task
    await recorder_thread()

    # Start the WebSocket server
    start_server = websockets.serve(echo, "localhost", 8001)

    # Run the WebSocket server and allow the asyncio event loop to handle everything
    await start_server
    print("Server started. Press Ctrl+C to stop the server.")
    await asyncio.Future()  # Run forever

if __name__ == '__main__':
    print("Starting server, please wait...")
    asyncio.run(main())  # Run everything using the main asyncio event loop
