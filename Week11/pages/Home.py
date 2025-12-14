import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime, timedelta

def run_page():
    st.title(f"🏠 Dashboard")
    
    username = st.session_state.get("username", "User")
    role = st.session_state.get("role", "user")
    
    st.subheader(f"Welcome, {username}! ({role})")
    st.markdown("---")
    
    # ---------- Sample Overview Metrics ----------
    st.subheader("Platform Overview")
    col1, col2, col3, col4 = st.columns(4)

    cyber_incidents = random.randint(10, 50)
    it_tickets = random.randint(5, 30)
    security_threats = random.randint(2, 20)
    ai_queries = random.randint(50, 200)

    col1.metric("Cyber Incidents", cyber_incidents)
    col2.metric("IT Tickets", it_tickets)
    col3.metric("Security Threats", security_threats)
    col4.metric("AI Queries", ai_queries)

    st.markdown("---")

    # ---------- Sample Trend Chart ----------
    st.subheader("Incidents Trend (Last 7 Days)")
    dates = [datetime.today() - timedelta(days=i) for i in range(6, -1, -1)]
    incidents = [random.randint(0, 10) for _ in range(7)]
    df = pd.DataFrame({"Date": dates, "Incidents": incidents})

    fig = px.line(df, x="Date", y="Incidents", markers=True)
    fig.update_layout(yaxis_title="Number of Incidents", xaxis_title="Date", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    # ---------- Quick Links ----------
    st.subheader("Quick Actions")
    st.markdown("""
    - View all **Cyber Incidents**
    - Manage **IT Tickets**
    - Monitor **Security Threats**
    - Access **AI Assistant**
    """)
