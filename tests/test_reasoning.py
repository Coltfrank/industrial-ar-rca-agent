from app.core.orchestrator import DiagnosisOrchestrator
from app.core.models import AlarmEvent, PLCPoint, OperationRecord


def test_alarm_204_jam_ranked_top():
    orchestrator = DiagnosisOrchestrator()
    event = AlarmEvent(
        line_id="L1",
        station_id="S1",
        equipment_id="E1",
        timestamp="2026-04-30T09:00:00",
        alarm_code="ALM-204",
        alarm_message="Transfer station timeout",
        plc_snapshot=[
            PLCPoint(tag="PE_14", value="OFF"),
            PLCPoint(tag="MTR_TRANSFER_CURRENT_HIGH", value="TRUE"),
            PLCPoint(tag="AIR_PRESSURE_LOW", value="FALSE"),
        ],
        recent_operations=[
            OperationRecord(ts="2026-04-30T08:59:59", action="Transfer command issued")
        ],
    )
    result = orchestrator.run(event)
    assert "jam" in result.root_cause["title"].lower()
    assert result.severity in {
        "AUTO_RECOVERABLE", "NEED_OPERATOR_CONFIRMATION", "REQUIRE_STOPPAGE"
    }
