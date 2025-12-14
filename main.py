import os
import sqlite3
import bcrypt
import streamlit as st
import pandas as pd
import importlib

# ----------------------------
# Dynamically import all pages
# ----------------------------
pages_path = os.path.join(os.path.dirname(__file__), "Week11", "pages")
pages_modules = {}
for file in os.listdir(pages_path):
    if file.endswith(".py") and file != "__init__.py":
        module_name = file[:-3]
        pages_modules[module_name] = importlib.import_module(f"Week11.pages.{module_name}")

# ----------------------------
# Database setup
# ----------------------------
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "DATA")
DB_FILE = os.path.join(DATA_FOLDER, "intelligence_platform.db")
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

def connect_database():
    return sqlite3.connect(DB_FILE)

def create_tables():
    conn = connect_database()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            incident_type TEXT,
            severity TEXT,
            status TEXT,
            description TEXT,
            reported_by TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets(
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            priority TEXT,
            assigned_to TEXT,
            created_on TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS security_threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            threat_type TEXT,
            severity TEXT,
            status TEXT,
            description TEXT,
            reported_by TEXT
        )
    """)
    conn.commit()
    conn.close()

# ----------------------------
# User functions
# ----------------------------
def register_user(username, password, role="user"):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, f"Username '{username}' already exists."
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, hashed, role)
    )
    conn.commit()
    conn.close()
    return True, f"User '{username}' registered successfully!"

def login_user(username, password):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return False, "Username not found."
    stored_hash = user[2]
    if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
        return True, f"Welcome, {username}!"
    return False, "Invalid password."

# ----------------------------
# Login/Register page
# ----------------------------
def show_login_register():
    st.title("🔐 Login / Register")

    # --- Register ---
    st.subheader("Register")
    reg_user = st.text_input("Username", key="reg_user")
    reg_pass = st.text_input("Password", type="password", key="reg_pass")
    reg_role = st.selectbox("Role", ["user", "analyst", "admin"], key="reg_role")
    if st.button("Register"):
        if not reg_user or not reg_pass:
            st.warning("Please enter both username and password.")
        else:
            success, msg = register_user(reg_user, reg_pass, reg_role)
            if success:
                st.success(msg)
            else:
                st.error(msg)

    st.markdown("---")

    # --- Login ---
    st.subheader("Login")
    login_user_input = st.text_input("Username", key="login_user")
    login_pass_input = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        if not login_user_input or not login_pass_input:
            st.warning("Please enter both username and password.")
        else:
            success, msg = login_user(login_user_input, login_pass_input)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = login_user_input
                conn = connect_database()
                role_df = pd.read_sql(
                    f"SELECT role FROM users WHERE username='{login_user_input}'", conn
                )
                st.session_state.role = role_df.iloc[0]["role"]
                conn.close()
                st.session_state.page = "Home"
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

# ----------------------------
# Main app
# ----------------------------
def run_app():
    st.set_page_config(page_title="Intelligence Platform", layout="wide")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.session_state.page = "Home"

    if not st.session_state.logged_in:
        show_login_register()
        return

    # ----------------------------
    # Sidebar
    # ----------------------------
    st.sidebar.title("Navigation")
    st.sidebar.markdown(f"**Welcome, {st.session_state.username}**")
    pages = ["Home", "Cyber Incidents", "Security Threats"]
    if st.session_state.role in ["admin", "analyst"]:
        pages.extend(["IT Tickets", "AI Assistant", "Admin Panel", "Analyst Tools"])

    if not st.session_state.page or st.session_state.page == "":
        st.session_state.page = "Home"

    st.session_state.page = st.sidebar.radio("Go to:", pages, index=pages.index(st.session_state.page))
    st.sidebar.markdown("---")
    st.sidebar.write(f"**User:** {st.session_state.username}")
    st.sidebar.write(f"**Role:** {st.session_state.role}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.session_state.page = "Home"
        st.rerun()

    # ----------------------------
    # Page routing
    # ----------------------------
    page_name_map = {
        "Home": "Home",
        "Cyber Incidents": "Cyber_Incidents",
        "Security Threats": "Security_Threats",
        "IT Tickets": "IT_Tickets",
        "AI Assistant": "AI_Assistant",
        "Admin Panel": "Admin_Panel",
        "Analyst Tools": "Analyst_Tools"
    }

    module_name = page_name_map.get(st.session_state.page)
    if module_name and module_name in pages_modules:
        page_module = pages_modules[module_name]
        if hasattr(page_module, "run_page"):
            page_module.run_page()
        elif hasattr(page_module, "run_home"):
            page_module.run_home()

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    create_tables()
    run_app()  