import streamlit as st
import requests
import csv

# Page setup
st.set_page_config(page_title="AI Therapy Bot", page_icon="🧠")
st.title("🧠 AI Therapy Bot")
st.write("Hello! I'm here to support you. How are you feeling today?")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    role = "🧍 You" if msg["role"] == "user" else "🤖 Therapy Bot"
    st.markdown(f"**{role}:** {msg['text']}")

# Input field
user_input = st.text_input("Your Message:", key="input")

if st.button("Send"):
    if user_input.strip():
        # Save user message
        st.session_state.messages.append({"role": "user", "text": user_input})

        try:
            # Send to backend
            response = requests.post("http://127.0.0.1:5000/analyze", json={"text": user_input})
            if response.status_code == 200:
                result = response.json()
                emotion = result['emotion']
                confidence = result['confidence']

                # Emotion-based supportive reply
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

                # Save bot reply
                full_bot_msg = f"{bot_reply} (Detected: *{emotion}*, Confidence: *{confidence}*)"
                st.session_state.messages.append({"role": "bot", "text": full_bot_msg})

                # Save to file
                with open("chat_log.csv", "a", newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["User", user_input])
                    writer.writerow(["Bot", bot_reply])
            else:
                st.error("Backend error. Please try again.")
        except requests.exceptions.RequestException:
            st.error("❌ Cannot connect to backend. Please ensure Flask server is running.")
    else:
        st.warning("Please enter some text.")
