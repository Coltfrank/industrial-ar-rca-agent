from app.connectors.plc_mock import snapshot_to_map


class SignalAgent:
    def collect(self, event):
        plc_map = snapshot_to_map([p.model_dump() for p in event.plc_snapshot])
        last_actions = [op.model_dump() for op in event.recent_operations][-5:]
        trigger_summary = {
            "alarm_code": event.alarm_code,
            "alarm_message": event.alarm_message or "",
            "mode": event.mode,
            "line": event.line_id,
            "station": event.station_id,
            "equipment": event.equipment_id,
            "process_context": event.process_context,
            "plc_map": plc_map,
            "recent_actions": last_actions,
        }
        return trigger_summary
