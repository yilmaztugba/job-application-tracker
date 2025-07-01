import streamlit as st
import pandas as pd
from datetime import datetime

# Load or initialize data
csv_file = "job_tracker.csv"
columns = [
    "Date Applied", "Company", "Position Title", "Job Link", "Location",
    "Application Status", "Follow-Up Date", "Interview Date",
    "Contact Person", "Notes"
]

try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    df = pd.DataFrame(columns=columns)

st.title("📋 Job Application Tracker")

# --- ADD NEW APPLICATION ---
with st.form("job_form"):
    st.subheader("➕ Add New Application")
    col1, col2 = st.columns(2)
    with col1:
        company = st.text_input("Company")
        position = st.text_input("Position Title")
        location = st.text_input("Location")
        job_link = st.text_input("Job Link")
    with col2:
        date_applied = st.date_input("Date Applied", value=datetime.today())
        follow_up = st.date_input("Follow-Up Date")
        interview_date = st.date_input("Interview Date")
        contact = st.text_input("Contact Person")

    status = st.selectbox("Application Status", ["Submitted", "Interview Scheduled", "Rejected", "Offer", "Other"])
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Add Application")

    if submitted:
        new_entry = {
            "Date Applied": date_applied,
            "Company": company,
            "Position Title": position,
            "Job Link": job_link,
            "Location": location,
            "Application Status": status,
            "Follow-Up Date": follow_up,
            "Interview Date": interview_date,
            "Contact Person": contact,
            "Notes": notes
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(csv_file, index=False)
        st.success("🎉 Application added!")

        # 🔄 Refresh the app to clear form fields
        st.experimental_rerun()

# --- FILTER + DISPLAY ---
st.subheader("📊 View & Filter Applications")
if not df.empty:
    status_filter = st.multiselect("Filter by Status", df["Application Status"].unique(), default=list(df["Application Status"].unique()))
    filtered_df = df[df["Application Status"].isin(status_filter)]
    st.dataframe(filtered_df)
    st.download_button("📥 Download Filtered CSV", filtered_df.to_csv(index=False), file_name="filtered_job_apps.csv")
else:
    st.info("No applications found yet.")

# --- EDIT EXISTING ENTRY ---
st.subheader("✏️ Edit an Existing Application")
if not df.empty:
    selected_index = st.selectbox("Select an application to edit (by index):", df.index)
    row = df.loc[selected_index]

    with st.form("edit_form"):
        status = st.selectbox("Application Status", ["Submitted", "Interview Scheduled", "Rejected", "Offer", "Other"],
                              index=["Submitted", "Interview Scheduled", "Rejected", "Offer", "Other"].index(row["Application Status"]))
        follow_up = st.date_input("Follow-Up Date", value=pd.to_datetime(row["Follow-Up Date"]) if pd.notna(row["Follow-Up Date"]) else datetime.today())
        interview_date = st.date_input("Interview Date", value=pd.to_datetime(row["Interview Date"]) if pd.notna(row["Interview Date"]) else datetime.today())
        notes = st.text_area("Notes", value=row["Notes"] if pd.notna(row["Notes"]) else "")

        submitted_edit = st.form_submit_button("Save Changes")
        if submitted_edit:
            df.at[selected_index, "Application Status"] = status
            df.at[selected_index, "Follow-Up Date"] = follow_up
            df.at[selected_index, "Interview Date"] = interview_date
            df.at[selected_index, "Notes"] = notes
            df.to_csv(csv_file, index=False)
            st.success("✅ Application updated!")
else:
    st.info("No applications available to edit.")

# --- DELETE APPLICATION ---
st.subheader("🗑️ Delete an Application")
if not df.empty:
    delete_index = st.selectbox("Select application to delete (by index):", df.index, key="delete_selector")

    if st.button("Delete Selected Application"):
        deleted_row = df.loc[delete_index]
        df = df.drop(index=delete_index).reset_index(drop=True)
        df.to_csv(csv_file, index=False)
        st.success(f"✅ Deleted application: {deleted_row['Position Title']} at {deleted_row['Company']}")
        st.experimental_rerun()
else:
    st.info("No applications available to delete.")