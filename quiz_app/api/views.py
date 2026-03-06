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
    queryset = Quiz.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return QuizCreateSerializer
        return QuizSerializer

    def create(self, request, *args, **kwargs):
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
        serializer.save(user=self.request.user)


class QuizDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizDetailSerializer
    permission_classes = [IsAuthenticated, IsQuizCreator]
    lookup_field = "id"
