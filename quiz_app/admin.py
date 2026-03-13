from django.contrib import admin

from quiz_app.models import Question, Quiz


# Register your models here.
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "created_at", "updated_at"]
    list_filter = ["user"]
    search_fields = ["title", "description"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_title", "quiz", "answer", "created_at"]
    list_filter = ["quiz"]
    search_fields = ["question_title"]
