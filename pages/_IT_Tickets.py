import streamlit as st
import pandas as pd
import plotly.express as px

# --- File Path ---
FILE_PATH = r"C:\Users\SAMEENA\OneDrive\Documents\Hana\Programming for Data Communication & Networks\Lab Files 7-12\DATA\it_tickets.csv"

# --- Load CSV ---
df = pd.read_csv(FILE_PATH)
df.columns = df.columns.str.strip()  # clean column names

# --- Rename columns for dashboard ---
df = df.rename(columns={
    'description': 'Title',
    'assigned_to': 'Assigned To',
    'priority': 'Priority',
    'status': 'Status',
    'created_at': 'Created On'
})

# --- Convert Created On to datetime ---
df['Created On'] = pd.to_datetime(df['Created On'], format='%d/%m/%Y', errors='coerce')

# --- Page Config ---
st.set_page_config(page_title="IT Tickets", layout="wide")
st.sidebar.title("User Info")
st.sidebar.write("User: Alice")
st.sidebar.write("Role: Analyst")
st.sidebar.button("Logout")

# --- Title ---
st.title("💻 IT Tickets")
st.write("Manage IT tickets using the buttons below.")
st.write("---")

# --- Initialize session state for form toggles ---
for key in ['show_add', 'show_update', 'show_delete', 'show_ai']:
    if key not in st.session_state:
        st.session_state[key] = False

# --- Horizontal Action Buttons ---
btn1, btn2, btn3, btn4 = st.columns(4)
with btn1:
    if st.button("➕ Add"):
        st.session_state.show_add = True
with btn2:
    if st.button("✏️ Update"):
        st.session_state.show_update = True
with btn3:
    if st.button("🗑 Delete"):
        st.session_state.show_delete = True
with btn4:
    if st.button("🤖 AI"):
        st.session_state.show_ai = True

st.write("---")

# --- ADD TICKET ---
if st.session_state.show_add:
    st.subheader("➕ Add New Ticket")
    with st.form("add_ticket"):
        title = st.text_input("Title")
        assigned_to = st.text_input("Assigned To")
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
        created_on = st.date_input("Created On")
        submitted = st.form_submit_button("Add Ticket")
        if submitted:
            new_row = pd.DataFrame({
                "Title": [title],
                "Assigned To": [assigned_to],
                "Priority": [priority],
                "Status": [status],
                "Created On": [created_on]
            })
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(FILE_PATH, index=False)
            st.success("Ticket added successfully!")
            st.rerun()

# --- UPDATE TICKET ---
if st.session_state.show_update:
    st.subheader("✏️ Update Ticket")
    update_index = st.number_input("Row Number to Update", 0, len(df)-1, 0)
    if st.button("Load Ticket for Update", key="load_update_ticket"):
        row = df.iloc[update_index]
        title = st.text_input("Title", row['Title'], key="update_title")
        assigned_to = st.text_input("Assigned To", row['Assigned To'], key="update_assigned")
        priority = st.selectbox(
            "Priority", ["Low", "Medium", "High", "Critical"], 
            index=["Low", "Medium", "High", "Critical"].index(row['Priority']),
            key="update_priority"
        )
        status = st.selectbox(
            "Status", ["Open", "In Progress", "Resolved", "Closed"], 
            index=["Open", "In Progress", "Resolved", "Closed"].index(row['Status']),
            key="update_status"
        )
        created_on = st.date_input("Created On", row['Created On'], key="update_date")
        if st.button("Update Ticket", key="update_btn_ticket"):
            df.at[update_index, 'Title'] = title
            df.at[update_index, 'Assigned To'] = assigned_to
            df.at[update_index, 'Priority'] = priority
            df.at[update_index, 'Status'] = status
            df.at[update_index, 'Created On'] = created_on
            df.to_csv(FILE_PATH, index=False)
            st.success("Ticket updated successfully!")
            st.rerun()

# --- DELETE TICKET ---
if st.session_state.show_delete:
    st.subheader("🗑️ Delete Ticket")
    delete_index = st.number_input("Row Number to Delete", 0, len(df)-1, 0, key="del_index_ticket")
    if st.button("Delete Ticket", key="del_btn_ticket"):
        df = df.drop(delete_index).reset_index(drop=True)
        df.to_csv(FILE_PATH, index=False)
        st.success("Ticket deleted!")
        st.rerun()

# --- AI ASSISTANT ---
if st.session_state.show_ai:
    st.subheader("🤖 AI Assistant")
    query = st.text_input("Ask about IT Tickets", key="ai_query_ticket")
    if st.button("Get Answer", key="ai_btn_ticket"):
        if query.strip() == "":
            st.write("Please enter a query.")
        else:
            filtered = df[df.apply(lambda row: query.lower() in str(row).lower(), axis=1)]
            if not filtered.empty:
                st.dataframe(filtered, use_container_width=True)
            else:
                st.write("No matching tickets found.")

# --- Tickets Status Overview ---
st.subheader("📊 Tickets Status Overview")
if 'Status' in df.columns and not df.empty:
    status_counts = df['Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    fig = px.pie(status_counts, names='Status', values='Count', title="Tickets by Status")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No data available or 'Status' column missing.")

# --- Tickets Over Time ---
st.subheader("📈 Tickets Over Time")
if 'Created On' in df.columns and not df.empty:
    timeline = df.groupby('Created On').size().reset_index(name='Count')
    timeline = timeline.sort_values('Created On')
    if not timeline.empty:
        fig_line = px.line(timeline, x='Created On', y='Count', title="Tickets Created Over Time", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.write("No date data available to plot timeline.")
else:
    st.write("No 'Created On' column found. Add a date column to plot timeline.")

# --- Show All Tickets ---
st.header("📄 All IT Tickets")
st.dataframe(df, use_container_width=True)
