from django.urls import path
from .views import home, application_list

urlpatterns = [
    path("", home, name="home"),
    path("applications/", application_list, name="application_list"),
]


