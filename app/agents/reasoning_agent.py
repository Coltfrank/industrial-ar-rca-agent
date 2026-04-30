from __future__ import annotations
from pathlib import Path
import json
from app.core.models import CandidateCause, RootCauseResult


class ReasoningAgent:
    def __init__(self, knowledge_root: str):
        alarm_dict_path = Path(knowledge_root) / "alarm_dictionary.json"
        self.alarm_dict = json.loads(alarm_dict_path.read_text(encoding="utf-8"))

    def _score_alarm_204(self, ctx: dict, docs: list) -> list[CandidateCause]:
        plc = ctx.get("plc_map", {})
        ops = [a.get("action", "") for a in ctx.get("recent_actions", [])]
        candidates = []

        sensor_off = plc.get("PE_14", "OFF") == "OFF"
        conveyor_high_current = plc.get("MTR_TRANSFER_CURRENT_HIGH", "FALSE") == "TRUE"
        air_low = plc.get("AIR_PRESSURE_LOW", "FALSE") == "TRUE"
        auto_mode = ctx.get("mode", "AUTO") == "AUTO"
        transfer_cmd_present = any("transfer" in x.lower() for x in ops)

        score = 0.2
        evidence = []
        missing = []
        if sensor_off:
            score += 0.25
            evidence.append("Transfer sensor PE_14 remained OFF after transfer command")
        else:
            missing.append("Verify PE_14 input quality and wiring")
        if conveyor_high_current:
            score += 0.2
            evidence.append("Transfer conveyor current entered high window, consistent with jam")
        if transfer_cmd_present:
            score += 0.15
            evidence.append("Recent operation chain contains transfer request")
        if auto_mode:
            score += 0.05
            evidence.append("Line was in AUTO mode, so timeout likely happened during normal cycle")

        case_hit = any(d.source == "case" and "jam" in d.snippet.lower() for d in docs)
        if case_hit:
            score += 0.15
            evidence.append("Historical case retrieval shows similar transfer jam pattern")

        candidates.append(CandidateCause(
            title="Transfer sensor not triggered due to workpiece jam",
            score=round(min(score, 0.95), 2),
            evidence=evidence,
            missing_checks=missing + ["Check transfer zone for stuck workpiece"],
        ))

        score2 = 0.18
        evidence2 = []
        if sensor_off:
            score2 += 0.2
            evidence2.append("PE_14 not triggered, could be caused by sensor contamination or failure")
        if not conveyor_high_current:
            score2 += 0.1
        if case_hit:
            score2 += 0.05
        candidates.append(CandidateCause(
            title="Photoelectric sensor PE_14 contaminated or failed",
            score=round(min(score2, 0.8), 2),
            evidence=evidence2,
            missing_checks=["Clean PE_14 lens", "Check PE_14 indicator and IO wiring"],
        ))

        score3 = 0.12
        evidence3 = []
        if air_low:
            score3 += 0.35
            evidence3.append("Air pressure low flag is ON, transfer actuator may not reach end position")
        candidates.append(CandidateCause(
            title="Cylinder did not reach position due to low air pressure",
            score=round(min(score3, 0.75), 2),
            evidence=evidence3,
            missing_checks=["Measure pneumatic pressure", "Inspect FRL and actuator leak"],
        ))

        candidates.sort(key=lambda c: c.score, reverse=True)
        return candidates

    def infer(self, signal_context: dict, docs: list):
        alarm_code = signal_context.get("alarm_code")
        alarm_entry = self.alarm_dict.get(alarm_code, {
            "message": signal_context.get("alarm_message", "Unknown alarm")
        })

        if alarm_code == "ALM-204":
            ranked = self._score_alarm_204(signal_context, docs)
        else:
            ranked = [CandidateCause(
                title="Insufficient knowledge coverage for this alarm code",
                score=0.25,
                evidence=["Alarm code not found in specialized rule pack"],
                missing_checks=["Review manual", "Add historical cases", "Confirm interlock states"],
            )]

        return RootCauseResult(
            alarm_code=alarm_code,
            alarm_message=alarm_entry.get("message", signal_context.get("alarm_message", "Unknown alarm")),
            top_cause=ranked[0],
            alternatives=ranked[1:],
            evidence_docs=docs,
        )
