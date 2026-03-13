from rest_framework.permissions import BasePermission


class IsQuizCreator(BasePermission):
    """Custom permission to allow only quiz creators to access their quizzes."""

    def has_object_permission(self, request, view, obj):

        return request.user == obj.user
