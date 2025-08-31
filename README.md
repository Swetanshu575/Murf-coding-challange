🎙️ AI Voice Assistant & Dubbing Studio

An AI-powered voice assistant and dubbing tool built with Streamlit, Groq LLM, and Murf TTS API.
It allows natural conversation with an AI assistant that can adopt personas (like a Doctor), generate context-aware responses, and convert them into realistic speech using Murf.

🚀 Features

💬 Chat with AI (powered by Groq LLM)

🩺 Persona-based system prompts (e.g., City Doctor)

🔊 Text-to-Speech conversion with Murf API

🎧 Auto-play audio replies

🎭 Multiple voice options (US, UK, FR voices)

🎬 Future-ready dubbing support with MoviePy & FFmpeg

🛠️ Tech Stack

Streamlit
 – UI & Chat Interface

Groq
 – Fast LLM inference

Murf AI
 – Text-to-Speech API

Requests
 – REST API calls

MoviePy
 & FFmpeg
 – (optional) dubbing & video processing

📦 Installation

Clone the repo:

git clone https://github.com/your-username/murf-coding-challange.git
cd murf-coding-challange


Install dependencies:

pip install -r requirements.txt

🔑 API Keys Setup

Create a .env file (or use Streamlit secrets.toml) with:

GROQ_API_KEY=your_groq_api_key
MURF_API_KEY=your_murf_api_key


For Streamlit Cloud → add these under Project Settings → Secrets.

▶️ Run the App
streamlit run app.py


Then open your browser at http://localhost:8501
 🎉

📖 How It Works

User types a message → sent to Groq LLM for response generation.

AI reply is styled and shown in chat interface.

Response is converted into speech using Murf API.

Audio playback happens automatically (if enabled).

🎯 Use Cases

AI Medical Assistant 🩺

Podcast & Video Dubbing 🎬

Accessibility Voice Narration ♿

Language Learning Tools 🌍

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

📜 License

This project is licensed under the MIT License.
