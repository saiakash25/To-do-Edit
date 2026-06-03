from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Todo

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)

    email = forms.EmailField()

    message = forms.CharField(
        widget=forms.Textarea
    )

    def clean_name(self):
        name = self.cleaned_data['name']

        if not re.match(r'^[A-Za-z ]+$', name):
            raise ValidationError(
                "Name can contain only letters and spaces."
            )

        return name
    
    def clean_message(self):
        message = self.cleaned_data['message']

        if len(message.strip()) < 5:
            raise ValidationError(
                "Message must be at least 5 characters."
            )

        return message
    
class RegisterForm(forms.Form):
        
        username = forms.CharField()
        password = forms.CharField(
            widget=forms.PasswordInput
        )
        confirm_password = forms.CharField(
            widget=forms.PasswordInput
        )

        def clean_username(self):
            username = self.cleaned_data["username"]
            if len(username) < 5:
                raise forms.ValidationError(
                    "Username too short"
                )
            return username
        
        def clean(self):

            cleaned_data = super().clean()

            password = cleaned_data.get("password")
            confirm = cleaned_data.get("confirm_password")

            if password != confirm:

                raise forms.ValidationError(
                    "Passwords do not match"
                )

            return cleaned_data
        

class TodoForm(forms.ModelForm):

     class Meta:
        model = Todo

        fields = [
            "title",
            "assigned_to",
        ]