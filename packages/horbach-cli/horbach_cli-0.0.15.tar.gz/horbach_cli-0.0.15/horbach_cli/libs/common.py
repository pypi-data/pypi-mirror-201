import typer

LOG_LVL = [
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
]


def log_lvl_callback(value: str):
    lvls = [lvl.lower() for lvl in LOG_LVL]
    lvls.extend(LOG_LVL)
    if value not in lvls:
        raise typer.BadParameter(f"Only {LOG_LVL} are allowed")
    return value
