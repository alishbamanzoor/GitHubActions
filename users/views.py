from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import re  # For regex password checks

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/user.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {"message": "Invalid credentials."})
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out"})

def is_strong_password(password):
    """
    Check if password is strong:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"\d", password) and
        re.search(r"[^\w\s]", password)
    )

def signup_view(request):
    if request.method == "POST":
        # Get and strip form data
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        # Check if any field is empty
        if not all([username, email, first_name, last_name, password, confirm_password]):
            return render(request, "users/signup.html", {
                "message": "All fields are required."
            })

        # Check if passwords match
        if password != confirm_password:
            return render(request, "users/signup.html", {
                "message": "Passwords do not match."
            })

        # Check if password is strong
        if not is_strong_password(password):
            return render(request, "users/signup.html", {
                "message": "Password must be 8+ characters long and include uppercase, lowercase, digit, and special character."
            })

        # Check if username is already taken
        if User.objects.filter(username=username).exists():
            return render(request, "users/signup.html", {
                "message": "Username already taken."
            })

        # Check if email is already in use
        if User.objects.filter(email=email).exists():
            return render(request, "users/signup.html", {
                "message": "An account with this email already exists."
            })

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Log the user in and redirect to homepage
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    # If not POST, render the sign-up form
    return render(request, "users/signup.html")