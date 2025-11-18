from rest_framework import serializers
from .models import Hangman

class HangSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hangman
        fields = ['words', 'clue_1', 'clue_2', 'clue_3']