import pytest


def bug_test_assign_single_user(controller):
    bug = controller.create("Bug", "This is a test bug", "LOW")
    updated = controller.assign(bug.id, "staff01")
    assert "staff01" in updated.assigned_to


def test_bug_assign_multiple_user(controller):
    bug = controller.create("Bug", "This is a test bug", "LOW")
    updated = controller.assign(bug.id, ["staff01, staff02"]) #List
    assert len(updated.assigned_to) == 2

def test_bug_assign_empty_list(controller):
    bug = controller.create("Bug", "This is a test bug", "LOW")
    with pytest.raises(Exception):
        controller.assign(bug.id, [])