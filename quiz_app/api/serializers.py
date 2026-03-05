from rest_framework import serializers

from quiz_app.models import Question, Quiz
from quiz_app.services.video_to_text import get_video_transcript


class QuestionBaseSerializer(serializers.ModelSerializer):
    """
    QuestionBaseSerializer description
    """

    class Meta:
        model = Question
        fields = ["id", "question_title", "question_options", "answer"]


class QuestionExtendedSerializer(serializers.ModelSerializer):
    """
    QuestionExtendedSerializer description
    """

    class Meta:
        model = Question
        fields = [
            "id",
            "question_title",
            "question_options",
            "answer",
            "created_at",
            "updated_at",
        ]


class QuizSerializer(serializers.ModelSerializer):
    """
    QuizSerializer description
    """

    questions = QuestionBaseSerializer(many=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "video_url",
            "questions",
        ]


class QuizCreateSerializer(serializers.ModelSerializer):
    """
    QuizCreateSerializer description
    """

    url = serializers.URLField(write_only=True)
    questions = QuestionExtendedSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "video_url",
            "questions",
            "url",
        ]
        read_only_fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "video_url",
            "questions",
            "url",
        ]

    def create(self, validated_data):
        transcript = get_video_transcript(validated_data.get("url"))

        if transcript is None:
            raise serializers.ValidationError(
                {"url": "No transcript available for this video."}
            )

        validated_data.pop("url")
        return super().create(validated_data)
