
from django.db import models
from django.contrib.auth.models import User

PHOBIA_CHOICES = [
    ('heights', 'Fear of Heights'),
    ('spider', 'Fear of Spiders'),
    ('publicspeaking', 'Public Speaking'),
]
    
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("patient", "Patient"),
        ("therapist", "Therapist"),
        ("researcher", "Researcher"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, default="")
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True, default="")
    license_no = models.CharField(max_length=100, blank=True, default="")
    experience = models.PositiveIntegerField(null=True, blank=True)
    specialization = models.CharField(max_length=200, blank=True, default="")
    institution = models.CharField(max_length=200, blank=True, default="")
    research_field = models.CharField(max_length=200, blank=True, default="")


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # ... your existing fields ...

    current_phobia = models.CharField(
        max_length=20,
        choices=PHOBIA_CHOICES,
        blank=True,
        null=True,
        help_text="Current active therapy phobia for this user."
    )
def __str__(self):
        return self.user.username


class PreAssessment(models.Model):
    """
    Stores key pre-assessment answers per user and phobia.
    (This is the short version you can edit from dashboard.)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phobia = models.CharField(max_length=20, choices=PHOBIA_CHOICES)

    # some important editable fields (you can add more later)
    severity_now = models.IntegerField(
        default=5,
        help_text="How intense is the fear right now (0–10)?"
    )
    main_triggers = models.TextField(
        blank=True,
        help_text="Situations or objects that trigger the fear."
    )
    physical_symptoms = models.TextField(
        blank=True,
        help_text="What happens in your body when you face this fear?"
    )
    main_goal = models.TextField(
        blank=True,
        help_text="What would you like to be able to do after therapy?"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'phobia')  # one assessment per phobia

    def __str__(self):
        return f"{self.user.username} - {self.phobia}"