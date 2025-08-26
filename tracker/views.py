from django.http import HttpResponse
from django.shortcuts import render
from .models import JobApplication

def home(request):
    return HttpResponse("Job Tracker is running ✅")

def application_list(request):
    applications = JobApplication.objects.all().order_by("-date_applied")
    return render(request, "tracker/application_list.html", {"applications": applications})

