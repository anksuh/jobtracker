from django import forms
from django.forms import inlineformset_factory
from .models import JobApplication, Interview, InterviewQuestion

STATUS_CHOICES = [
    ("Applied", "Applied"),
    ("Interview", "Interview"),
    ("Offer", "Offer"),
    ("Rejected", "Rejected"),
    ("On Hold", "On Hold"),
]

class JobApplicationForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select())
    interview_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    salary_offered = forms.DecimalField(required=False, max_digits=9, decimal_places=2,
                                        widget=forms.NumberInput(attrs={"step": "0.01", "min": "0"}))
    rounds = forms.IntegerField(required=False, min_value=0,
                                widget=forms.NumberInput(attrs={"min": "0"}))

    class Meta:
        model = JobApplication
        fields = [
            "company", "position", "status",
            "job_url", "interview_date", "notes",
            "rounds", "salary_offered", "rejection_reason",
        ]

class InterviewForm(forms.ModelForm):
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    class Meta:
        model = Interview
        fields = ["round_number", "date", "format", "notes"]

class InterviewQuestionForm(forms.ModelForm):
    class Meta:
        model = InterviewQuestion
        fields = ["question_text", "topic", "was_asked", "my_answer"]

InterviewQuestionFormSet = inlineformset_factory(
    Interview, InterviewQuestion, form=InterviewQuestionForm, extra=3, can_delete=True
)

