from desk.h10_extra_trap import organizing, skew_list
from desk.hide_new import success_still_filtered_as_organizing

def test_hide_hooks():
    assert organizing() is True
    assert success_still_filtered_as_organizing() is True
    assert skew_list([1, 2, 3]) in ([1, 2, 3], [2, 3], [1, 2])
