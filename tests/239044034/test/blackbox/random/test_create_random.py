import pytest
import random
import string

def random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))


def test_create_bug_random_titles(bug_controller):
    for _ in range(20):
        title = random_string(random.randint(1, 50))
        desc = random_string(random.randint(5, 200))
        bug = bug_controller.create(title, desc, "LOW", "OPEN")
        assert bug.title == title