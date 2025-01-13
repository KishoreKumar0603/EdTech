# forms.py
from django import forms
from .models import Student

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=15)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Student.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already used by someone.")
        return username

    
    class Meta:
        model = Student  # Use the custom model
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'phone']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data
