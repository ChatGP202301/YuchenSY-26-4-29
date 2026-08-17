SCHEDULES = {"daily":"0 2 * * *", "weekly":"0 3 * * 1", "monthly":"0 4 1 * *"}


def schedule_for(kind: str) -> str:
    if kind not in SCHEDULES:
        raise ValueError(kind)
    return SCHEDULES[kind]
