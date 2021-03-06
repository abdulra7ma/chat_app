from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Account


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label="Enter Username", min_length=4, max_length=50, help_text="Required"
    )
    email = forms.CharField(
        max_length=100,
        help_text="Required",
        error_messages={"required": "Sorry, you will need an email"},
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = (
            "username",
            "email",
        )

    def clean_username(self):
        user_name = self.cleaned_data["username"].lower()
        r = Account.objects.filter(username=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords do not match.")
        return cd["password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Please use another Email, that is already taken"
            )
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Username"})
        self.fields["email"].widget.attrs.update(
            {
                # "class": "form-control mb-3",
                "placeholder": "E-mail",
                "name": "email",
                "id": "id_email",
            }
        )
        self.fields["password"].widget.attrs.update({"placeholder": "Password"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Repeat Password"})


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Email",
                "id": "login-username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "id": "login-pwd",
            }
        )
    )
