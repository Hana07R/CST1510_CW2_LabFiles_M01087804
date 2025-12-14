import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

def run_page():
    st.title("🔒 Security Threats")

    num_records = 10
    types = ["Unauthorized Access", "Malware", "Vulnerability", "DDoS"]
    severities = ["Low", "Medium", "High", "Critical"]
    statuses = ["Active", "Mitigated", "Resolved"]

    data = {
        "Date": [datetime.today() - timedelta(days=random.randint(0,30)) for _ in range(num_records)],
        "Threat Type": [random.choice(types) for _ in range(num_records)],
        "Severity": [random.choice(severities) for _ in range(num_records)],
        "Status": [random.choice(statuses) for _ in range(num_records)],
        "Reported By": [f"user{random.randint(1,5)}" for _ in range(num_records)]
    }

    df = pd.DataFrame(data)
    st.subheader("Recent Security Threats")
    st.dataframe(df)

    # Metrics
    st.subheader("Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Threats", len(df))
    col2.metric("Active", len(df[df["Status"]=="Active"]))
    col3.metric("Critical", len(df[df["Severity"]=="Critical"]))
