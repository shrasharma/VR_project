from django import forms
from .models import PreAssessment

class PreAssessmentForm(forms.ModelForm):
    class Meta:
        model = PreAssessment
        fields = ['severity_now', 'main_triggers', 'physical_symptoms', 'main_goal']
        widgets = {
            'severity_now': forms.NumberInput(attrs={'min': 0, 'max': 10}),
            'main_triggers': forms.Textarea(attrs={'rows': 3}),
            'physical_symptoms': forms.Textarea(attrs={'rows': 3}),
            'main_goal': forms.Textarea(attrs={'rows': 3}),
        }
