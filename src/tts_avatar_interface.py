"""
Legacy Memory Assistant - Text-to-Speech Avatar Interface
Handles avatar rendering and voice synthesis for memory playback.
"""

import pyttsx3
import threading
import queue
import time
from typing import Dict, Optional, Callable, List
import json
import os
import random


class AvatarInterface:
    """Manages the avatar interface and text-to-speech functionality."""
    
    def __init__(self, voice_id: Optional[str] = None, speaking_rate: int = 150):
        """
        Initialize the avatar interface.
        
        Args:
            voice_id: Specific voice ID to use
            speaking_rate: Words per minute for speech
        """
        self.tts_engine = pyttsx3.init()
        self.speaking_rate = speaking_rate
        self.is_speaking = False
        self.voice_profiles = {}
        self.current_emotion = "neutral"
        self.avatar_state = {
            'is_active': False,
            'current_expression': 'neutral',
            'speaking': False,
            'last_activity': None
        }
        
        self._setup_tts()
        self._load_voice_profiles()
    
    def _setup_tts(self):
        """Configure the text-to-speech engine."""
        try:
            # Set speech rate
            self.tts_engine.setProperty('rate', self.speaking_rate)
            
            # Set volume
            self.tts_engine.setProperty('volume', 0.8)
            
            # List available voices
            voices = self.tts_engine.getProperty('voices')
            print("Available voices:")
            for i, voice in enumerate(voices):
                print(f"  {i}: {voice.name} ({voice.id})")
            
            # Use a more natural voice if available
            if voices:
                # Prefer female voices for warmer feel
                female_voices = [v for v in voices if 'female' in v.name.lower() or 'woman' in v.name.lower()]
                if female_voices:
                    self.tts_engine.setProperty('voice', female_voices[0].id)
                    print(f"Selected voice: {female_voices[0].name}")
                else:
                    self.tts_engine.setProperty('voice', voices[0].id)
                    print(f"Selected voice: {voices[0].name}")
        
        except Exception as e:
            print(f"Error setting up TTS: {e}")
    
    def _load_voice_profiles(self):
        """Load voice profiles for different emotional states."""
        self.voice_profiles = {
            'happy': {
                'rate': self.speaking_rate + 20,
                'volume': 0.9,
                'pitch_modifier': 1.1
            },
            'sad': {
                'rate': self.speaking_rate - 30,
                'volume': 0.6,
                'pitch_modifier': 0.9
            },
            'excited': {
                'rate': self.speaking_rate + 40,
                'volume': 1.0,
                'pitch_modifier': 1.2
            },
            'calm': {
                'rate': self.speaking_rate - 10,
                'volume': 0.7,
                'pitch_modifier': 1.0
            },
            'neutral': {
                'rate': self.speaking_rate,
                'volume': 0.8,
                'pitch_modifier': 1.0
            }
        }
    
    def speak(self, text: str, emotion: str = "neutral", blocking: bool = True):
        """
        Speak the given text with appropriate emotion.
        
        Args:
            text: Text to speak
            emotion: Emotional context for speech
            blocking: Whether to wait for speech to complete
        """
        if not text or not text.strip():
            return
        
        self.current_emotion = emotion
        self._apply_voice_profile(emotion)
        
        # Add emotional context to speech
        enhanced_text = self._enhance_text_with_emotion(text, emotion)
        
        # Update avatar state
        self.avatar_state.update({
            'speaking': True,
            'current_expression': emotion,
            'last_activity': time.time()
        })
        
        def speak_async():
            try:
                self.is_speaking = True
                print(f"[Avatar - {emotion}]: {text}")
                self.tts_engine.say(enhanced_text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"Error during speech: {e}")
            finally:
                self.is_speaking = False
                self.avatar_state['speaking'] = False
        
        if blocking:
            speak_async()
        else:
            threading.Thread(target=speak_async, daemon=True).start()
    
    def _apply_voice_profile(self, emotion: str):
        """Apply voice settings based on emotion."""
        profile = self.voice_profiles.get(emotion, self.voice_profiles['neutral'])
        
        try:
            self.tts_engine.setProperty('rate', profile['rate'])
            self.tts_engine.setProperty('volume', profile['volume'])
            # Note: Pitch modification is limited in pyttsx3
        except Exception as e:
            print(f"Error applying voice profile: {e}")
    
    def _enhance_text_with_emotion(self, text: str, emotion: str) -> str:
        """Add emotional context to text through punctuation and pacing."""
        if emotion == "happy":
            # Add slight enthusiasm
            text = text.replace(".", "!")
            return text
        elif emotion == "sad":
            # Add pauses and softer tone
            text = text.replace(",", "... ")
            return text
        elif emotion == "excited":
            # Add emphasis and exclamation
            text = text.replace(".", "!")
            text = text.replace("!", "!!")
            return text
        elif emotion == "calm":
            # Add gentle pauses
            text = text.replace(".", "... ")
            return text
        
        return text
    
    def stop_speaking(self):
        """Stop current speech."""
        try:
            self.tts_engine.stop()
            self.is_speaking = False
            self.avatar_state['speaking'] = False
        except Exception as e:
            print(f"Error stopping speech: {e}")
    
    def get_avatar_state(self) -> Dict:
        """Get current avatar state."""
        return self.avatar_state.copy()
    
    def set_avatar_expression(self, expression: str):
        """Set avatar facial expression."""
        self.avatar_state['current_expression'] = expression
        print(f"Avatar expression: {expression}")
    
    def simulate_avatar_movement(self, duration: float = 2.0):
        """Simulate avatar movement/gestures."""
        def animate():
            gestures = ['nod', 'smile', 'tilt_head', 'gentle_wave']
            gesture = random.choice(gestures)
            print(f"Avatar gesture: {gesture}")
            time.sleep(duration)
        
        threading.Thread(target=animate, daemon=True).start()


