import streamlit as st
import requests


# --------------------------------
# Page Configuration
# --------------------------------

st.set_page_config(
    page_title="College AI Assistant",
    page_icon="🎓",
    layout="centered"
)


# --------------------------------
# Header
# --------------------------------

st.title("🎓 College AI Assistant")

st.write(
    "Ask questions about college regulations, "
    "placements, internships and other college documents."
)


# --------------------------------
# Question Input
# --------------------------------

question = st.text_input(
    "Ask your question:",
    placeholder="Example: What are the placement guidelines?"
)


# --------------------------------
# Ask AI
# --------------------------------

if st.button("Ask AI"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching college documents..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/ask",
                    json={
                        "question": question
                    }
                )

                if response.status_code == 200:

                    data = response.json()

                    st.success("Answer")

                    st.write(data["answer"])

                else:

                    st.error(
                        f"Backend error: {response.status_code}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to FastAPI. "
                    "Make sure the backend is running."
                )

            except Exception as e:

                st.error(f"Error: {e}")
