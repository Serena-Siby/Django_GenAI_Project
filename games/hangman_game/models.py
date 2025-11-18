from django.db import models

# Create your models here.
class Hangman(models.Model):
    id = models.AutoField(primary_key=True)
    words = models.TextField()
    category = models.TextField()
    clue_1 = models.TextField()
    clue_2 = models.TextField()
    clue_3 = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"The word is {self.words}"
