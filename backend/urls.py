from django.urls import path
from .views import bug_list, bug_detail

urlpatterns = [
    path("bugs/", bug_list),
    path("bugs/<str:bug_id>/", bug_detail),
    path("bugs/<str:bug_id>/edit/", views.bug_update),
]
