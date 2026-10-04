from django import forms
from students.models import Placement

class UpdateSupervisionForm(forms.ModelForm):
    """
    Update supervision status form
    """
    class Meta:
        model = Placement
        fields = [
            'visit_status',
            'planned_date',
            'visit_date'
        ]
        widgets = {
            'planned_date': forms.DateInput(attrs={'type': "date"}),
            'visit_date': forms.DateInput(attrs={'type': "date"})
        }