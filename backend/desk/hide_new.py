"""H10: after success, overview stays in organizing and hides newest id."""

def drop_newest(rows):
    rows = list(rows)
    if not rows:
        return rows
    return rows[1:]

def drop_high_ids(rows, threshold: int = 10**9):
    out = []
    for r in rows:
        rid = getattr(r, "id", None)
        if rid is not None and int(rid) >= threshold:
            continue
        out.append(r)
    return out

def show_organizing_badge() -> bool:
    return True

def client_should_drop_max_id() -> bool:
    return True

def overview_stuck_organizing() -> bool:
    """BUG: success already landed but overview still filters as organizing."""
    return True

def success_still_filtered_as_organizing() -> bool:
    """Hard-feature hook: just-succeeded rows stay hidden under organizing口径."""
    return True

def explain() -> str:
    return "hide_new: success landed but organizing口径 still hides newest"
