import streamlit as st
import openai

# ---------- CONFIG ----------
st.set_page_config(layout="wide")
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"

# ---------- Personality Setup ----------
if "ai_personality" not in st.session_state:
    st.session_state.ai_personality = ""
    st.session_state.show_personality_input = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": st.session_state.ai_personality}
    ]

# ---------- Top UI ----------
col1, col2 = st.columns([8, 1])
with col1:
    st.header("💬 Hello, what can I do for you?")
with col2:
    if st.button("🧹 Clear"):
        st.session_state.chat_history = [
            {"role": "system", "content": st.session_state.ai_personality}
        ]
        st.rerun()

# Show personality input
if st.button("✨ Get better experience"):
    st.session_state.show_personality_input = True

if st.session_state.show_personality_input:
    personality = st.text_input("Describe how the AI should behave (e.g. funny, helpful, expert in science):", key="personality_input")
    if personality:
        st.session_state.ai_personality = personality
        st.session_state.chat_history = [
            {"role": "system", "content": st.session_state.ai_personality}
        ]
        st.session_state.show_personality_input = False
        st.rerun()

# ---------- Display Chat ----------
for msg in st.session_state.chat_history[1:]:  # skip system message
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**AI:** {msg['content']}")

# ---------- CSS for Bottom Input ----------
st.markdown("""
    <style>
    .bottom-form {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 1rem;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.15);
        z-index: 1000;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Input Form at Bottom ----------
st.markdown('<div class="bottom-form">', unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    que = st.text_input("Type your message here...", label_visibility="collapsed")
    send = st.form_submit_button("Send")
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Handle Chat Request ----------
if send and que:
    st.session_state.chat_history.append({"role": "user", "content": que})

    response = openai.ChatCompletion.create(
        model="mistralai/mistral-7b-instruct:free",
        messages=st.session_state.chat_history
    )
    reply = response['choices'][0]['message']['content']
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.rerun()
