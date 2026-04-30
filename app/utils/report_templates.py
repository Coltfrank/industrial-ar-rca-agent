def build_timeline(event_timestamp: str, operations: list[dict]) -> list[str]:
    timeline = [f"{event_timestamp} - Alarm captured by Signal Agent"]
    for op in operations:
        timeline.append(f"{op['ts']} - {op['action']} (by {op.get('operator', 'system')})")
    return timeline
