import streamlit as st
import speech_recognition as sr
import pyttsx3
import tempfile
import os
import time
import threading
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="🎤 Voice Chat Prasad AI Bot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        margin-left: 20%;
    }
    
    .ai-message {
        background: #e3f2fd;
        color: #1976d2;
        margin-right: 20%;
    }
    
    .audio-container {
        background: #f5f5f5;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

class VoiceChatBot:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_lock = threading.Lock()
        self.llm = None
        self.conversation_chain = None
        self.memory = ConversationBufferMemory(return_messages=True)
        
    def initialize_llm(self, api_key):
        """Initialize the Google Gemini LLM"""
        try:
            genai.configure(api_key=api_key)
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key,
                temperature=0.7,
                convert_system_message_to_human=True
            )
            self.conversation_chain = ConversationChain(
                llm=self.llm,
                memory=self.memory,
                verbose=False
            )
            return True
        except Exception as e:
            st.error(f"Failed to initialize LLM: {str(e)}")
            return False
    
    def listen_for_speech(self):
        """Capture voice input"""
        try:
            with self.microphone as source:
                st.info("🔧 Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
            with self.microphone as source:
                st.info("🎤 Listening... Speak now!")
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=8)
            
            # Save audio to file
            audio_file_path = self.save_audio_to_file(audio)
            
            # Convert to text
            text = self.recognizer.recognize_google(audio)
            return text, audio_file_path
            
        except sr.WaitTimeoutError:
            return "timeout", None
        except sr.UnknownValueError:
            return "unclear", None
        except sr.RequestError as e:
            return f"error: {e}", None
    
    def save_audio_to_file(self, audio):
        """Save audio to temporary file"""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_file_path = temp_file.name
            temp_file.close()
            
            with open(temp_file_path, 'wb') as f:
                f.write(audio.get_wav_data())
            
            return temp_file_path
        except Exception as e:
            st.error(f"Error saving audio: {str(e)}")
            return None
    
    def process_with_llm(self, user_text):
        """Process with LLM"""
        try:
            if not self.conversation_chain:
                return "Please initialize the API key first!"
            
            response = self.conversation_chain.predict(input=user_text)
            return response
        except Exception as e:
            return f"Error processing with LLM: {str(e)}"
    
    def text_to_speech(self, text):
        """Convert text to speech - FIXED VERSION"""
        try:
            # Clean text
            clean_text = text.replace('*', '').replace('#', '').replace('`', '')
            clean_text = clean_text.replace('\n', ' ').replace('\r', ' ')
            clean_text = ' '.join(clean_text.split())
            
            # Limit length
            if len(clean_text) > 500:
                clean_text = clean_text[:500] + "..."
            
            if not clean_text.strip():
                return None
            
            # Create temp file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_file_path = temp_file.name
            temp_file.close()
            
            # FIXED: Create new TTS engine for each conversion
            with self.tts_lock:
                try:
                    # Initialize fresh engine each time
                    tts_engine = pyttsx3.init()
                    
                    # Set properties
                    tts_engine.setProperty('rate', 150)
                    tts_engine.setProperty('volume', 0.9)
                    
                    # Generate speech
                    tts_engine.save_to_file(clean_text, temp_file_path)
                    tts_engine.runAndWait()
                    
                    # IMPORTANT: Stop and delete engine to free resources
                    tts_engine.stop()
                    del tts_engine
                    
                except Exception as e:
                    st.error(f"TTS Error: {str(e)}")
                    return None
            
            # Verify file was created
            if os.path.exists(temp_file_path) and os.path.getsize(temp_file_path) > 0:
                return temp_file_path
            else:
                return None
                
        except Exception as e:
            st.error(f"Text-to-speech error: {str(e)}")
            return None

    def display_response(self, text_response, audio_path):
        """Display text and audio response"""
        st.markdown(f"""
        <div class="ai-message">
            <strong>🤖 AI Response:</strong><br>
            {text_response}
        </div>
        """, unsafe_allow_html=True)
        
        if audio_path and os.path.exists(audio_path):
            try:
                st.markdown("""
                <div class="audio-container">
                    <strong>🔊 Voice Response:</strong>
                </div>
                """, unsafe_allow_html=True)
                
                with open(audio_path, 'rb') as audio_file:
                    st.audio(audio_file.read(), format='audio/wav')
                    
            except Exception as e:
                st.error(f"Error playing audio: {str(e)}")
        else:
            st.warning("⚠️ Audio generation failed")

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎤 Voice Chat With Prasad AI Bot</h1>
        <p>Prasad AI maked your response better.......!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'chat_bot' not in st.session_state:
        st.session_state.chat_bot = VoiceChatBot()
        st.session_state.chat_history = []
        st.session_state.llm_initialized = False
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input("Google Gemini API Key", type="password")
        
        if api_key and not st.session_state.llm_initialized:
            if st.button("Initialize LLM"):
                with st.spinner("Initializing..."):
                    if st.session_state.chat_bot.initialize_llm(api_key):
                        st.session_state.llm_initialized = True
                        st.success("✅ LLM initialized!")
                    else:
                        st.error("❌ Failed to initialize LLM")
        
        st.markdown("---")
        st.info(f"Messages: {len(st.session_state.chat_history)}")
        
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.session_state.chat_bot.memory.clear()
            st.success("Chat cleared!")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message['type'] == 'user':
            st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
            
            if 'audio_path' in message and message['audio_path']:
                try:
                    with open(message['audio_path'], 'rb') as audio_file:
                        st.audio(audio_file.read(), format='audio/wav')
                except:
                    pass
        else:
            st.session_state.chat_bot.display_response(
                message['content'], 
                message.get('audio_path')
            )
    
    # Input section
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("🎙️ Voice Input")
        if st.button("🎤 Start Recording", disabled=not st.session_state.llm_initialized):
            if st.session_state.llm_initialized:
                # Voice input
                user_text, user_audio = st.session_state.chat_bot.listen_for_speech()
                
                if user_text not in ["timeout", "unclear"] and not user_text.startswith("error:"):
                    st.success(f"🎤 You said: {user_text}")
                    
                    # Add user message
                    st.session_state.chat_history.append({
                        'type': 'user',
                        'content': user_text,
                        'audio_path': user_audio
                    })
                    
                    # Get AI response
                    with st.spinner("🤖 soch bhai soch..."):
                        ai_response = st.session_state.chat_bot.process_with_llm(user_text)
                    
                    # Convert to speech
                    with st.spinner("🔊 speech main badal..."):
                        ai_audio = st.session_state.chat_bot.text_to_speech(ai_response)
                    
                    # Add AI response
                    st.session_state.chat_history.append({
                        'type': 'ai',
                        'content': ai_response,
                        'audio_path': ai_audio
                    })
                    
                    st.rerun()
                else:
                    st.warning(f"Voice input failed: {user_text}")
    
    with col2:
        st.header("📝 Text Input")
        text_input = st.text_area("Type your message:", height=100)
        
        if st.button("Send Message", disabled=not st.session_state.llm_initialized):
            if text_input.strip() and st.session_state.llm_initialized:
                # Add user message
                st.session_state.chat_history.append({
                    'type': 'user',
                    'content': text_input
                })
                
                # Get AI response
                with st.spinner("🤖 soch bhai soch ..."):
                    ai_response = st.session_state.chat_bot.process_with_llm(text_input)
                
                # Convert to speech
                with st.spinner("🔊 speech main badal..."):
                    ai_audio = st.session_state.chat_bot.text_to_speech(ai_response)
                
                # Add AI response
                st.session_state.chat_history.append({
                    'type': 'ai',
                    'content': ai_response,
                    'audio_path': ai_audio
                })
                
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🚀 Fixed Version - Audio works for every response!</p>
        <p><strong>Key Fix:</strong> TTS engine is properly reinitialized for each conversion</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()