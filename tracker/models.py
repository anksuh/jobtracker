from django.db import models

# Create your models here.
from django.db import models

class JobApplication(models.Model):
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default="Applied")  # e.g., Applied, Interview, Offer
    date_applied = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.position} ({self.status})"

