from django.http import JsonResponse, Http404
from .repo import BugRepo
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse, Http404
from .services import BugService


def bug_list(request):
    bugs = BugRepo.list()
    return JsonResponse([b.id for b in bugs], safe=False)

def bug_detail(request, bug_id: str):
    bug = BugRepo.get(bug_id)

    if bug is None:
        raise Http404("Bug not found")

    data = {
        "id": bug.id,
        "title": bug.title,
        "description": bug.description,
        "status": bug.status,
        "priority": bug.priority,
        "screenshots": bug.screenshots,
        "assigned_to": bug.assigned_to,
        "created": bug.created,
        "updated": bug.updated,
    }

    return JsonResponse(data)

@csrf_exempt
def bug_update(request, bug_id: str):
    if request.method not in ["PUT", "PATCH"]:
        return JsonResponse({"error": "Method not allowed"}, status=405)

    service = BugService(BugRepo())

    try:
        body = json.loads(request.body.decode("utf-8"))

        title = body.get("title")
        description = body.get("description")

        updated_bug = service.update_bug_details(
            bug_id=bug_id,
            title=title,
            description=description
        )

        return JsonResponse(updated_bug.to_dict(), status=200)

    except ValueError as e:
        msg = str(e)
        if "not found" in msg.lower():
            raise Http404(msg)
        return JsonResponse({"error": msg}, status=400)

