from django import forms
from .models import Coffee
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Form for adding new coffee items
class CoffeeForm(forms.ModelForm):
    class Meta:
        model = Coffee
        fields = ['name', 'price', 'quantity', 'image', 'category', 'temperature']

# Custom registration form using only username, password, phone number (stored in first_name)
class CustomRegisterForm(forms.ModelForm):

    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'password']

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if User.objects.filter(first_name=phone).exists():
            raise ValidationError("A user with this phone number already exists.")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])              # 🔐 Password hashing
        user.first_name = self.cleaned_data['phone_number']           # Store phone number in first_name
        if commit:
            user.save()
        return user


