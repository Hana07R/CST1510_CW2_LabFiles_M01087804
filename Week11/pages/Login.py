import streamlit as st

def run_page():
    """
    This page is just a placeholder for Login.
    Actual login/register functionality is handled in main.py
    """
    st.title("🔐 Login Page")
    st.write(
        "Please use the login/register form on the main page to access the Multi-Domain Intelligence Platform."
    )
    st.info("After logging in, you will be able to navigate to other pages from the sidebar.")

    # Optional: Show current login status
    if "logged_in" in st.session_state:
        if st.session_state.logged_in:
            st.success(f"Logged in as **{st.session_state.username}** ({st.session_state.role})")
        else:
            st.warning("You are not logged in.")
    else:
        st.warning("You are not logged in.")
