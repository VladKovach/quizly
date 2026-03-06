from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class Quiz(models.Model):
    user = models.ForeignKey(
        User, related_name="quizzes", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.URLField()

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, related_name="questions", on_delete=models.CASCADE
    )
    question_title = models.CharField(max_length=200)
    question_options = models.JSONField()
    answer = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
