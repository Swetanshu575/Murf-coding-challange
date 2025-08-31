import streamlit as st
import requests
import os
from datetime import datetime
from typing import Optional

# APIs
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except Exception:
    GROQ_AVAILABLE = False
    st.warning("⚠️ Groq SDK not installed.")

try:
    from murf import Murf, MurfDub
    MURF_AVAILABLE = True
except Exception:
    MURF_AVAILABLE = False
    st.warning("⚠️ Murf SDK not installed.")

# Streamlit config
st.set_page_config(page_title="AI Voice Assistant & Dubbing Studio", page_icon="🎙️", layout="wide")

# CSS styling
st.markdown("""
<style>
.chat-message { padding: 1rem; border-radius: 10px; margin: 1rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
.user-message { background: linear-gradient(135deg, #667eea, #764ba2); color: white; margin-left:20%;}
.assistant-message { background: linear-gradient(135deg, #f093fb, #f5576c); color: white; margin-right:20%;}
</style>
""", unsafe_allow_html=True)

VOICE_OPTIONS = {
    "en-US-terrell": "Terrell (US Male)",
    "en-US-natalie": "Natalie (US Female)",
    "en-US-ariana": "Ariana (US Female)",
    "en-UK-ruby": "Ruby (UK Female)",
    "fr-FR-axel": "Axel (FR Male)"
}

# 🔑 Hardcoded API Keys (replace with your actual keys)
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
MURF_API_KEY = st.secrets.get("MURF_API_KEY", os.getenv("MURF_API_KEY"))
# 🎭 Hardcoded System Prompt
SYSTEM_PROMPT = "You are the doctor of the city. As a doctor, explain and diagnose health issues clearly."

class AIVoiceAssistant:
    def __init__(self):
        self.groq = None
        self.murf = None
        self.murfdub = None
        self.init_state()
        self.setup_clients()

    def init_state(self):
        if 'history' not in st.session_state: 
            st.session_state.history = []
        if 'auto_play' not in st.session_state: 
            st.session_state.auto_play = True

    def setup_clients(self):
        if GROQ_API_KEY and GROQ_AVAILABLE:
            self.groq = Groq(api_key=GROQ_API_KEY)
        if MURF_API_KEY and MURF_AVAILABLE:
            self.murf = Murf(api_key=MURF_API_KEY)
            self.murfdub = MurfDub(api_key=MURF_API_KEY)

    def generate_response(self, msg: str) -> str:
        if not self.groq:
            return "❌ Groq not configured."
        
        history = [{"role": "system", "content": SYSTEM_PROMPT}] + \
                  [{"role": m["role"], "content": m["content"]} for m in st.session_state.history[-10:]]
        history.append({"role": "user", "content": msg})

        resp = self.groq.chat.completions.create(
            model="qwen/qwen3-32b", messages=history, temperature=0.7, max_tokens=500
        )
        return resp.choices[0].message.content

    def text_to_speech(self, text: str, voice_id: str) -> Optional[bytes]:
        if not self.murf:
            return None
        try:
            resp = self.murf.text_to_speech.generate(text=text, voice_id=voice_id)
            url = getattr(resp, "audio_file", None)
            if url:
                r = requests.get(url)
                r.raise_for_status()
                return r.content
            st.error("❌ No audio_file in Murf response.")
        except Exception as e:
            st.error(f"❌ TTS error: {e}")
        return None

    def run(self):
        st.title("🎙️ AI Doctor Assistant")
        st.caption("Persona: 🩺 The City Doctor – Ask me for diagnoses and medical advice.")

        col1, col2 = st.columns([2,1])
        voice = col1.selectbox("Select Voice", options=list(VOICE_OPTIONS.keys()), format_func=lambda x: VOICE_OPTIONS[x])
        st.session_state.auto_play = col2.checkbox("Auto-play Audio", value=st.session_state.auto_play)

        user_msg = st.chat_input("Your message>")
        if user_msg:
            st.session_state.history.append({"role": "user", "content": user_msg})
            ai_msg = self.generate_response(user_msg)
            audio = self.text_to_speech(ai_msg, voice)
            st.session_state.history.append({"role": "assistant", "content": ai_msg, "audio": audio})
            st.rerun()

        for msg in st.session_state.history:
            ts = datetime.fromisoformat(msg.get("timestamp", datetime.now().isoformat())).strftime("%H:%M:%S")
            if msg["role"] == "user":
                st.markdown(f"<div class='chat-message user-message'>👤 You: {msg['content']}<br><small>{ts}</small></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-message assistant-message'>🤖 Doctor AI: {msg['content']}<br><small>{ts}</small></div>", unsafe_allow_html=True)
                if msg.get("audio") and st.session_state.auto_play:
                    st.audio(msg["audio"], format="audio/wav")

def main():
    app = AIVoiceAssistant()
    app.run()

if __name__ == "__main__":
    main()
