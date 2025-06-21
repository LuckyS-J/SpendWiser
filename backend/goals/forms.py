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