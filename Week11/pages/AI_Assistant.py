import streamlit as st

def run_page():
    st.title("🤖 AI Assistant")
    st.write("Ask me anything about the platform or incidents!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # User input
    user_input = st.text_input("Your question:", key="ai_input")

    if st.button("Send") and user_input:
        # Simple response logic
        response = generate_response(user_input)
        st.session_state.chat_history.append({"user": user_input, "bot": response})
        st.rerun()  # rerun to show updated chat

    # Display chat history
    for chat in reversed(st.session_state.chat_history):
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**AI:** {chat['bot']}")

# Simple response generator
def generate_response(query):
    query = query.lower()
    if "incident" in query:
        return "You can check all cyber incidents in the 'Cyber Incidents' page."
    elif "ticket" in query:
        return "IT tickets are displayed in the 'IT Tickets' page."
    elif "security" in query:
        return "Security threats are listed in the 'Security Threats' page."
    elif "dashboard" in query:
        return "The dashboard overview is on the 'Home' page."
    else:
        return "I'm here to guide you through the platform. Try asking about incidents, tickets, or security threats."  
    