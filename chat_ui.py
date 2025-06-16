import streamlit as st
import requests
import csv

st.set_page_config(page_title="AI Therapy Bot", page_icon="🧠")
st.title("🧠 AI Therapy Bot")

# Step 1: Get user name once
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if st.session_state.user_name == "":
    st.session_state.user_name = st.text_input("Enter your name to start:", key="name_input")
    if not st.session_state.user_name:
        st.stop()
    else:
        st.success(f"Welcome, {st.session_state.user_name}!")

# Step 2: Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    role = "🧍 You" if msg["role"] == "user" else "🤖 Therapy Bot"
    st.markdown(f"**{role}:** {msg['text']}")

# Input field
user_input = st.text_input("Your Message:", key="user_input")

if st.button("Send"):
    if user_input.strip():
        st.session_state.messages.append({"role": "user", "text": user_input})

        try:
            response = requests.post("http://127.0.0.1:5000/analyze", json={"text": user_input})
            if response.status_code == 200:
                result = response.json()
                emotion = result['emotion']
                confidence = result['confidence']

                # Supportive reply
                suggestions = {
                    "sadness": "I'm really sorry you're feeling down. Want to talk about what's bothering you?",
                    "joy": "That's wonderful! Tell me more about what's making you feel happy 😊",
                    "anger": "It’s okay to feel angry. I'm here if you want to let it out.",
                    "fear": "That must feel overwhelming. Would talking about it help?",
                    "surprise": "Wow! That sounds unexpected. Want to share more?",
                    "love": "Love is beautiful. I'm glad you're feeling this way!",
                    "neutral": "I'm here to listen — tell me anything on your mind."
                }

                bot_reply = suggestions.get(emotion.lower(), "I'm here to support you.")
                full_bot_msg = f"{bot_reply} (Detected: *{emotion}*, Confidence: *{confidence}*)"

                st.session_state.messages.append({"role": "bot", "text": full_bot_msg})

                # Save to CSV
                log_file = f"chat_log_{st.session_state.user_name.lower()}.csv"
                with open(log_file, "a", newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["User", user_input])
                    writer.writerow(["Bot", bot_reply])
            else:
                st.error("Backend error. Please try again.")
        except requests.exceptions.RequestException:
            st.error("❌ Cannot connect to backend. Please ensure Flask server is running.")
    else:
        st.warning("Please enter some text.")
