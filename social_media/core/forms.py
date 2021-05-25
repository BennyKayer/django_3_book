"""Login, register forms
"""

from django import forms
from django.contrib.auth.models import User
from core.models import Profile


class LoginForm(forms.Form):
    """Login and begin authenticated session"""

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Powtórz hasło", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "email")

    def clean_password2(self):
        """clean_[nazwa_pola] to takie dopisywanie do is_valid()

        Raises:
            forms.ValidationError: Błąd jeżeli hasła nie są takie same

        Returns:
            str: zwalidowane hasło
        """
        c_d = self.cleaned_data
        if c_d["password"] != c_d["password2"]:
            raise forms.ValidationError("Hasła nie są identyczne")
        return c_d["password2"]


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("date_of_birth", "photo")
