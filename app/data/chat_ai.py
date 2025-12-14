import streamlit as st

def show():
    st.header("AI Assistant")
    st.write("This is a placeholder for the AI Assistant.")
    user_input = st.text_area("Ask a question:")
    if st.button("Get AI Response"):
        if user_input.strip() == "":
            st.warning("Please enter a question.")
        else:
            # Placeholder response
            st.success(f"AI Response: I received your question: '{user_input}'")
