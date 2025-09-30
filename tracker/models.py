from django.db import models
from django.contrib.auth.models import User

class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications", null=True, blank=True)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default="Applied")
    date_applied = models.DateField(auto_now_add=True)

    # NEW FIELDS
    rounds = models.PositiveSmallIntegerField(default=0)  # total rounds completed
    salary_offered = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    job_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    interview_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.company} - {self.position} ({self.status})"


class Interview(models.Model):
    class Format(models.TextChoices):
        PHONE = "Phone", "Phone"
        ONLINE = "Online", "Online"
        ONSITE = "Onsite", "Onsite"
        OTHER = "Other", "Other"

    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name="interviews")
    round_number = models.PositiveSmallIntegerField()
    date = models.DateField(null=True, blank=True)
    format = models.CharField(max_length=20, choices=Format.choices, default=Format.ONLINE)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Interview r{self.round_number} - {self.application.company} ({self.application.position})"


class InterviewQuestion(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=300)
    topic = models.CharField(max_length=100, blank=True)  # e.g. "System Design", "Behavioral"
    was_asked = models.BooleanField(default=True)
    my_answer = models.TextField(blank=True)

    def __str__(self):
        return self.question_text[:60]

