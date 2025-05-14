from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    features = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter features separated by commas'}),
        help_text='Enter features separated by commas (e.g., GPS, Bluetooth, Leather Seats)',
        required=False
    )
    
    class Meta:
        model = Car
        fields = ['name', 'model', 'image', 'price', 'status', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 