from django import forms
from .models import WaterFaultReport

class ReportFaultForm(forms.ModelForm):
    class Meta:
        model = WaterFaultReport
        # Add latitude and longitude to the fields list
        fields = ['title', 'description', 'street_address', 'latitude', 'longitude', 'severity', 'evidence_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Burst pipe on Main Road'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'street_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional: Nearest street or landmark'}),
            'severity': forms.Select(attrs={'class': 'form-select'}),
            'evidence_image': forms.FileInput(attrs={'class': 'form-control'}),
            
            # These will be populated by JavaScript when the user clicks the map
            'latitude': forms.NumberInput(attrs={'class': 'form-control bg-light', 'readonly': 'readonly', 'id': 'id_latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control bg-light', 'readonly': 'readonly', 'id': 'id_longitude'}),
        }