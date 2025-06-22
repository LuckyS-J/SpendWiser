from django import forms
from .models import Goal


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'target', 'current']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-100'}),
            'target': forms.NumberInput(attrs={'class': 'w-100'}),
            'current': forms.NumberInput(attrs={'class': 'w-100'}),
        }

    def clean_current(self):
        current = self.cleaned_data.get('current')
        if current < 0:
            raise forms.ValidationError("Current cannot be negative")
        return current

    def clean_target(self):
        target = self.cleaned_data.get('target')
        if target < 0:
            raise forms.ValidationError("Target cannot be negative")
        return target

    def clean(self):
        cleaned_data = super().clean()
        target = cleaned_data.get('target')
        current = cleaned_data.get('current')
        if target and current and current > target:
            raise forms.ValidationError("Current value cannot exceed target.")


class ProgressForm(forms.Form):
    progress = forms.IntegerField(
        min_value=0,
        label="Add Amount",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 100%; background-color: #122130; color: #e0e6f0; border: 1px solid #2c3e50;'
        })
    )

    def __init__(self, *args, goal=None, **kwargs):
        self.goal = goal
        super().__init__(*args, **kwargs)

    def clean_progress(self):
        progress = self.cleaned_data['progress']
        if self.goal and (self.goal.current + progress) > self.goal.target:
            raise forms.ValidationError(
                "Progress cannot exceed the target value.")
        return progress
