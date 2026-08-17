from __future__ import annotations

from collections import defaultdict


def aggregate_learning(experiments: list[dict]) -> list[dict]:
    groups = defaultdict(list)
    for row in experiments:
        groups[(row.get("language"), row.get("page_type", "unknown"), row.get("change_type"))].append(row)
    output = []
    for (language, page_type, change_type), rows in sorted(groups.items()):
        known = [row for row in rows if row.get("result") in {"WIN","NEUTRAL","LOSS"}]
        wins = sum(row.get("result") == "WIN" for row in known)
        output.append({"language":language,"page_type":page_type,"optimization_type":change_type,"sample_size":len(known),"success_rate":round(wins/len(known),4) if known else None,"risk_policy_override":False})
    return output
