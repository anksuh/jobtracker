from django.http import HttpResponse
from django.shortcuts import render
from .models import JobApplication

def home(request):
    return HttpResponse("Job Tracker is running ✅")

def application_list(request):
    applications = JobApplication.objects.all().order_by("-date_applied")
    return render(request, "tracker/application_list.html", {"applications": applications})

from django.shortcuts import render, redirect
from .forms import JobApplicationForm

def application_create(request):
    if request.method == "POST":
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("application_list")
    else:
        form = JobApplicationForm()
    return render(request, "tracker/application_form.html", {"form": form})

from django.shortcuts import get_object_or_404, redirect
from .forms import JobApplicationForm
from .models import JobApplication

def application_edit(request, pk):
    app = get_object_or_404(JobApplication, pk=pk)
    if request.method == "POST":
        form = JobApplicationForm(request.POST, instance=app)
        if form.is_valid():
            form.save()
            return redirect("application_list")
    else:
        form = JobApplicationForm(instance=app)
    return render(request, "tracker/application_form.html", {"form": form, "editing": True, "app": app})

def application_delete(request, pk):
    app = get_object_or_404(JobApplication, pk=pk)
    if request.method == "POST":
        app.delete()
        return redirect("application_list")
    return render(request, "tracker/application_confirm_delete.html", {"app": app})

