import streamlit as st
import datetime

# --- APP CONFIGURATION ---
st.set_page_config(page_title="TNR Housekeeping", page_icon="🏨")
st.title("🏨 Tashi Namgay Resort")
st.subheader("Housekeeping Inspection Portal")

# --- DATA ---
room_types = {
    "Executive Suite": ["Paro Dzong View", "Ta Dzong View", "Jetted Bathtub"],
    "Junior Suite": ["Floor Heating System", "Extra Bed Space"],
    "Deluxe Cottage": ["Traditional Bhutanese Theme", "Private Entry"],
    "Deluxe Room": ["Standard Amenities", "River View"]
}

# --- INTERFACE ---
with st.sidebar:
    st.header("Inspection Details")
    inspector = st.text_input("Staff Name")
    room_no = st.text_input("Room Number", placeholder="e.g., 101")
    room_cat = st.selectbox("Room Category", list(room_types.keys()))

st.info(f"Inspecting: **{room_cat}**")

# Standard Checklist + Specific Amenities
checklist = [
    "Bedding & Linens (Hospital Corners)",
    "Traditional Bhutanese Decor Condition",
    "Tea/Coffee Maker & Minibar Restock",
    "Bathroom Sanitization & Toiletries",
    "AC/Heating Functionality Check",
    "Balcony & Window Cleanliness"
]

# Add category-specific checks
if room_cat == "Junior Suite":
    checklist.append("Floor Heating Functionality")

# --- FORM ---
results = {}
for item in checklist:
    results[item] = st.radio(f"{item}:", ["Pass", "Fail", "N/A"], horizontal=True, key=item)

comments = st.text_area("Additional Maintenance Notes")

if st.button("Submit Inspection Report"):
    if not inspector or not room_no:
        st.error("Please provide Staff Name and Room Number.")
    else:
        # Create report string
        report_data = f"""
        TASHI NAMGAY RESORT INSPECTION
        Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
        Inspector: {inspector}
        Room: {room_no} ({room_cat})
        --------------------------------
        """
        for item, status in results.items():
            report_data += f"{item}: {status}\n"
        
        st.success(f"Inspection for Room {room_no} Submitted!")
        st.download_button("Download Report (.txt)", report_data, file_name=f"TNR_Room_{room_no}.txt")
