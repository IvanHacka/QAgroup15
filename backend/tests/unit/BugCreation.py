import unittest
import pytest
from backend.models.Bug import BugStatus


def test_invalid_status_rejected():
    with pytest.raises(ValueError):
        BugStatus("BROKEN")
