from tokenize import TokenError

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    """User registration endpoint"""

    permission_classes = [AllowAny]

    def post(self, request):
        """Handle user registration, set JWT tokens in cookies on success"""
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # Returns the created user from create()

        # Same as LoginView — generate tokens and set cookies
        refresh = RefreshToken.for_user(user)

        response = Response(
            {"detail": "User created successfully!"},
            status=status.HTTP_201_CREATED,
        )

        response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=30 * 60,
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60,
        )

        return response


class LoginView(APIView):
    """User login endpoint, set JWT tokens in cookies on success"""

    permission_classes = [AllowAny]

    def post(self, request):
        """Handle user login"""
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)

            response = Response(
                {
                    "detail": "Login successfully!",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                }
            )

            response.set_cookie(
                key="access_token",
                value=str(refresh.access_token),
                httponly=True,
                secure=True,
                samesite="Lax",
                max_age=30 * 60,  # 30 min
            )

            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite="Lax",
                max_age=7 * 24 * 60 * 60,  # 7 days
            )

            return response

        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "No refresh token provided"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)

            response = Response({"detail": "Token refreshed"})
            response.set_cookie(
                key="access_token",
                value=new_access,
                httponly=True,
                secure=True,
                samesite="Lax",
                max_age=30 * 60,
            )

            return response

        except Exception:
            return Response(
                {"error": "Invalid refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Adds to blacklist DB table
            except TokenError:
                pass  # Already invalid, no problem

        response = Response(
            {
                "detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."
            }
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
