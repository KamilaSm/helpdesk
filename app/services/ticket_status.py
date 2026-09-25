ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "open": {"in_progress"},
    "in_progress": {"waiting", "resolved"},
    "waiting": {"in_progress", "resolved"},
    "resolved": {"closed", "in_progress"},
    "closed": {"in_progress"},
}


def is_transition_allowed(old_status: str, new_status: str) -> bool:
    if old_status == new_status:
        return True
    return new_status in ALLOWED_TRANSITIONS.get(old_status, set())