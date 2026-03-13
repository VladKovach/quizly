# Quizly - Video-to-Quiz API

A Django REST Framework backend that converts YouTube videos into quiz sets, with JWT auth and user-scoped quiz management.

## ✅ Overview

- User registration and login with JWT (refresh tokens in secure cookies)
- Create quizzes by submitting a YouTube video URL
- Automatic transcript extraction (youtube-transcript-api)
- AI-powered quiz generation (google-genai, Gemini models)
- Quiz CRUD operations (list, retrieve, update, delete)

## 📦 Tech stack

- Python 3.8+
- Django 6.0
- Django REST Framework
- djangorestframework-simplejwt
- google-genai (Gemini API)
- youtube-transcript-api

## 🔑 Required env vars

- GEMINI_API_KEY — required to call Google Gemini AI API
- .env is loaded automatically by python-dotenv

## 🛠 Setup

1. Clone repository

`ash
git clone <your-repo-url> quizly
cd quizly
`

2. Create virtual env and activate

Windows (PowerShell):
`powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
`

Windows (CMD):
`cmd
python -m venv .venv
.venv\Scripts\activate.bat
`

Linux/macOS:
`ash
python3 -m venv .venv
source .venv/bin/activate
`

3. Install dependencies

`ash
pip install -r requirements.txt
`

4. Create .env and set key

`ash
copy .env.template .env
`

Add:

`ini
GEMINI_API_KEY=your_gemini_api_key
`

5. Apply migrations

`ash
python manage.py makemigrations
python manage.py migrate
`

6. Create superuser

`ash
python manage.py createsuperuser
`

7. Run server

`ash
python manage.py runserver
`

Default: http://127.0.0.1:8000/

## 🌐 API Endpoints

### Authentication

- POST /api/register/
  - body: email, username, password, confirmed_password

- POST /api/login/
  - body: username, password

- POST /api/logout/

- POST /api/token/refresh/

All auth endpoints use cookies:

- access_token, refresh_token (HttpOnly, secure, samesite=Lax)

### Quizzes (JWT + authenticated)

- GET /api/quizzes/ (list user's quizzes)
- POST /api/quizzes/ (generate quiz from url)
  - request body: url (YouTube URL)
  - auto-creates quiz + questions by parsing video transcript & calling Gemini
  - if quiz exists for same video_url and user, returns existing quiz (status 200)

- GET /api/quizzes/<id>/ (retrieve quiz)
- PUT/PATCH /api/quizzes/<id>/ (update title/description)
- DELETE /api/quizzes/<id>/ (delete quiz)

PUT/PATCH/DELETE are guarded by IsQuizCreator and IsAuthenticated.

## 🧩 Data models

### Quiz

- user (FK to User)
- title
- description
- video_url
- created_at, updated_at
- related questions

### Question

- quiz (FK)
- question_title
- question_options (JSON array of 4 items)
- answer
- created_at, updated_at

## 🤖 AI flow

1. video_url -> get_video_transcript (from YouTube transcript API)
2. transcript -> generate_quizzes with Gemini (prompt enforces strict JSON output)
3. response parsed by parse_ai_responce and saved as Quiz + Question set

## 🧪 Tests

`ash
pytest
`

## 📘 Admin

- Visit http://127.0.0.1:8000/admin/
- Login with superuser

## ⚠️ Security

- Cookie-based JWT tokens are secure=True (HTTPS required in production)
- Refresh token blacklist is supported via RefreshToken.blacklist()