class MemoryPlaybackInterface:
    """Interface for playing back memories through the avatar."""
    
    def __init__(self, avatar: AvatarInterface):
        """
        Initialize the playback interface.
        
        Args:
            avatar: Avatar interface instance
        """
        self.avatar = avatar
        self.playback_queue = queue.Queue()
        self.is_playing = False
        self.current_memory = None
    
    def play_memory(self, memory: Dict, interactive: bool = False):
        """
        Play back a memory through the avatar.
        
        Args:
            memory: Memory dictionary with content and metadata
            interactive: Whether to allow interaction during playback
        """
        if not memory or 'content' not in memory:
            print("Invalid memory data")
            return
        
        self.current_memory = memory
        emotion = memory.get('emotion', 'neutral')
        content = memory['content']
        
        # Add contextual introduction
        intro = self._generate_memory_intro(memory)
        if intro:
            self.avatar.speak(intro, emotion='calm')
            time.sleep(0.5)
        
        # Speak the main content
        self.avatar.speak(content, emotion=emotion)
        
        # Add closing if appropriate
        if memory.get('tags') and 'family' in memory['tags']:
            self.avatar.speak("I hope you treasure this memory as much as I do.", emotion='warm')
    
    def _generate_memory_intro(self, memory: Dict) -> str:
        """Generate a contextual introduction for the memory."""
        timestamp = memory.get('timestamp', '')
        tags = memory.get('tags', [])
        
        if 'family' in tags:
            intros = [
                "Here's something special I want to share with you...",
                "This is one of my favorite family memories...",
                "Let me tell you about a wonderful moment..."
            ]
        elif 'achievement' in tags:
            intros = [
                "I was so proud when this happened...",
                "This was such an important moment for me..."
            ]
        else:
            intros = [
                "Here's something I wanted you to know...",
                "This memory means a lot to me..."
            ]
        
        return random.choice(intros)
    
    def play_memory_sequence(self, memories: List[Dict], delay: float = 2.0):
        """
        Play multiple memories in sequence.
        
        Args:
            memories: List of memory dictionaries
            delay: Delay between memories in seconds
        """
        self.is_playing = True
        
        try:
            for i, memory in enumerate(memories):
                if not self.is_playing:
                    break
                
                print(f"Playing memory {i+1}/{len(memories)}")
                self.play_memory(memory)
                
                if i < len(memories) - 1:  # Not the last memory
                    time.sleep(delay)
        
        except KeyboardInterrupt:
            print("Playback interrupted")
        finally:
            self.is_playing = False
    
    def stop_playback(self):
        """Stop current playback."""
        self.is_playing = False
        self.avatar.stop_speaking()
    
    def interactive_session(self, memories: List[Dict]):
        """
        Start an interactive session where users can request specific memories.
        
        Args:
            memories: Available memories to choose from
        """
        print("Starting interactive memory session...")
        print("Available commands: 'play [number]', 'list', 'search [term]', 'quit'")
        
        while True:
            try:
                command = input("\nWhat would you like to hear? ").strip().lower()
                
                if command == 'quit':
                    break
                elif command == 'list':
                    self._list_memories(memories)
                elif command.startswith('play '):
                    try:
                        index = int(command.split()[1]) - 1
                        if 0 <= index < len(memories):
                            self.play_memory(memories[index])
                        else:
                            print(f"Invalid memory number. Choose 1-{len(memories)}")
                    except (ValueError, IndexError):
                        print("Invalid command. Use 'play [number]'")
                elif command.startswith('search '):
                    search_term = command[7:]
                    matching_memories = self._search_memories(memories, search_term)
                    if matching_memories:
                        print(f"Found {len(matching_memories)} matching memories:")
                        self._list_memories(matching_memories)
                    else:
                        print("No matching memories found.")
                else:
                    print("Unknown command. Try 'list', 'play [number]', 'search [term]', or 'quit'")
            
            except KeyboardInterrupt:
                break
        
        print("Goodbye! Take care of these memories.")
    
    def _list_memories(self, memories: List[Dict]):
        """List available memories."""
        for i, memory in enumerate(memories, 1):
            content_preview = memory['content'][:50] + "..." if len(memory['content']) > 50 else memory['content']
            emotion = memory.get('emotion', 'neutral')
            tags = ', '.join(memory.get('tags', []))
            print(f"{i}. [{emotion}] {content_preview} (Tags: {tags})")
    
    def _search_memories(self, memories: List[Dict], search_term: str) -> List[Dict]:
        """Search memories by content or tags."""
        matching = []
        search_term = search_term.lower()
        
        for memory in memories:
            if (search_term in memory['content'].lower() or 
                any(search_term in tag.lower() for tag in memory.get('tags', []))):
                matching.append(memory)
        
        return matching


if __name__ == "__main__":
    # Example usage
    avatar = AvatarInterface()
    playback = MemoryPlaybackInterface(avatar)
    
    # Example memories
    sample_memories = [
        {
            'content': "Today was your first day of school, and you were so brave walking into that classroom.",
            'emotion': 'proud',
            'tags': ['family', 'milestone', 'school'],
            'timestamp': '2023-09-01'
        },
        {
            'content': "We had the most wonderful picnic in the park, and you laughed so much when the ducks came over.",
            'emotion': 'happy',
            'tags': ['family', 'park', 'fun'],
            'timestamp': '2023-07-15'
        }
    ]
    
    # Test single memory playback
    print("Playing sample memory...")
    playback.play_memory(sample_memories[0])
    
    time.sleep(2)
    
    # Test interactive session
    print("\n" + "="*50)
    print("Starting interactive session...")
    playback.interactive_session(sample_memories)
