from rest_framework import serializers

from quiz_app.models import Question, Quiz
from quiz_app.services.ai_service import generate_quizzes, parse_ai_responce
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

    # renew = serializers.BooleanField(write_only=True, required=False, default=False)

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
        # get transcript
        transcript = get_video_transcript(validated_data.get("url"))
        if transcript is None:
            raise serializers.ValidationError(
                {"url": "No transcript available for this video."}
            )
        # paste transcript to gemini
        ai_response = generate_quizzes(transcript)
        print("ai_response =", ai_response)
        if isinstance(ai_response, dict) and ai_response.get("error"):
            raise serializers.ValidationError(
                {"message": f"{ai_response['message']}"}
            )

        # provide validated data
        quizze_data = parse_ai_responce(ai_response)
        print("quizze_data = ", quizze_data)
        validated_data["title"] = quizze_data["title"]
        validated_data["description"] = quizze_data["description"]
        validated_data["video_url"] = validated_data["url"]
        validated_data.pop("url")
        # validated_data.pop("renew", None)

        # create quiz
        quiz = Quiz.objects.create(**validated_data)
        # create questions
        for q in quizze_data["questions"]:
            Question.objects.create(
                question_title=q["question_title"],
                question_options=q["answer_options"],
                answer=q["answer"],
                quiz=quiz,
            )

        return quiz


class QuizDetailSerializer(QuizSerializer):
    title = serializers.CharField(max_length=120, min_length=15)
    description = serializers.CharField(max_length=300, min_length=25)

    class Meta(QuizSerializer.Meta):
        fields = QuizSerializer.Meta.fields
        read_only_fields = [
            "created_at",
            "updated_at",
            "video_url",
            "questions",
        ]
