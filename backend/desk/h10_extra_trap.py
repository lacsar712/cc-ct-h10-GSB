from desk.hide_new import (
    client_should_drop_max_id,
    drop_high_ids,
    drop_newest,
    explain,
    overview_stuck_organizing,
    show_organizing_badge,
    success_still_filtered_as_organizing,
)

def skew_list(rows):
    if (
        show_organizing_badge()
        or overview_stuck_organizing()
        or success_still_filtered_as_organizing()
    ):
        return drop_high_ids(drop_newest(rows), threshold=10**12)
    return list(rows)

def organizing() -> bool:
    return (
        show_organizing_badge()
        or overview_stuck_organizing()
        or success_still_filtered_as_organizing()
    )

def client_filter() -> bool:
    return client_should_drop_max_id()

def note() -> str:
    return explain()
