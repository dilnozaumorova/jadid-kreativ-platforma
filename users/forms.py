from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from users.models import CustomUser


class UserRegisterForm(forms.ModelForm):
    password=forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Parol'}),label="Parol"
        )
    
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolni tasdiqlang'}),label="Parolni tasdiqlang"
    )
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get('password')
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Kiritilgan parollar bir-biriga mos emas")
        
        if password:
            validate_password(password)
        return cleaned_data
    
    def clean_first_name(self):
        first_name=self.cleaned_data.get('first_name')
        if len(first_name)<=2:
            raise ValidationError("Ism juda qisqa ! Kamida 3 ta harif yozing ")
        if not first_name.isalpha():
            raise forms.ValidationError("Ismda faqat harflar bo'lishi kerak.")
        return first_name
    
    def clean_last_name(self):
        last_name=self.cleaned_data.get('last_name')
        if len(last_name)<=2:
            raise ValidationError("Ism juda qisqa ! Kamida 3 ta harif yozing ")
        if not last_name.isalpha():
            raise forms.ValidationError("Ismda faqat harflar bo'lishi kerak.")
        return last_name
    
    
    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    

class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username kiriting'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parol kiriting'
        })
    )