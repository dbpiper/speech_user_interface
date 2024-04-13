import pyaudio
import numpy as np
from google.cloud import speech_v1 as speech


def read_in_speech() -> str | None:
    client = speech.SpeechClient()

    # Initialize PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8192,
    )
    stream.start_stream()

    # Configure the request
    audio_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=audio_config, interim_results=True
    )

    audio_buffer = []
    silent_frames = 0
    threshold = 500  # Silence threshold
    silence_limit = 10  # Lower number of silent frames required to consider it the end of a speech

    try:
        while True:
            data = stream.read(8192, exception_on_overflow=False)
            if not data:
                break  # Stop if no data is read

            audio_buffer.append(data)

            # Check if current chunk is silent
            if is_silence(data, threshold):
                silent_frames += 1
            else:
                silent_frames = 0  # reset silent count on noise

            # If silence has been detected long enough, consider end of speech
            if silent_frames > silence_limit:
                # Send buffered audio to Google Speech API
                requests = (
                    speech.StreamingRecognizeRequest(audio_content=chunk)
                    for chunk in audio_buffer
                )
                responses = client.streaming_recognize(
                    config=streaming_config, requests=requests
                )
                for response in responses:
                    for result in response.results:
                        if result.is_final:
                            return result.alternatives[0].transcript

                # Clear the buffer and reset silence frames
                audio_buffer = []
                silent_frames = 0
    finally:
        # Close the stream properly
        stream.stop_stream()
        stream.close()
        p.terminate()

    return None


def is_silence(data, threshold):
    """Check if the given audio data contains silence defined by the threshold."""
    # Convert to numpy array to check audio volume
    as_ints = np.frombuffer(data, dtype=np.int16)
    if np.mean(np.abs(as_ints)) < threshold:
        return True
    return False
