import os
import tempfile

ScreenshotsFile = "data/screenshots"

class ScreenRepo:
    # Save in temp file safely
    # Return path
    def save_screenshot_temp(file: bytes) -> str:
        fd, path = tempfile.mkstemp()
        with os.fdopen(fd, "wb") as f:
            f.write(file)
        return path

    @staticmethod
    def commit_screenshot(filename, path):
        final_path = os.path.join(ScreenshotsFile, filename)
        os.replace(path, final_path) # Overwrite the temp file path

    @staticmethod
    def delete_screenshot(path):
        if os.path.exists(path):
            os.remove(path)


