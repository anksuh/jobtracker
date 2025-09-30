from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.db.models import Count

from .models import JobApplication, Interview, InterviewQuestion
from .forms import JobApplicationForm, InterviewForm, InterviewQuestionFormSet


# ===== Dashboard (per-user) =====
def home(request):
    qs = JobApplication.objects.filter(user=request.user) if request.user.is_authenticated else JobApplication.objects.none()

    total = qs.count()
    by_status = {
        "Applied": qs.filter(status="Applied").count(),
        "Interview": qs.filter(status="Interview").count(),
        "Offer": qs.filter(status="Offer").count(),
        "Rejected": qs.filter(status="Rejected").count(),
        "On_Hold": qs.filter(status="On Hold").count(),
    }
    recent = qs.order_by("-date_applied")[:5]

    # Question analytics
    iq = InterviewQuestion.objects.filter(interview__application__in=qs)
    top_questions_overall = (
        iq.values("question_text").annotate(cnt=Count("id")).order_by("-cnt")[:5]
    )
    by_role = {}
    for position in qs.values_list("position", flat=True).distinct():
        role_qs = iq.filter(interview__application__position=position)
        top_for_role = (
            role_qs.values("question_text").annotate(cnt=Count("id")).order_by("-cnt")[:3]
        )
        by_role[position] = list(top_for_role)

    return render(request, "tracker/home.html", {
        "total": total,
        "by_status": by_status,
        "recent": recent,
        "top_questions_overall": top_questions_overall,
        "top_questions_by_role": by_role,
    })


# ===== Applications CRUD (per-user) =====
@login_required
def application_list(request):
    applications = JobApplication.objects.filter(user=request.user).order_by("-date_applied")
    return render(request, "tracker/application_list.html", {"applications": applications})

@login_required
def application_create(request):
    if request.method == "POST":
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()
            messages.success(request, "Application created.")
            return redirect("application_list")
    else:
        form = JobApplicationForm()
    return render(request, "tracker/application_form.html", {"form": form})

@login_required
def application_edit(request, pk):
    app = get_object_or_404(JobApplication, pk=pk, user=request.user)
    if request.method == "POST":
        form = JobApplicationForm(request.POST, instance=app)
        if form.is_valid():
            form.save()
            messages.success(request, "Application updated.")
            return redirect("application_list")
    else:
        form = JobApplicationForm(instance=app)
    return render(request, "tracker/application_form.html", {"form": form, "editing": True, "app": app})

@login_required
def application_delete(request, pk):
    app = get_object_or_404(JobApplication, pk=pk, user=request.user)
    if request.method == "POST":
        app.delete()
        messages.success(request, "Application deleted.")
        return redirect("application_list")
    return render(request, "tracker/application_confirm_delete.html", {"app": app})

# ===== NEW: Application detail & Interview creation =====
@login_required
def application_detail(request, pk):
    app = get_object_or_404(JobApplication, pk=pk, user=request.user)
    interviews = app.interviews.order_by("round_number")
    return render(request, "tracker/application_detail.html", {"app": app, "interviews": interviews})

@login_required
def interview_create(request, application_pk):
    app = get_object_or_404(JobApplication, pk=application_pk, user=request.user)
    if request.method == "POST":
        form = InterviewForm(request.POST)
        formset = InterviewQuestionFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            interview = form.save(commit=False)
            interview.application = app
            interview.save()
            formset.instance = interview
            formset.save()
            # bump rounds if needed
            if interview.round_number > (app.rounds or 0):
                app.rounds = interview.round_number
                app.save(update_fields=["rounds"])
            messages.success(request, "Interview & questions saved.")
            return redirect("application_detail", pk=app.pk)
    else:
        next_round = (app.rounds or 0) + 1
        form = InterviewForm(initial={"round_number": next_round})
        formset = InterviewQuestionFormSet()
    return render(request, "tracker/interview_form.html", {"app": app, "form": form, "formset": formset})


# ===== Auth: Signup =====
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect("application_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

