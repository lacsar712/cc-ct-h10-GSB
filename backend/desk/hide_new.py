"""H10 fixed: once a submission has landed successfully, the overview must
show every row (including the newest id) and must not stay in the
“整理中” (organizing) filtering mode. All hide hooks are therefore off and
the drop helpers are pass-through."""


def drop_newest(rows):
    # 不再丢最新一行：成功落盘的记录必须保留在总览里。
    return list(rows)


def drop_high_ids(rows, threshold: int = 10**9):
    # 不再按 id 阈值过滤：任何已提交成功的编号都要可见。
    return list(rows)


def show_organizing_badge() -> bool:
    return False


def client_should_drop_max_id() -> bool:
    return False


def overview_stuck_organizing() -> bool:
    """FIXED: success landed -> overview leaves organizing mode, no hiding."""
    return False


def success_still_filtered_as_organizing() -> bool:
    """FIXED: just-succeeded rows stay visible, never hidden as organizing."""
    return False


def explain() -> str:
    return "hide_new fixed: 落盘成功后不再按整理中口径隐藏最新记录"
