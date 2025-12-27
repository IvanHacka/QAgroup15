# import os
# import tempfile
#
# ScreenshotsFile = "data/screenshots"
#
# class ScreenRepo:
#     # Save in temp file safely
#     # Return path
#     def save_screenshot_temp(file: bytes) -> str:
#         fd, path = tempfile.mkstemp()
#         with os.fdopen(fd, "wb") as f:
#             f.write(file)
#         return path
#
#     @staticmethod
#     def commit_screenshot(filename, path):
#         final_path = os.path.join(ScreenshotsFile, filename)
#         os.replace(path, final_path) # Overwrite the temp file path
#
#     @staticmethod
#     def delete_screenshot(path):
#         if os.path.exists(path):
#             os.remove(path)

import os
import tempfile

SCREENSHOTS_DIR = "data/screenshots"

class ScreenRepo:
    @staticmethod
    def ensure_dir():
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    @staticmethod
    def save_temp(file_bytes: bytes) -> str:
        fd, path = tempfile.mkstemp()
        with os.fdopen(fd, "wb") as f:
            f.write(file_bytes)
        return path

    @staticmethod
    def commit(temp_path: str, filename: str) -> str:
        ScreenRepo.ensure_dir()
        final_path = os.path.join(SCREENSHOTS_DIR, filename)
        os.replace(temp_path, final_path)
        return final_path

    @staticmethod
    def delete(path: str):
        if os.path.exists(path):
            os.remove(path)



