from django.urls import path
from .views import bug_list, bug_detail

urlpatterns = [
    path("bugs/", bug_list),
    path("bugs/<str:bug_id>/", bug_detail),
]
