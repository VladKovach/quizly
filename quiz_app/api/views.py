from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from quiz_app.api.permissions import IsQuizCreator
from quiz_app.api.serializers import (
    QuizCreateSerializer,
    QuizDetailSerializer,
    QuizSerializer,
)
from quiz_app.models import Quiz


class QuizListCreateView(ListCreateAPIView):
    """QuizListCreateView description"""

    def get_queryset(self):
        """Return quizzes belonging to the authenticated user"""
        return Quiz.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """Use QuizCreateSerializer for POST requests, otherwise QuizSerializer"""
        if self.request.method == "POST":
            return QuizCreateSerializer
        return QuizSerializer

    def create(self, request, *args, **kwargs):
        """Override create to check for existing quiz with same video URL before creating a new one"""
        url = request.data.get("url")
        # renew = request.data.get("renew", False)

        existing_quiz = Quiz.objects.filter(
            video_url=url, user=request.user
        ).first()

        if existing_quiz:
            # if not renew: ich werde das nach der Abgabe implementieren
            serializer = QuizSerializer(existing_quiz)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # else:
        #     existing_quiz.delete()

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Set the user field to the authenticated user when creating a quiz"""
        serializer.save(user=self.request.user)


class QuizDetailView(RetrieveUpdateDestroyAPIView):
    """QuizDetailView description"""

    queryset = Quiz.objects.all()
    serializer_class = QuizDetailSerializer
    permission_classes = [IsAuthenticated, IsQuizCreator]
    lookup_field = "id"
