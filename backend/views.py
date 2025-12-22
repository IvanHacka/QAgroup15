from django.http import JsonResponse, Http404
from .repo import BugRepo


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
