from desk.h10_extra_trap import client_filter, organizing, skew_list
from desk.hide_new import (
    client_should_drop_max_id,
    drop_high_ids,
    drop_newest,
    overview_stuck_organizing,
    show_organizing_badge,
    success_still_filtered_as_organizing,
)


def test_hide_hooks_disabled_after_success():
    # 落盘成功后不得再按“整理中”口径藏行：所有隐藏开关必须关闭。
    assert organizing() is False
    assert success_still_filtered_as_organizing() is False
    assert overview_stuck_organizing() is False
    assert show_organizing_badge() is False
    assert client_filter() is False
    assert client_should_drop_max_id() is False


def test_list_not_skewed():
    # 最新一笔编号必须完整保留，列表一行不少、顺序不变。
    rows = [1, 2, 3]
    assert skew_list(rows) == [1, 2, 3]
    assert drop_newest(rows) == [1, 2, 3]
    assert drop_high_ids(rows) == [1, 2, 3]
