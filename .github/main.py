import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# ✅ Set page configuration FIRST
st.set_page_config(
    page_title="Virtual AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ✅ Load API key securely from Streamlit Secrets
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("❌ Google API key not found in Streamlit Secrets.")
    st.stop()

# ✅ Initialize Gemini model using LangChain
try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7)
except Exception as e:
    st.error(f"🚨 Failed to initialize Gemini model: {e}")
    st.stop()

# ✅ Streamlit Chat UI
st.title("🤖 Virtual AI Assistant")
st.markdown("Ask me anything and I’ll do my best to help!")

# ✅ Chat session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! How can I assist you today?"}
    ]

# ✅ Display past messages
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✅ Handle new user input
if prompt := st.chat_input("Type your message here..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            response = llm.invoke(prompt)

            # ✅ Stream response word by word, with formatting
            for chunk in response.content.split():
                full_response += chunk + " "
                message_placeholder.markdown(full_response + "▌")

            # ✅ Format newlines and proper markdown
            formatted_response = full_response.replace("* ", "\n\n* ").replace(". ", ".\n\n")
            message_placeholder.markdown(formatted_response.strip())

            st.session_state["messages"].append({"role": "assistant", "content": formatted_response.strip()})

        except Exception as e:
            st.error(f"❌ Error from Gemini: {e}")
            st.session_state["messages"].append({"role": "assistant", "content": f"Sorry, something went wrong: {e}"})
            message_placeholder.markdown(f"Sorry, something went wrong: {e}")
