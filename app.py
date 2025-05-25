import streamlit as st
import google.generativeai as genai
from utils import load_files, store_in_chroma
import os
from dotenv import load_dotenv

load_dotenv()
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

st.set_page_config(page_title="DEVMIND", layout="wide")
st.title("DevMind : Second Brain for Developers")

# Initialize session state for multi-turn memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
if "chat_responses" not in st.session_state:
    st.session_state.chat_responses = []


# Load and embed docs
with st.spinner("Loading your knowledge base..."):
    docs = load_files()
    collection = store_in_chroma(docs)


# --- SIDEBAR (Chat History) ---

with st.sidebar:

    st.header("🕓 Chat History")

    if st.session_state.chat_history:

        for i, q in enumerate(st.session_state.chat_history):

            st.markdown(f"**{i+1}.** {q}")

    else:
        st.info("No previous chats.")

# --- MAIN CHAT DISPLAY ---

chat_container = st.container()
with chat_container:
    for i, question in enumerate(st.session_state.chat_history):
        st.markdown(f"**🙋 You:** {question}")
        if i < len(st.session_state.chat_responses):
            st.markdown(f"**🤖 Gemini:** {st.session_state.chat_responses[i]}")

# User input
query = st.text_input("Ask your codebase a question...")
if query:
    st.session_state.chat_history.append(query)

    # If it looks like code (simple heuristic)
    if any(keyword in query for keyword in ["print", "def", "class", "import", "=", ":", "{", "}"]):
        st.subheader("🧠 Code Explanation")
        code_explanation_prompt = f"Explain this code clearly for a beginner:\n\n{query}"
        code_explanation = model.generate_content(code_explanation_prompt)
        st.markdown(f"**💡 Gemini Answer:**\n\n{code_explanation.text}")
    else:
        # Combine last 3 turns for context
        full_query_context = "\n".join(st.session_state.chat_history[-3:])

        # Chroma search
        results = collection.query(query_texts=[full_query_context], n_results=3)
        relevant_texts = results["documents"][0]

        # Full context to Gemini
        full_context = "\n\n".join(relevant_texts)
        prompt = f"Answer the user's question based on this context:\n\n{full_context}\n\nQuestion: {query}"
        response = model.generate_content(prompt)

        # Show Gemini Answer
        st.subheader("💡 Gemini Answer")
        st.write(response.text)
        st.session_state.chat_responses.append(response.text)

        st.subheader("🔍 Top Matches")
        for i, text in enumerate(relevant_texts):
            with st.expander(f"Match {i+1}"):
                st.code(text[:500], language="python")  # Trim if too long

                col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

                if col1.button("🔍 Explain", key=f"explain_{i}", use_container_width=True):
                    explain_prompt = f"Explain this code:\n\n{text}"
                    explanation = model.generate_content(explain_prompt)
                    st.markdown(f"**🧠 Explanation:**\n\n{explanation.text}")

                if col2.button("🌐 Convert JS", key=f"convert_{i}", use_container_width=True):
                    convert_prompt = f"Convert this Python code to JavaScript:\n\n{text}"
                    conversion = model.generate_content(convert_prompt)
                    st.code(conversion.text, language="javascript")

                if col3.button("🧪 Tests", key=f"test_{i}", use_container_width=True):
                    test_prompt = f"Write unit tests for this code:\n\n{text}"
                    tests = model.generate_content(test_prompt)
                    st.code(tests.text, language="python")

                if col4.button("🔧 Refactor", key=f"refactor_{i}", use_container_width=True):
                    refactor_prompt = f"Refactor this code for better readability and performance:\n\n{text}"
                    refactor = model.generate_content(refactor_prompt)
                    st.code(refactor.text, language="python")

                if col5.button("📄 README", key=f"readme_{i}", use_container_width=True):
                    readme_prompt = f"Generate a README.md section for this code. Include a short description, usage example, and installation instructions if applicable:\n\n{text}"
                    readme = model.generate_content(readme_prompt)
                    st.markdown(f"**📘 README:**\n\n```\n{readme.text.strip()}\n```")
