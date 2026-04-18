import streamlit as st
from core import generate_handoff

st.set_page_config(
    page_title="ContextBridge",
    page_icon="🌉",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

#MainMenu, footer, header { visibility: hidden; }

html, body, .stApp {
    background: #0f0f11;
    color: #e5e7eb;
}

.cb-topbar {
    position: fixed;
    top: 0; left: 0;
    width: 100%;
    height: 64px;
    padding: 0 32px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    background: rgba(15,15,17,0.85);
    backdrop-filter: blur(10px);
    z-index: 1000;
}

.cb-topbar-inner { display: flex; align-items: center; gap: 10px; }

.cb-logo-icon {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
}

.cb-logo-text { font-size: 1.05rem; font-weight: 600; color: #e2e8f0; }

.stApp::before, .stApp::after {
    content: "";
    position: fixed;
    width: 280px; height: 280px;
    border-radius: 50%;
    filter: blur(70px);
    pointer-events: none;
    z-index: 0;
}

.stApp::before {
    top: 20%; left: 8%;
    background: rgba(139,92,246,0.18);
    animation: floatLeft 18s ease-in-out infinite;
}

.stApp::after {
    bottom: 15%; right: 10%;
    background: rgba(99,102,241,0.18);
    animation: floatRight 22s ease-in-out infinite;
}

body::after {
    content: "";
    position: fixed;
    width: 240px; height: 240px;
    top: 60%; left: 40%;
    border-radius: 50%;
    background: rgba(139,92,246,0.12);
    filter: blur(60px);
    animation: floatCenter 20s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes floatLeft {
    0% { transform: translate(0,0); }
    50% { transform: translate(40px,-50px); }
    100% { transform: translate(0,0); }
}

@keyframes floatRight {
    0% { transform: translate(0,0); }
    50% { transform: translate(-40px,40px); }
    100% { transform: translate(0,0); }
}

@keyframes floatCenter {
    0% { transform: translate(0,0); }
    50% { transform: translate(20px,-30px); }
    100% { transform: translate(0,0); }
}

.main .block-container {
    max-width: 720px;
    margin: 0 auto;
    padding-top: 100px;
    padding-bottom: 4rem;
    position: relative;
    z-index: 1;
}

.cb-header { margin-bottom: 2.5rem; }

.cb-headline {
    font-size: 2.6rem;
    font-weight: 700;
    color: #f8fafc;
    line-height: 1.2;
}

.cb-subheadline { color: #94a3b8; }

.cb-label { font-size: 0.85rem; color: #94a3b8; margin-bottom: 0.4rem; }

.stSelectbox > div > div {
    background-color: #1a1a2e !important;
    border: 1px solid #2d2d44 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

.stTextArea textarea {
    background-color: #13131f !important;
    border: 1px solid #2d2d44 !important;
    border-radius: 16px !important;
    color: #cbd5e1 !important;
    padding: 18px !important;
}

.stTextArea textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.18) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border-radius: 10px !important;
    width: 100% !important;
}

.output-card {
    background: #13131f;
    border: 1px solid #2d2d44;
    border-radius: 16px;
    padding: 28px 32px;
    margin-top: 1.5rem;
    white-space: pre-wrap;  /* preserves formatting of the card */
}
</style>
""", unsafe_allow_html=True)

# ---------- TOP BAR ----------
st.markdown("""
<div class="cb-topbar">
    <div class="cb-topbar-inner">
        <div class="cb-logo-icon">⇄</div>
        <span class="cb-logo-text">ContextBridge</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- UI ----------
st.markdown("""
<div class="cb-header">
    <div class="cb-headline">Hit your limit.<br>Don't lose your work.</div>
    <div class="cb-subheadline">
    Paste any AI conversation and get a structured handoff card.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="cb-label">What were you working on?</div>', unsafe_allow_html=True)

mode = st.selectbox(
    "",
    ["Continue coding", "Continue writing", "Continue research", "Continue problem solving"],
    label_visibility="collapsed"
)

st.markdown('<div style="height: 20px"></div>', unsafe_allow_html=True)

conversation = st.text_area(
    "Paste your conversation",
    height=280,
    placeholder="Paste your full conversation with Claude, ChatGPT, Gemini, or any AI here...",
    label_visibility="collapsed"
)

st.markdown('<div style="height: 8px"></div>', unsafe_allow_html=True)

if st.button("Generate Handoff Card"):
    if not conversation.strip():
        st.warning("Paste a conversation first.")
    else:
        # THIS was the missing piece — spinner + error handling
        with st.spinner("Generating your handoff card..."):
            try:
                result = generate_handoff(conversation, mode)
                st.markdown(
                    f"<div class='output-card'>{result}</div>",
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")