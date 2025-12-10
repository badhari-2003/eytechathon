import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# =========================================================
#               AGENTIC MODEL (BACKEND LOGIC)
# =========================================================

class DataAnalysisAgent:
    def analyze(self, temp, vibration, last_service):
        """Very simple 'risk score' model for demo."""
        risk = 0.0
        if temp > 95:
            risk += 0.4
        if vibration > 0.7:
            risk += 0.3
        if last_service > 180:
            risk += 0.3
        return min(risk, 1.0)


class DiagnosisAgent:
    def diagnose(self, risk_score: float) -> str:
        if risk_score >= 0.66:
            return "High Failure Likelihood"
        elif risk_score >= 0.33:
            return "Medium Failure Likelihood"
        return "Low Failure Likelihood"


class CustomerVoiceAgent:
    def build_message(self, owner_name: str, diagnosis: str) -> str:
        if "High" in diagnosis:
            return f"Hello {owner_name}, our system has detected a HIGH risk issue. Please visit service immediately."
        elif "Medium" in diagnosis:
            return f"Hello {owner_name}, your vehicle shows a MEDIUM level risk. We recommend scheduling service soon."
        else:
            return f"Hello {owner_name}, your vehicle is in good condition. No urgent action is required."


class SchedulingAgent:
    def suggest_slot(self):
        dates = [datetime.now().date() + timedelta(days=i) for i in range(1, 6)]
        slots = ["09:00–11:00", "11:00–13:00", "14:00–16:00"]
        centers = ["Hero Service Center", "Mahindra AutoCare", "Express Auto Hub"]

        date_choice = random.choice(dates)
        slot_choice = random.choice(slots)
        center_choice = random.choice(centers)

        return {
            "date": date_choice,
            "slot": slot_choice,
            "center": center_choice
        }


class ManufacturingInsightsAgent:
    def rca_feedback(self, diagnosis: str) -> str:
        if "High" in diagnosis:
            return "Frequent high-risk alerts indicate issues in cooling system and vibration damping. Recommend CAPA on those components."
        elif "Medium" in diagnosis:
            return "Medium risk suggests early signs of wear. Suggest preventive checks on engine & suspension in next service cycle."
        else:
            return "Low risk. Use data to validate existing design robustness and update reliability KPIs."


class MasterAgent:
    def __init__(self):
        self.data_agent = DataAnalysisAgent()
        self.diagnosis_agent = DiagnosisAgent()
        self.voice_agent = CustomerVoiceAgent()
        self.schedule_agent = SchedulingAgent()
        self.rca_agent = ManufacturingInsightsAgent()

    def run_for_vehicle(self, vehicle_row: pd.Series) -> dict:
        """End-to-end pipeline for a single vehicle."""
        temp = vehicle_row["temp"]
        vibration = vehicle_row["vibration"]
        last_service = vehicle_row["last_service"]
        owner = vehicle_row["owner"]

        # 1. Analyze data
        risk_score = self.data_agent.analyze(temp, vibration, last_service)

        # 2. Diagnosis
        diagnosis = self.diagnosis_agent.diagnose(risk_score)

        # 3. Customer message
        voice_msg = self.voice_agent.build_message(owner, diagnosis)

        # 4. Decide scheduling
        should_book = "High" in diagnosis or "Medium" in diagnosis
        booking = self.schedule_agent.suggest_slot() if should_book else None

        # 5. Manufacturing insights
        rca_text = self.rca_agent.rca_feedback(diagnosis)

        # Convert risk_score to level + %
        if risk_score >= 0.66:
            level = "High"
            icon = "🔴"
        elif risk_score >= 0.33:
            level = "Medium"
            icon = "🟡"
        else:
            level = "Low"
            icon = "🟢"

        return {
            "risk_score": round(risk_score * 100, 1),
            "risk_level": level,
            "risk_icon": icon,
            "diagnosis": diagnosis,
            "voice_message": voice_msg,
            "should_book": should_book,
            "booking": booking,
            "rca_feedback": rca_text
        }


# =========================================================
#                 STREAMLIT UI (FRONTEND)
# =========================================================

st.set_page_config(page_title="AutoSense AI", layout="wide")
st.title("🚗 AutoSense – Agentic Predictive Maintenance Prototype")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["Dashboard", "Vehicle Details (Agentic)", "Schedule Service (Manual)", "RCA/CAPA Insights"]
)

# ---------- Dummy vehicle data ----------
vehicles = [
    {"id": "VH-101", "owner": "Rahul", "model": "Hero Xpulse 200", "temp": 98, "vibration": 0.8, "last_service": 210, "odometer": 28500},
    {"id": "VH-102", "owner": "Ananya", "model": "Mahindra XUV700", "temp": 90, "vibration": 0.4, "last_service": 120, "odometer": 15000},
    {"id": "VH-103", "owner": "Kunal", "model": "Hero Splendor", "temp": 93, "vibration": 0.6, "last_service": 300, "odometer": 42000},
]

