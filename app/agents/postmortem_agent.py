from datetime import datetime
from app.core.models import PostmortemReport
from app.utils.report_templates import build_timeline


class PostmortemAgent:
    def generate(self, event, root_cause_result, action_plan):
        report_id = f"RCA-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        timeline = build_timeline(event.timestamp, [op.model_dump() for op in event.recent_operations])
        summary = (
            f"Alarm {root_cause_result.alarm_code} at station {event.station_id} was analyzed. "
            f"Top cause: {root_cause_result.top_cause.title}."
        )
        preventive = [
            "Add this case to approved troubleshooting knowledge base",
            "Review PM plan for transfer sensor cleaning",
            "Monitor repeated occurrences by station and shift",
        ]
        return PostmortemReport(
            report_id=report_id,
            summary=summary,
            timeline=timeline,
            root_cause=root_cause_result.top_cause.title,
            evidence=root_cause_result.top_cause.evidence,
            actions_taken=action_plan.steps,
            preventive_actions=preventive,
        )
