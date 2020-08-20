from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    title = models.CharField(max_length=256)
    is_active = models.BooleanField()

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    dimension = models.IntegerField()

    def __str__(self):
        return self.text

class User_Quiz_Answers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answers = models.CharField(max_length=250)
    is_complete = models.BooleanField()
    dt_saved = models.DateTimeField(auto_now=True)

