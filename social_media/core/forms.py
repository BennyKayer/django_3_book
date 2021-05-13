"""Login, register forms
"""

from django import forms


class LoginForm(forms.Form):
    """Login and begin authenticated session"""

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
