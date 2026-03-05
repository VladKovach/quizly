from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from quiz_app.api.serializers import QuizCreateSerializer, QuizSerializer
from quiz_app.models import Quiz


class QuizListCreateView(ListCreateAPIView):
    queryset = Quiz.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return QuizCreateSerializer
        return QuizSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuizDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
