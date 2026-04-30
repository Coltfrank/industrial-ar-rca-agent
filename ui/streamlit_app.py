import json
from pathlib import Path
import streamlit as st
from app.core.orchestrator import DiagnosisOrchestrator
from app.core.models import AlarmEvent

st.set_page_config(page_title="Industrial RCA Agent", layout="wide")
st.title("Industrial Anomaly Diagnosis + RCA Agent")
st.caption("Demo UI for PLC alarm diagnosis, root cause ranking, and action recommendation")

example_path = Path(__file__).resolve().parents[1] / "examples" / "sample_alarm_event.json"
default_json = example_path.read_text(encoding="utf-8")

payload = st.text_area("Alarm Event JSON", value=default_json, height=360)

if st.button("Run Diagnosis"):
    try:
        event = AlarmEvent(**json.loads(payload))
        orchestrator = DiagnosisOrchestrator()
        result = orchestrator.run(event)
        st.subheader("Diagnosis Result")
        st.json(result.model_dump())
    except Exception as e:
        st.error(str(e))
