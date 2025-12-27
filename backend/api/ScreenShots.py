# from backend.services.ScreenshotsServices import ScreenshotsServices
#
#
# def upload_screenshots(request, bug_id):
#     files = request.files
#     ScreenshotsServices.add_screenshots(bug_id, files)
#     return {"message": "ScreenShots Uploaded"}

from flask import jsonify
from backend.services.ScreenshotsServices import ScreenshotsServices

def upload_screenshots(request, bug_id: str, screenshots_service: ScreenshotsServices):
    files = request.files.getlist("screenshots")
    if not files:
        return jsonify({"error": "No files uploaded. Use field name 'screenshots'."}), 400

    try:
        result = screenshots_service.add_screenshots(bug_id, files)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "Server error"}), 500