df = pd.DataFrame(vehicles)

# Precompute a readable risk (for dashboard only)
def simple_risk(row):
    risk = 0.0
    if row["temp"] > 95:
        risk += 0.4
    if row["vibration"] > 0.7:
        risk += 0.3
    if row["last_service"] > 180:
        risk += 0.3
    if risk >= 0.66:
        return "🔴 High"
    elif risk >= 0.33:
        return "🟡 Medium"
    else:
        return "🟢 Low"

df["Risk"] = df.apply(simple_risk, axis=1)

master_agent = MasterAgent()

# =========================================================
#                        PAGES
# =========================================================

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.subheader("📊 Fleet Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Vehicles", len(df))
    col2.metric("High Risk", (df["Risk"] == "🔴 High").sum())
    col3.metric("Medium Risk", (df["Risk"] == "🟡 Medium").sum())

    st.markdown("### Vehicle Summary")
    st.dataframe(df)

    st.markdown("### Sample Telematics Stream (Simulated)")
    times = pd.date_range(end=datetime.now(), periods=24, freq="h")
    temps = 92 + np.random.randn(24).cumsum() * 0.3
    chart = pd.DataFrame({"Engine Temp (°C)": temps}, index=times)
    st.line_chart(chart)

# ---------------- VEHICLE DETAILS + AGENTIC ----------------
elif page == "Vehicle Details (Agentic)":
    st.subheader("🤖 Vehicle Health & Agentic AI Orchestration")

    selected_id = st.selectbox("Select Vehicle", df["id"])
    row = df[df["id"] == selected_id].iloc[0]

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Owner:** {row['owner']}")
        st.write(f"**Model:** {row['model']}")
        st.write(f"**Odometer:** {row['odometer']} km")
    with col2:
        st.write(f"**Engine Temp:** {row['temp']} °C")
        st.write(f"**Vibration:** {row['vibration']}")
        st.write(f"**Last Service:** {row['last_service']} days")

    st.markdown("---")

    if st.button("Run Agentic AI for this Vehicle"):
        result = master_agent.run_for_vehicle(row)

        st.markdown(f"### Predicted Failure Risk: {result['risk_icon']} **{result['risk_level']}** ({result['risk_score']}%)")
        st.write(f"**Diagnosis:** {result['diagnosis']}")
        st.write(f"**Voice Agent Message:** {result['voice_message']}")

        if result["should_book"] and result["booking"]:
            b = result["booking"]
            st.success(
                f"📅 Recommended Service Slot: **{b['date']}**, **{b['slot']}** at **{b['center']}**"
            )
        else:
            st.info("No immediate booking required. Continue monitoring the vehicle.")

        st.markdown("### Manufacturing RCA / CAPA Insight")
        st.write(result["rca_feedback"])

    else:
        st.info("Click **'Run Agentic AI for this Vehicle'** to simulate the full multi-agent flow.")

# ---------------- MANUAL SCHEDULING PAGE ----------------
elif page == "Schedule Service (Manual)":
    st.subheader("🛠 Manual Service Slot Booking (for demo)")

    selected_id = st.selectbox("Select Vehicle", df["id"])
    row = df[df["id"] == selected_id].iloc[0]

    st.write(f"**Owner:** {row['owner']}  |  **Model:** {row['model']}")

    date = st.date_input("Preferred Date", datetime.now() + timedelta(days=1))
    slot = st.selectbox("Time Slot", ["09:00–11:00", "11:00–13:00", "14:00–16:00"])
    center = st.selectbox("Service Center", ["Hero Service Center", "Mahindra AutoCare", "Express Auto Hub"])

    if st.button("Confirm Booking"):
        st.success(f"✅ Booking Confirmed for {selected_id} on {date} at {slot} – {center}")

# ---------------- RCA / CAPA PAGE ----------------
elif page == "RCA/CAPA Insights":
    st.subheader("🏭 RCA / CAPA Insights (Aggregated Demo)")

    causes = ["Cooling System", "Vibration / Suspension", "Battery", "ECU / Electronics"]
    values = [12, 9, 5, 3]
    chart_df = pd.DataFrame({"Failures": values}, index=causes)
    st.bar_chart(chart_df)

    st.write("""
    ### Sample OEM-Level Recommendations
    - Increase quality checks on coolant pump, thermostat and related hoses.  
    - Review vibration damping components and torque specifications.  
    - Set preventive battery replacement at 3 years / 50,000 km.  
    - Log and analyze ECU error codes to refine firmware.  
    """)

    st.info("These insights represent what the Manufacturing Insights Agent can send back to OEM quality teams.")
