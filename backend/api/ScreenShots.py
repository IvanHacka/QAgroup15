from backend.services.ScreenshotsServices import ScreenshotsServices


def upload_screenshots(request, bug_id):
    files = request.files
    ScreenshotsServices.add_screenshots(bug_id, files)
    return {"message": "ScreenShots Uploaded"}