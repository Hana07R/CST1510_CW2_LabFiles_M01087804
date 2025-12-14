import streamlit as st
import pandas as pd
import plotly.express as px

# --- FILE PATH ---
FILE_PATH = r"C:\Users\SAMEENA\OneDrive\Documents\Hana\Programming for Data Communication & Networks\Lab Files 7-12\DATA\security_threats.csv"

# --- Load CSV ---
df = pd.read_csv(FILE_PATH)
df.columns = df.columns.str.strip()
df['detected_on'] = pd.to_datetime(df['detected_on'], errors='coerce')

# --- Page Config ---
st.set_page_config(page_title="Security Threats", layout="wide")

st.title("🛡️ Security Threats")
st.write("Manage security threats using the buttons below.")
st.write("---")

# --- Initialize session state for form toggles ---
for key in ['show_add', 'show_update', 'show_delete', 'show_ai']:
    if key not in st.session_state:
        st.session_state[key] = False

# --- Horizontal Action Buttons ---
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

# --- ADD THREAT ---
if st.session_state.show_add:
    st.subheader("➕ Add New Threat")
    with st.form("add_threat"):
        threat_name = st.text_input("Threat Name")
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        detected_on = st.date_input("Detected On")
        submitted = st.form_submit_button("Add Threat")
        if submitted:
            new_row = pd.DataFrame({
                "threat_name": [threat_name],
                "severity": [severity],
                "detected_on": [detected_on]
            })
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(FILE_PATH, index=False)
            st.success("Threat added successfully!")
            st.rerun()

# --- UPDATE THREAT ---
if st.session_state.show_update:
    st.subheader("✏️ Update Threat")
    update_index = st.number_input("Row Number to Update", 0, len(df)-1, 0)
    if st.button("Load Threat for Update", key="load_update_threat"):
        row = df.iloc[update_index]
        threat_name = st.text_input("Threat Name", row['threat_name'], key="update_name")
        severity = st.selectbox(
            "Severity", ["Low", "Medium", "High", "Critical"], 
            index=["Low", "Medium", "High", "Critical"].index(row['severity']),
            key="update_sev"
        )
        detected_on = st.date_input("Detected On", pd.to_datetime(row['detected_on']), key="update_date")
        if st.button("Update Threat", key="update_btn_threat"):
            df.at[update_index, 'threat_name'] = threat_name
            df.at[update_index, 'severity'] = severity
            df.at[update_index, 'detected_on'] = detected_on
            df.to_csv(FILE_PATH, index=False)
            st.success("Threat updated!")
            st.rerun()

# --- DELETE THREAT ---
if st.session_state.show_delete:
    st.subheader("🗑️ Delete Threat")
    delete_index = st.number_input("Row Number to Delete", 0, len(df)-1, 0, key="del_index_threat")
    if st.button("Delete Threat", key="delete_btn_threat"):
        df = df.drop(delete_index).reset_index(drop=True)
        df.to_csv(FILE_PATH, index=False)
        st.success("Threat deleted!")
        st.rerun()

# --- AI ASSISTANT ---
if st.session_state.show_ai:
    st.subheader("🤖 AI Assistant")
    query = st.text_input("Ask about Security Threats", key="ai_query_threat")
    if st.button("Get Answer", key="ai_btn_threat"):
        if query.strip() == "":
            st.write("Please enter a query.")
        else:
            filtered = df[df.apply(lambda row: query.lower() in str(row).lower(), axis=1)]
            if not filtered.empty:
                st.dataframe(filtered, use_container_width=True)
            else:
                st.write("No matching threats found.")

# --- PIE CHART BY SEVERITY ---
st.subheader("📊 Threats Overview by Severity")
if 'severity' in df.columns and not df.empty:
    severity_counts = df['severity'].value_counts().reset_index()
    severity_counts.columns = ['Severity', 'Count']
    fig = px.pie(severity_counts, names='Severity', values='Count', title="Threats by Severity")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No threats to display.")

# --- LINE CHART OVER TIME ---
st.subheader("📈 Threats Detected Over Time")
if 'detected_on' in df.columns and not df.empty:
    timeline = df.groupby('detected_on').size().reset_index(name='Count').sort_values('detected_on')
    if not timeline.empty:
        fig_line = px.line(timeline, x='detected_on', y='Count', title="Threats Over Time", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.write("No date data available to plot timeline.")
else:
    st.write("No 'Detected On' column found.")

# --- SHOW DATA TABLE ---
st.header("📋 All Security Threats")
st.dataframe(df, use_container_width=True)
