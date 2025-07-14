# Prasad-AI-chatbot

# 🎤 Voice Chat Prasad AI Bot

A Streamlit-based voice chat application that combines speech recognition, Google Gemini AI, and text-to-speech functionality for natural voice conversations.

## 🚀 Program Flow

### 1. **Application Initialization**
```
├── Streamlit app configuration (page title, icon, layout)
├── Custom CSS styling for chat interface
├── VoiceChatBot class instantiation
└── Session state initialization
```

### 2. **Core Components Setup**

#### **VoiceChatBot Class Components:**
- **Speech Recognition**: Uses `speech_recognition` library with Google's API
- **Text-to-Speech**: Implements `pyttsx3` for audio response generation
- **LLM Integration**: Google Gemini AI via `langchain_google_genai`
- **Memory Management**: `ConversationBufferMemory` for chat history
- **Threading**: Thread-safe TTS operations with locks

### 3. **User Interface Layout**

```
┌─────────────────────────────────────────────────────────────┐
│                    🎤 Voice Chat Header                     │
├─────────────────────────────────────────────────────────────┤
│ Sidebar:           │              Main Chat Area            │
│ • API Key Input    │ • Chat History Display                 │
│ • LLM Initialize   │ • User Messages (right-aligned)        │
│ • Message Counter  │ • AI Responses (left-aligned)          │
│ • Clear Chat       │ • Audio Players for voice messages     │
├─────────────────────────────────────────────────────────────┤
│ Input Section:                                              │
│ • Voice Input (🎤 Start Recording)                          │
│ • Text Input (📝 Type Message)                              │
└─────────────────────────────────────────────────────────────┘
```

### 4. **Detailed Workflow**

#### **A. Initialization Phase**
1. **Page Setup**: Configure Streamlit page properties and custom CSS
2. **Session State**: Initialize chat bot, history, and LLM status
3. **API Configuration**: User enters Google Gemini API key
4. **LLM Initialization**: 
   - Configure Google Generative AI
   - Create ChatGoogleGenerativeAI instance
   - Setup ConversationChain with memory

#### **B. Voice Input Flow**
```
User clicks "🎤 Start Recording"
         ↓
Microphone captures audio (8s timeout)
         ↓
Ambient noise adjustment
         ↓
Audio saved to temporary WAV file
         ↓
Google Speech Recognition converts to text
         ↓
Text displayed to user for confirmation
         ↓
Process with LLM (next phase)
```

#### **C. Text Input Flow**
```
User types message in text area
         ↓
User clicks "Send Message"
         ↓
Text stored in session state
         ↓
Process with LLM (next phase)
```

#### **D. AI Processing Flow**
```
User input (voice/text) received
         ↓
ConversationChain processes with Gemini AI
         ↓
AI response generated with conversation context
         ↓
Response stored in chat history
         ↓
Text-to-Speech conversion initiated
```

#### **E. Text-to-Speech Flow**
```
AI response text received
         ↓
Text cleaning (remove markdown, limit length)
         ↓
Thread-safe TTS engine initialization
         ↓
Speech generation to temporary WAV file
         ↓
Engine cleanup and resource release
         ↓
Audio file validation and storage
```

#### **F. Response Display Flow**
```
Chat history updated with new messages
         ↓
UI re-rendered with new conversation
         ↓
Text response displayed in styled container
         ↓
Audio player embedded for voice response
         ↓
Temporary files managed for cleanup
```

### 5. **Key Features**

#### **🎯 Core Functionality**
- **Bidirectional Communication**: Voice input → AI processing → Voice output
- **Multi-modal Input**: Both voice and text input supported
- **Conversation Memory**: Maintains context across interactions
- **Real-time Processing**: Immediate response generation and audio conversion

#### **🔧 Technical Highlights**
- **Thread Safety**: TTS operations protected with threading locks
- **Resource Management**: Proper cleanup of TTS engines and temporary files
- **Error Handling**: Comprehensive error handling for speech recognition and TTS
- **Session Persistence**: Chat history maintained during app session

### 6. **Error Handling & Edge Cases**

#### **Speech Recognition Errors**
- **Timeout**: 8-second listening limit with user feedback
- **Unclear Speech**: Recognition failure handling
- **API Errors**: Network/service error management

#### **TTS Engine Issues**
- **Engine Reinitialization**: Fresh engine creation for each conversion
- **Resource Cleanup**: Proper engine disposal to prevent memory leaks
- **Audio Validation**: File existence and size verification

### 7. **File Structure & Dependencies**

#### **Core Dependencies**
```python
streamlit              # Web app framework
speech_recognition     # Voice input processing
pyttsx3               # Text-to-speech conversion
langchain_google_genai # Google Gemini AI integration
google.generativeai    # Google AI API
tempfile              # Temporary file management
threading             # Thread-safe operations
```

#### **Data Flow**
```
User Input → Speech Recognition → LLM Processing → TTS Generation → UI Display
     ↓              ↓                   ↓              ↓            ↓
Audio/Text → Transcription → AI Response → Audio File → Chat Interface
```

### 8. **Session Management**

- **Chat History**: Persistent conversation storage during session
- **Memory Buffer**: LangChain conversation memory for context
- **State Management**: Streamlit session state for app persistence
- **File Cleanup**: Automatic temporary file management

### 9. **User Experience Flow**

1. **Setup**: Enter API key and initialize LLM
2. **Interact**: Choose voice or text input method
3. **Communicate**: Speak or type message
4. **Receive**: Get AI response in both text and audio format
5. **Continue**: Maintain conversation with full context
6. **Manage**: Clear chat history when needed

This application provides a seamless voice-first AI interaction experience with robust error handling and professional UI design.
