from django.urls import path
from . import views

urlpatterns = [
    path("hangman", views.HangmanView.as_view(), name="hangman"),
    path("hangman/clue", views.clue_generation, name="hangman_clue")
]