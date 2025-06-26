"""
Legacy Memory Assistant - Speech to Text Processing
Handles real-time audio capture and transcription.
"""

import whisper
import pyaudio
import wave
import numpy as np
import threading
import queue
import time
from typing import Optional, Callable
import os


class SpeechProcessor:
    """Handles speech-to-text conversion with real-time processing."""
    
    def __init__(self, model_size: str = "base", language: str = "en"):
        """
        Initialize the speech processor.
        
        Args:
            model_size: Whisper model size ("tiny", "base", "small", "medium", "large")
            language: Primary language for transcription
        """
        self.model_size = model_size
        self.language = language
        self.model = None
        self.is_listening = False
        self.audio_queue = queue.Queue()
        
        # Audio configuration
        self.chunk_size = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.silence_threshold = 500
        self.silence_duration = 2.0  # seconds of silence to stop recording
        
        self._load_model()
    
    def _load_model(self):
        """Load the Whisper model."""
        try:
            print(f"Loading Whisper model ({self.model_size})...")
            self.model = whisper.load_model(self.model_size)
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            raise
    
    def listen_once(self, duration: float = 5.0) -> Optional[str]:
        """
        Record audio for a specific duration and transcribe it.
        
        Args:
            duration: Recording duration in seconds
            
        Returns:
            Transcribed text or None if failed
        """
        try:
            audio = pyaudio.PyAudio()
            
            stream = audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            print(f"Recording for {duration} seconds...")
            frames = []
            
            for _ in range(0, int(self.rate / self.chunk_size * duration)):
                data = stream.read(self.chunk_size)
                frames.append(data)
            
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            # Convert to numpy array
            audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
            audio_data = audio_data.astype(np.float32) / 32768.0
            
            return self.transcribe_audio(audio_data)
            
        except Exception as e:
            print(f"Error during recording: {e}")
            return None
    
    def listen_continuous(self, callback: Callable[[str], None], 
                         stop_event: threading.Event = None):
        """
        Continuously listen for speech and transcribe it.
        
        Args:
            callback: Function to call with transcribed text
            stop_event: Threading event to stop listening
        """
        if stop_event is None:
            stop_event = threading.Event()
        
        self.is_listening = True
        audio = pyaudio.PyAudio()
        
        try:
            stream = audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            print("Listening continuously... Press Ctrl+C to stop")
            
            frames = []
            silence_start = None
            
            while self.is_listening and not stop_event.is_set():
                data = stream.read(self.chunk_size, exception_on_overflow=False)
                frames.append(data)
                
                # Check for silence
                audio_chunk = np.frombuffer(data, dtype=np.int16)
                volume = np.sqrt(np.mean(audio_chunk**2))
                
                if volume < self.silence_threshold:
                    if silence_start is None:
                        silence_start = time.time()
                    elif time.time() - silence_start > self.silence_duration:
                        # Process accumulated audio
                        if len(frames) > self.rate // self.chunk_size:  # At least 1 second
                            audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
                            audio_data = audio_data.astype(np.float32) / 32768.0
                            
                            text = self.transcribe_audio(audio_data)
                            if text and text.strip():
                                callback(text.strip())
                        
                        frames = []
                        silence_start = None
                else:
                    silence_start = None
            
            stream.stop_stream()
            stream.close()
            
        except KeyboardInterrupt:
            print("\nStopping continuous listening...")
        except Exception as e:
            print(f"Error during continuous listening: {e}")
        finally:
            audio.terminate()
            self.is_listening = False
    
    def transcribe_audio(self, audio_data: np.ndarray) -> Optional[str]:
        """
        Transcribe audio data using Whisper.
        
        Args:
            audio_data: Audio data as numpy array
            
        Returns:
            Transcribed text or None if failed
        """
        if self.model is None:
            print("Model not loaded!")
            return None
        
        try:
            # Whisper expects audio at 16kHz
            if len(audio_data) < self.rate * 0.1:  # Less than 0.1 seconds
                return None
            
            result = self.model.transcribe(
                audio_data,
                language=self.language,
                task="transcribe"
            )
            
            text = result["text"].strip()
            confidence = result.get("confidence", 0.0)
            
            # Filter out low confidence or very short results
            if len(text) < 3 or confidence < 0.3:
                return None
            
            return text
            
        except Exception as e:
            print(f"Error during transcription: {e}")
            return None
    
    def transcribe_file(self, file_path: str) -> Optional[str]:
        """
        Transcribe an audio file.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Transcribed text or None if failed
        """
        if not os.path.exists(file_path):
            print(f"Audio file not found: {file_path}")
            return None
        
        try:
            result = self.model.transcribe(file_path, language=self.language)
            return result["text"].strip()
        except Exception as e:
            print(f"Error transcribing file: {e}")
            return None
    
    def stop_listening(self):
        """Stop continuous listening."""
        self.is_listening = False
    
    def get_available_devices(self):
        """Get list of available audio input devices."""
        audio = pyaudio.PyAudio()
        devices = []
        
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                devices.append({
                    'index': i,
                    'name': device_info['name'],
                    'channels': device_info['maxInputChannels']
                })
        
        audio.terminate()
        return devices
    
    def test_microphone(self, duration: float = 3.0) -> bool:
        """
        Test microphone functionality.
        
        Args:
            duration: Test duration in seconds
            
        Returns:
            True if microphone works, False otherwise
        """
        try:
            print(f"Testing microphone for {duration} seconds...")
            audio = pyaudio.PyAudio()
            
            stream = audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            max_volume = 0
            for _ in range(int(self.rate / self.chunk_size * duration)):
                data = stream.read(self.chunk_size)
                audio_chunk = np.frombuffer(data, dtype=np.int16)
                volume = np.sqrt(np.mean(audio_chunk**2))
                max_volume = max(max_volume, volume)
            
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            print(f"Maximum volume detected: {max_volume}")
            return max_volume > 50  # Threshold for working microphone
            
        except Exception as e:
            print(f"Microphone test failed: {e}")
            return False


def emotion_from_audio(audio_data: np.ndarray) -> str:
    """
    Simple emotion detection from audio features.
    This is a placeholder - in production, you'd use a proper emotion recognition model.
    
    Args:
        audio_data: Audio data as numpy array
        
    Returns:
        Detected emotion as string
    """
    # Simple heuristic based on audio characteristics
    volume = np.sqrt(np.mean(audio_data**2))
    pitch_variance = np.var(audio_data)
    
    if volume > 0.3 and pitch_variance > 0.1:
        return "excited"
    elif volume < 0.1:
        return "calm"
    elif pitch_variance > 0.15:
        return "animated"
    else:
        return "neutral"


if __name__ == "__main__":
    # Example usage
    processor = SpeechProcessor(model_size="base")
    
    # Test microphone
    if processor.test_microphone():
        print("Microphone test passed!")
        
        # Record once
        text = processor.listen_once(duration=5.0)
        if text:
            print(f"You said: {text}")
        
        # Continuous listening example
        def on_speech(text):
            print(f"Transcribed: {text}")
        
        try:
            processor.listen_continuous(on_speech)
        except KeyboardInterrupt:
            processor.stop_listening()
    else:
        print("Microphone test failed!")
