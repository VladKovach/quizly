from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.factories import UserFactory
from quiz_app.factories import QuizFactory


class QuizTestHappy(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_list_returns_only_own_quizzes(self):
        QuizFactory.create_batch(2, user=self.user)
        QuizFactory(user=self.other_user)

        response = self.client.get(reverse("quiz-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # only user's quizzes

    def test_retrieve_quiz_ok(self):
        quiz = QuizFactory(user=self.user)

        url = reverse("quiz-detail", kwargs={"id": quiz.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_quiz_ok(self):
        quiz = QuizFactory(user=self.user)

        url = reverse(
            "quiz-detail",
            kwargs={"id": quiz.id},
        )

        response = self.client.patch(
            url,
            {
                "title": "Partially Updated Title",
                "description": "Partially Updated Description",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Partially Updated Title")
        self.assertEqual(
            response.data["description"], "Partially Updated Description"
        )

    def test_delete_quiz_ok(self):
        quiz = QuizFactory(user=self.user)

        url = reverse(
            "quiz-detail",
            kwargs={"id": quiz.id},
        )

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class QuizTestUnhappy(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.client.force_authenticate(user=self.user)

    # ── AUTH ──────────────────────────────────────────
    def test_unauthenticated_list_returns_401(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("quiz-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_retrieve_returns_401(self):
        quiz = QuizFactory(user=self.user)
        self.client.force_authenticate(user=None)

        response = self.client.get(
            reverse("quiz-detail", kwargs={"id": quiz.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ── OWNERSHIP ─────────────────────────────────────
    def test_retrieve_other_user_quiz_returns_403(self):
        quiz = QuizFactory(user=self.other_user)

        response = self.client.get(
            reverse("quiz-detail", kwargs={"id": quiz.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_other_user_quiz_returns_403(self):
        quiz = QuizFactory(user=self.other_user)

        response = self.client.patch(
            reverse("quiz-detail", kwargs={"id": quiz.id}),
            {"title": "Hacked Title"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_other_user_quiz_returns_403(self):
        quiz = QuizFactory(user=self.other_user)

        response = self.client.delete(
            reverse("quiz-detail", kwargs={"id": quiz.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ── NOT FOUND ─────────────────────────────────────
    def test_retrieve_nonexistent_quiz_returns_404(self):
        response = self.client.get(
            reverse("quiz-detail", kwargs={"id": 99999})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_quiz_returns_404(self):
        response = self.client.delete(
            reverse("quiz-detail", kwargs={"id": 99999})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ── EMPTY STATE ───────────────────────────────────
    def test_list_returns_empty_when_no_quizzes(self):
        response = self.client.get(reverse("quiz-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
