from django.urls import path
from .views import LoginView, RegisterView
url_patterns = [
    path('/login', LoginView.as_view()),
    path('/register', RegisterView.as_view()),
]
    