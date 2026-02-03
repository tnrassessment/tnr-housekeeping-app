import streamlit as st
import datetime
import pandas as pd

# --- APP CONFIGURATION ---
# Use the local file path to the uploaded logo
TNR_LOGO_PATH = "TNR_logo-03.png"

st.set_page_config(page_title="TNR Housekeeping", page_icon=TNR_LOGO_PATH, layout="wide")
st.title("🏨 Tashi Namgay Resort Housekeeping Inspection")

# Define all the inspection columns from the user's list
CHECKLIST_ITEMS = [
    "Bed Linen Clean & Proper",
    "Bathroom Clean & Sanitized",
    "Floor Clean & Dry",
    "Furniture Dust-Free",
    "Mirror & Glass Clean",
    "Amenities Properly Placed",
    "Trash Emptied",
    "No Odour in Room",
    "Towels Clean & Available",
    "Toiletries Complete",
    "WC & Shower Clean",
    "Drainage Working",
    "Lights Working",
    "AC / Heating Working",
    "Curtains & Locks OK"
]

# --- INTERFACE ---

# Main form
with st.form("inspection_form"):
    st.header("General Details")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        inspector_name = st.text_input("Inspector Name")
    with col2:
        room_number = st.text_input("Room Number / Area")
    with col3:
        room_type = st.text_input("Room Type")
    with col4:
        hk_staff_name = st.text_input("HK Staff Name")
    with col5:
        inspection_date = datetime.date.today()
        st.date_input("Inspection Date", value=inspection_date, disabled=True)

    st.header("Inspection Checklist (Pass/Fail/N/A)")
    
    # Use radio buttons for binary checks
    results = {}
    for item in CHECKLIST_ITEMS:
        results[item] = st.radio(f"**{item}**", ["Pass", "Fail", "N/A"], horizontal=True, key=item)

    st.header("Maintenance & Follow-up")
    colA, colB, colC = st.columns(3)
    with colA:
        damage_observed = st.selectbox("Any Damage Observed?", ["No", "Yes"])
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        responsible_dept = st.text_input("Responsible Dept")
    with colB:
        maintenance_required = st.selectbox("Maintenance Required?", ["No", "Yes"])
        target_date = st.date_input("Target Resolution Date", value=inspection_date + datetime.timedelta(days=1))
        status = st.selectbox("Status", ["Open", "Closed"])
    with colC:
        overall_condition = st.selectbox("Overall Room Condition", ["Excellent", "Good", "Fair", "Poor"])
    
    issue_description = st.text_area("Issue Description")
    inspector_remarks = st.text_area("Inspector Remarks")
    
    guest_ready_status = st.selectbox("Guest-Ready Status", ["Ready", "Not Ready"])

    # Every form must have a submit button
    submitted = st.form_submit_button("Submit Inspection Report")
    if submitted:
        # Compile all data into a format that matches your column titles
        data = {
            "Inspection Date": inspection_date,
            "Inspector Name": inspector_name,
            "Room Number / Area": room_number,
            "Room Type": room_type,
            "HK Staff Name": hk_staff_name,
        }
        # Add checklist results
        data.update(results)
        # Add maintenance details
        data.update({
            "Any Damage Observed?": damage_observed,
            "Maintenance Required?": maintenance_required,
            "Issue Description": issue_description,
            "Priority": priority,
            "Action Required": "See Remarks", # Action Required maps best to remarks here
            "Responsible Dept": responsible_dept,
            "Target Resolution Date": target_date,
            "Status": status,
            "Overall Room Condition": overall_condition,
            "Inspector Remarks": inspector_remarks,
            "Guest-Ready Status": guest_ready_status
        })

        # Create a DataFrame for nice formatting and CSV export
        report_df = pd.DataFrame([data])
        
        st.success("Inspection Report Submitted Successfully!")
        # Use st.download_button to get the report in a useful format like CSV
        st.download_button(
            label="Download Report as CSV",
            data=report_df.to_csv(index=False).encode('utf-8'),
            file_name=f"TNR_Inspection_{room_number}_{inspection_date}.csv",
            mime="text/csv",
        )
