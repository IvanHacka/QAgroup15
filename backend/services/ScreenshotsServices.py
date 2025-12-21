import os

from backend.repo.BugRepo import BugRepo
from backend.repo.ScreenRepo import ScreenRepo
from backend.utils.ImageValidation import validate_screenshot


class ScreenshotsServices:
    @staticmethod
    def add_screenshot(bug_id, files: list[bytes]):
        bug = BugRepo.get_by_id(bug_id)
        if not bug:
            raise ValueError(f"Bug with id {bug_id} not found")

        saved = []

        try:
            for i, f in enumerate(files):
                validate_screenshot(f)
                file_name = f"bug_{bug_id}_{len(bug.screenshot)+i}.png"
                temp = ScreenRepo.save_screenshot_temp(f)

                saved.append((temp, file_name))

            # Update entity
            bug.screenshot.extend(n for _, n in saved)
            BugRepo.save(bug)

            for temp, f in saved:
                ScreenRepo.commit_screenshot(temp, f)

        except Exception:
            for temp, _ in saved:
                ScreenRepo.delete_screenshot(temp)
            raise

