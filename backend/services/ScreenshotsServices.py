# import os
#
# from backend.repo.BugRepo import BugRepo
# from backend.repo.ScreenRepo import ScreenRepo
# from backend.utils.ImageValidation import validate_screenshot
#
#
# class ScreenshotsServices:
#     @staticmethod
#     def add_screenshot(bug_id, files: list[bytes]):
#         bug = BugRepo.get_by_id(bug_id)
#         if not bug:
#             raise ValueError(f"Bug with id {bug_id} not found")
#
#         saved = []
#
#         try:
#             for i, f in enumerate(files):
#                 validate_screenshot(f)
#                 file_name = f"bug_{bug_id}_{len(bug.screenshot)+i}.png"
#                 temp = ScreenRepo.save_screenshot_temp(f)
#
#                 saved.append((temp, file_name))
#
#             # Update entity
#             bug.screenshot.extend(n for _, n in saved)
#             BugRepo.save(bug)
#
#             for temp, f in saved:
#                 ScreenRepo.commit_screenshot(temp, f)
#
#         except Exception:
#             for temp, _ in saved:
#                 ScreenRepo.delete_screenshot(temp)
#             raise

from PIL import Image
import io


from backend.repo.ScreenRepo import ScreenRepo
from backend.repo.BugRepo import BugRepo

class ScreenshotsServices:
    def __init__(self, bug_repo: BugRepo):
        self.bug_repo = bug_repo

    @staticmethod
    def _validate_image_bytes(file_bytes: bytes) -> str:
        try:
            img = Image.open(io.BytesIO(file_bytes))
            img.verify()

            if img.format not in ("PNG", "JPEG"):
                raise ValueError("Only PNG and JPEG images are allowed")

            return "png" if img.format == "PNG" else "jpg"

        except Exception:
            raise ValueError("Invalid image file")

    def add_screenshots(self, bug_id: str, uploaded_files) -> dict:
        bug = self.bug_repo.get_by_id(bug_id)
        if not bug:
            raise ValueError(f"Bug with id {bug_id} not found")

        saved_temp = []  # (temp_path, filename)

        try:
            start_index = len(bug.screenshot)

            for i, f in enumerate(uploaded_files):
                file_bytes = f.read()  # FileStorage -> bytes
                self._validate_image_bytes(file_bytes)

                # keep extension consistent with actual type if you want
                # here we name by detected type:
                ext = self._validate_image_bytes(file_bytes)


                filename = f"bug_{bug_id}_{start_index + i}.{ext}"
                temp_path = ScreenRepo.save_temp(file_bytes)
                saved_temp.append((temp_path, filename))

            # update bug metadata first (filenames)
            bug.screenshot.extend([name for _, name in saved_temp])

            # persist to Bugs.json
            ok = self.bug_repo.update(bug)
            if not ok:
                raise Exception("Failed to update bug with screenshot references")

            # commit files to disk
            for temp_path, filename in saved_temp:
                ScreenRepo.commit(temp_path, filename)

            return {"message": "Screenshots uploaded", "files": bug.screenshot}

        except Exception:
            for temp_path, _ in saved_temp:
                ScreenRepo.delete(temp_path)
            raise

