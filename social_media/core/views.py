"""Application endpoints
"""
# Django
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from core.forms import (
    LoginForm,
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm,
)
from django.contrib.auth.decorators import login_required
from core.models import Profile


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "account/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Utworzenie nowego użytkownika ale jeszcze nie zapisujemy go w bazie
            new_user = user_form.save(commit=False)
            # Nie wprowadzamy bezpośrednio tylko szyfrujemy
            new_user.set_password(user_form.cleaned_data["password"])
            profile = Profile.objects.create(user=new_user)
            new_user.save()
            return render(
                request, "account/register_done.html", {"new_user": new_user}
            )
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


def user_login(request):
    """Process posted form or return empty to fill and be processed
    login vs authenticate
    authenticate only returns user if credentials are valid
    while login actually puts him into authenticated session
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            c_d = form.cleaned_data
            user = authenticate(
                username=c_d["username"], password=c_d["password"]
            )

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse(
                        "Uwierzytelnianie zakończyło się sukcesem"
                    )
                return HttpResponse("Konto jest zablokowane")
            return HttpResponse("Nieprawidłowe dane uwierzytelniające")
    else:
        form = LoginForm()

    return render(request, "account/login.html", {"form": form})


@login_required
def dashboard(request):
    return render(
        request=request,
        template_name="account/dashboard.html",
        context={"section": "dashboard"},
    )
