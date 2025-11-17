import streamlit as st
from chatbot_core import ask_chatbot
from memory_engine import load_long_memory
import base64
from avatar_loader import load_avatar
from PIL import Image


# ---------------------------
# Dark Theme CSS
# ---------------------------
dark_css = """
<style>
body {
    background-color: #0d0d0d;
    color: #e6e6e6;
}
[data-testid="stSidebar"] {
    background-color: #1a1a1a;
}

.user-bubble {
    background: #333333;
    color: white;
    padding: 10px 15px;
    border-radius: 12px;
    max-width: 60%;
    margin-left: auto;
    margin-right: 0;
    margin-bottom: 10px;
}

.bot-bubble {
    background: #262626;
    color: #f2f2f2;
    padding: 10px 15px;
    border-radius: 12px;
    max-width: 60%;
    margin-right: auto;
    margin-left: 0;
    margin-bottom: 10px;
}

.right-align {
    display: flex;
    justify-content: flex-end;
    align-items: center;
}

.left-align {
    display: flex;
    justify-content: flex-start;
    align-items: center;
}

.avatar-img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
    margin: 0 8px;
}
</style>
"""
st.markdown(dark_css, unsafe_allow_html=True)


# ---------------------------
# Page Config
# ---------------------------
icon = Image.open("assets/got_logo.png")

st.set_page_config(page_title="GOT Chatbot", page_icon=icon, layout="wide")

# Load image as base64
from avatar_loader import load_avatar

banner = load_avatar("assets/got_logo.jpg")

st.markdown(
    f"""
    <div style="
        background-image: url('{banner}');
        background-size: cover;
        background-position: center;
        width: 100%;
        height: 260px;
        border-radius: 14px;
        margin-bottom: 25px;
    ">
    </div>
    """,
    unsafe_allow_html=True,
)


st.write("Ask anything related to GoT lore, characters, events, houses, and history.")


# ---------------------------
# Character Avatar Mapping
# ---------------------------
AVATARS = {
    "tyrion": load_avatar("assets/tyrion.png"),
    "jonsnow": load_avatar("assets/jon.png"),
    "arya": load_avatar("assets/arya.png"),
    "daenerys": load_avatar("assets/daenerys.png"),
    "cersei": load_avatar("assets/cersei.png"),
    "none": load_avatar("assets/raven.png"),
}

USER_ICON = load_avatar("assets/user.png")


# ---------------------------
# Sidebar Settings
# ---------------------------
st.sidebar.header("⚙️ Settings")

character = st.sidebar.selectbox(
    "Choose Character Voice:",
    ["tyrion", "jonsnow", "arya", "daenerys", "cersei", "none"],
)

mode = st.sidebar.selectbox("Choose Mode:", ["lore-expert", "fun-mode", "dark-mode"])

temperature = st.sidebar.slider("Creativity (Temperature)", 0.0, 1.5, 0.7, step=0.1)

# Reset Chat Button
if st.sidebar.button("🗑️ Reset Chat"):
    st.session_state.conversation_history = [
        {"role": "system", "content": "You are a Game of Thrones chatbot."}
    ]
    st.experimental_rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("Made by **NeelDevX** ⚔️")


# ---------------------------
# Initialize Session State
# ---------------------------
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = [
        {"role": "system", "content": "You are a Game of Thrones chatbot."}
    ]

if "long_memory" not in st.session_state:
    st.session_state.long_memory = load_long_memory()


# ---------------------------
# Chat Message Display
# ---------------------------
for msg in st.session_state.conversation_history:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div class="right-align">
                <div class="user-bubble">{msg['content']}</div>
                <img src="{USER_ICON}" class="avatar-img">
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif msg["role"] == "assistant":
        st.markdown(
            f"""
            <div class="left-align">
                <img src="{AVATARS[character]}" class="avatar-img">
                <div class="bot-bubble">{msg['content']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------
# Chat Input Box
# ---------------------------
user_input = st.chat_input("Ask something about Game of Thrones...")

if user_input:
    # Add user message
    st.session_state.conversation_history.append(
        {"role": "user", "content": user_input}
    )

    # Right-aligned user bubble
    st.markdown(
        f"""
        <div class="right-align">
            <div class="user-bubble">{user_input}</div>
            <img src="{USER_ICON}" class="avatar-img">
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Generate reply
    reply = ask_chatbot(
        conversation_history=st.session_state.conversation_history,
        character=character,
        mode=mode,
        temperature=temperature,
        long_memory=st.session_state.long_memory,
    )

    # Add bot reply
    st.session_state.conversation_history.append(
        {"role": "assistant", "content": reply}
    )

    # Left-aligned bot bubble
    st.markdown(
        f"""
        <div class="left-align">
            <img src="{AVATARS[character]}" class="avatar-img">
            <div class="bot-bubble">{reply}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
