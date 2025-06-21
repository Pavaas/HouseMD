import streamlit as st
from fpdf import FPDF
import datetime
import os

st.set_page_config(page_title="HouseMD - Clinical App", layout="wide")

# ------------------ USER ROLE HANDLING ------------------
roles = {
    "doctor": "doctor123",
    "reception": "reception123",
    "pharmacy": "pharmacy123",
    "lab": "lab123",
    "radiology": "radiology123",
    "biochem": "biochem123",
    "pathology": "pathology123"
}

st.sidebar.title("HouseMD Login")
username = st.sidebar.selectbox("Select Role", list(roles.keys()))
password = st.sidebar.text_input("Enter Password", type="password")
if password != roles.get(username):
    st.sidebar.warning("Enter correct password to continue.")
    st.stop()

st.sidebar.success(f"Logged in as: {username.upper()}")

# ------------------ FUNCTIONS ------------------

def symptom_picker():
    st.header("🩺 Symptom-Based Trigger")
    symptoms = ["Fever", "Burning urination", "Abdominal pain", "Cough", "Chest pain"]
    selected = st.multiselect("Select presenting symptoms:", symptoms)
    if selected:
        st.info(f"Selected: {', '.join(selected)}")
        st.success("Might be: UTI, Pneumonia, Gastroenteritis (Mock output)")

def history_taking():
    st.header("📝 History Taking")
    systems = {
        "General": ["Fever", "Weight loss", "Fatigue"],
        "GI": ["Abdominal pain", "Nausea", "Vomiting"],
        "GU": ["Burning urination", "Frequency", "Flank pain"]
    }
    for system, questions in systems.items():
        with st.expander(f"{system} History"):
            for q in questions:
                st.checkbox(q)

def test_suggestions():
    st.header("🧪 Suggested Tests")
    if st.button("Show Suggested Tests"):
        tests = ["CBC", "Urine Routine", "RBS", "LFT"]
        for t in tests:
            st.checkbox(t)

def triage_tests():
    st.header("🚨 Triage Diagnostic Workflow")
    test = st.selectbox("Select Test", ["X-ray Chest", "CBC", "USG Abdomen"])
    triage = st.radio("Triage Level", ["🟢 Green", "🟡 Yellow", "🔴 Red"])
    st.success(f"Test ordered: {test} with {triage} priority")

def prescription_builder():
    st.header("💊 Prescription Generator")
    name = st.text_input("Patient Name")
    meds = st.text_area("Enter medicines and instructions")
    if st.button("Generate PDF Rx"):
        filename = f"{name}_rx.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Prescription for {name}", ln=True)
        pdf.multi_cell(0, 10, meds)
        pdf.output(filename)
        with open(filename, "rb") as f:
            st.download_button("Download Prescription PDF", f, file_name=filename)
        os.remove(filename)

def reception_panel():
    st.header("🧾 Reception - Patient Entry")
    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    complaint = st.text_input("Chief Complaint")
    if st.button("Add to Queue"):
        st.success(f"Added {name} to queue")

def pharmacy_panel():
    st.header("💊 Pharmacy Panel")
    st.table({"Patient": ["Aman"], "Medicines": ["Amoxicillin x5"], "Dispensed": ["❌"]})
    st.button("Mark as Dispensed")

def lab_panel():
    st.header("🔬 Lab Dashboard")
    st.table({"Patient": ["Ravi", "Neha"], "Test": ["CBC", "Urine"], "Status": ["Pending", "Pending"]})
    st.button("Mark Sample Collected")

def radiology_panel():
    st.header("🩻 Radiology Panel")
    file = st.file_uploader("Upload Radiology Report")
    if file:
        st.success("File uploaded.")

def admin_dashboard():
    st.header("📊 Admin Dashboard")
    st.metric("Today’s OPD Revenue", "₹6,000")
    st.metric("Pharmacy Income", "₹3,200")
    st.metric("Lab Collections", "₹2,500")

# ------------------ UI ROUTING ------------------

if username == "doctor":
    st.title("🏥 Doctor's Panel")
    tabs = st.tabs(["Symptom Trigger", "History", "Tests", "Triage", "Prescription", "Admin"])
    with tabs[0]: symptom_picker()
    with tabs[1]: history_taking()
    with tabs[2]: test_suggestions()
    with tabs[3]: triage_tests()
    with tabs[4]: prescription_builder()
    with tabs[5]: admin_dashboard()

elif username == "reception":
    st.title("🧾 Reception Desk")
    reception_panel()

elif username == "pharmacy":
    st.title("💊 Pharmacy Desk")
    pharmacy_panel()

elif username == "lab":
    st.title("🔬 Lab Technician Panel")
    lab_panel()

elif username == "radiology":
    st.title("🩻 Radiology Panel")
    radiology_panel()

else:
    st.info("Panel for this role is coming soon.")
