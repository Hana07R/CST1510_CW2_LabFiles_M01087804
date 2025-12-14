import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

def run_page():
    st.title("🛡️ Cyber Incidents")

    # Sample Data
    num_records = 10
    dates = [datetime.today() - timedelta(days=random.randint(0, 30)) for _ in range(num_records)]
    types = ["Phishing", "Malware", "Data Breach", "Ransomware"]
    severities = ["Low", "Medium", "High", "Critical"]
    statuses = ["Open", "Investigating", "Closed"]

    data = {
        "Date": dates,
        "Incident Type": [random.choice(types) for _ in range(num_records)],
        "Severity": [random.choice(severities) for _ in range(num_records)],
        "Status": [random.choice(statuses) for _ in range(num_records)],
        "Reported By": [f"user{random.randint(1,5)}" for _ in range(num_records)]
    }

    df = pd.DataFrame(data)
    st.subheader("Recent Cyber Incidents")
    st.dataframe(df)

    # Metrics
    st.subheader("Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Incidents", len(df))
    col2.metric("Open", len(df[df["Status"]=="Open"]))
    col3.metric("Critical", len(df[df["Severity"]=="Critical"]))
