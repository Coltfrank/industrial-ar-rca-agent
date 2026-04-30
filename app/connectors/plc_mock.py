from typing import Dict, List


def snapshot_to_map(points: List[dict]) -> Dict[str, str]:
    return {p["tag"]: str(p["value"]) for p in points}
