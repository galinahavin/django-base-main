from django import forms

class DateForm(forms.Form):
    start = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    stop = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
