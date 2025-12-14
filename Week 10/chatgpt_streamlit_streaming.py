import streamlit as st
from chatgpt_secure import client  # your secure client

model = "gpt-3.5-turbo-0125"  
temperature = 0.7

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Display existing chat history
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Wait for user input
prompt = st.chat_input("Ask something...")
if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # STREAMING response
    with st.chat_message("assistant"):
        container = st.empty()
        full_reply = ""

        stream = client.chat.completions.create(
            model=model,
            messages=st.session_state.messages,
            temperature=temperature,
            stream=True       # ✅ correct streaming flag
        )

        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                full_reply += delta.content
                container.markdown(full_reply + "▌")

        container.markdown(full_reply)

    # Save AI reply
    st.session_state.messages.append(
        {"role": "assistant", "content": full_reply}
    )
