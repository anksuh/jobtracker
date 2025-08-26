from django.urls import path
from .views import home, application_list, application_create, application_edit, application_delete

urlpatterns = [
    path("", home, name="home"),
    path("applications/", application_list, name="application_list"),
    path("applications/new/", application_create, name="application_create"),
    path("applications/<int:pk>/edit/", application_edit, name="application_edit"),
    path("applications/<int:pk>/delete/", application_delete, name="application_delete"),
]

