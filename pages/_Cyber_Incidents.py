import streamlit as st
import pandas as pd
import plotly.express as px

# --- FILE PATH ---
FILE_PATH = r"C:\Users\SAMEENA\OneDrive\Documents\Hana\Programming for Data Communication & Networks\Lab Files 7-12\DATA\cyber_incidents.csv"

# --- LOAD CSV ---
df = pd.read_csv(FILE_PATH)
df.columns = df.columns.str.strip()

st.set_page_config(page_title="Cyber Incidents", layout="wide")
st.title("📄 Cyber Incidents")
st.write("Manage cyber incidents easily using the buttons below.")

# --- SESSION STATE FOR FORM TOGGLES ---
for key in ['show_add', 'show_update', 'show_delete', 'show_ai']:
    if key not in st.session_state:
        st.session_state[key] = False

# --- HORIZONTAL ACTION BUTTONS ---
btn1, btn2, btn3, btn4 = st.columns(4)
with btn1:
    if st.button("➕ Add"): st.session_state.show_add = True
with btn2:
    if st.button("✏️ Update"): st.session_state.show_update = True
with btn3:
    if st.button("🗑 Delete"): st.session_state.show_delete = True
with btn4:
    if st.button("🤖 AI"): st.session_state.show_ai = True

st.write("---")

# --- ADD INCIDENT ---
if st.session_state.show_add:
    st.subheader("➕ Add New Incident")
    with st.form("add_incident"):
        timestamp = st.date_input("Date")
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        category = st.text_input("Category")
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
        description = st.text_area("Description")
        submitted = st.form_submit_button("Add Incident")
        if submitted:
            new_row = pd.DataFrame({
                "timestamp": [timestamp],
                "severity": [severity],
                "category": [category],
                "status": [status],
                "description": [description]
            })
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(FILE_PATH, index=False)
            st.success("Incident added successfully!")
            st.rerun()

# --- UPDATE INCIDENT ---
if st.session_state.show_update:
    st.subheader("✏️ Update Incident")
    update_index = st.number_input("Row Number to Update", 0, len(df)-1, 0)
    if st.button("Load Incident for Update", key="load_update"):
        row = df.iloc[update_index]
        timestamp = st.date_input("Date", pd.to_datetime(row['timestamp']), key="update_date")
        severity = st.selectbox(
            "Severity", ["Low", "Medium", "High", "Critical"],
            index=["Low", "Medium", "High", "Critical"].index(row['severity']),
            key="update_severity"
        )
        category = st.text_input("Category", row['category'], key="update_category")
        status = st.selectbox(
            "Status", ["Open", "In Progress", "Resolved", "Closed"],
            index=["Open", "In Progress", "Resolved", "Closed"].index(row['status']),
            key="update_status"
        )
        description = st.text_area("Description", row['description'], key="update_desc")
        if st.button("Update Incident", key="update_btn"):
            df.at[update_index, 'timestamp'] = timestamp
            df.at[update_index, 'severity'] = severity
            df.at[update_index, 'category'] = category
            df.at[update_index, 'status'] = status
            df.at[update_index, 'description'] = description
            df.to_csv(FILE_PATH, index=False)
            st.success("Incident updated!")
            st.rerun()

# --- DELETE INCIDENT ---
if st.session_state.show_delete:
    st.subheader("🗑️ Delete Incident")
    delete_index = st.number_input("Row Number to Delete", 0, len(df)-1, 0, key="del_index")
    if st.button("Delete Incident", key="delete_btn"):
        df = df.drop(delete_index).reset_index(drop=True)
        df.to_csv(FILE_PATH, index=False)
        st.success("Incident deleted!")
        st.rerun()

# --- AI ASSISTANT ---
if st.session_state.show_ai:
    st.subheader("🤖 AI Assistant")
    query = st.text_input("Ask about Cyber Incidents", key="ai_query")
    if st.button("Get Answer", key="ai_btn"):
        if query.strip() == "":
            st.write("Please enter a query.")
        else:
            filtered = df[df.apply(lambda row: query.lower() in str(row).lower(), axis=1)]
            if not filtered.empty:
                st.dataframe(filtered, width='stretch')
            else:
                st.write("No matching incidents found.")

# --- LINE GRAPH: Incidents Over Time ---
st.subheader("📈 Incidents Over Time")
if 'timestamp' in df.columns and not df.empty:
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    timeline = df.groupby("timestamp").size().reset_index(name="Count").sort_values('timestamp')
    if not timeline.empty:
        fig = px.line(timeline, x="timestamp", y="Count", title="Incidents Over Time", markers=True)
        st.plotly_chart(fig, width='stretch')
    else:
        st.write("No date data available to plot timeline.")
else:
    st.write("No 'timestamp' column found to display graph.")

# --- PIE CHARTS: Severity & Status ---
st.subheader("📊 Incident Overview by Severity")
if 'severity' in df.columns and not df.empty:
    severity_counts = df['severity'].value_counts().reset_index()
    severity_counts.columns = ['Severity', 'Count']
    fig1 = px.pie(severity_counts, names='Severity', values='Count', title="Incidents by Severity")
    st.plotly_chart(fig1, width='stretch')

st.subheader("📊 Incident Overview by Status")
if 'status' in df.columns and not df.empty:
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    fig2 = px.pie(status_counts, names='Status', values='Count', title="Incidents by Status")
    st.plotly_chart(fig2, width='stretch')

# --- SHOW DATA TABLE ---
st.header("📋 All Cyber Incidents")
st.dataframe(df, width='stretch')
