import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

def run_page():
    st.title("💻 IT Tickets")

    num_records = 10
    priorities = ["Low", "Medium", "High", "Urgent"]
    statuses = ["Open", "In Progress", "Resolved"]

    data = {
        "Ticket ID": [i+1 for i in range(num_records)],
        "Title": [f"Issue {i+1}" for i in range(num_records)],
        "Priority": [random.choice(priorities) for _ in range(num_records)],
        "Status": [random.choice(statuses) for _ in range(num_records)],
        "Assigned To": [f"analyst{random.randint(1,3)}" for _ in range(num_records)],
        "Created On": [datetime.today() - timedelta(days=random.randint(0,30)) for _ in range(num_records)]
    }

    df = pd.DataFrame(data)
    st.subheader("Recent IT Tickets")
    st.dataframe(df)

    # Metrics
    st.subheader("Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tickets", len(df))
    col2.metric("Open", len(df[df["Status"]=="Open"]))
    col3.metric("High Priority", len(df[df["Priority"]=="High"]))
