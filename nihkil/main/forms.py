from django import forms
from .models import ProjectReport

class ReportForm(forms.ModelForm):
    class Meta:
        model = ProjectReport
        fields = ['title', 'report_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Report Title'}),
            'report_file': forms.FileInput(attrs={'class': 'form-control'}),
        }
