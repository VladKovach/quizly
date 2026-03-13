# Quizly - Video-to-Quiz API

A Django REST Framework backend that converts YouTube videos into quiz sets, with JWT auth and user-scoped quiz management.

## ✅ Overview

- User registration and login with JWT (refresh tokens in secure cookies)
- Create quizzes by submitting a YouTube video URL
- Automatic transcript extraction (youtube-transcript-api)
- AI-powered quiz generation (google-genai, Gemini models)
- Quiz CRUD operations (list, retrieve, update, delete)

## 📦 Tech stack

- Python 3.8+ [Download Python](https://www.python.org/downloads/)
- Django 6.0
- Django REST Framework
- djangorestframework-simplejwt
- google-genai (Gemini API)
- youtube-transcript-api

## 🔑 Required env vars

- GEMINI_API_KEY — required to call Google Gemini AI API
- .env is loaded automatically by python-dotenv

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/VladKovach/quizly.git
cd Coderr
```

### Step 2: Create and Activate a Virtual Environment

#### On Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### On Windows (Command Prompt):

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

#### On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Verify installation:

```bash
pip list
```

### Step 4: Environment Setup

#### Copy .env

```
cp .env.template .env
```

### Step 5: Database Setup

#### Apply Migrations

Create the database tables and apply all migrations:

```bash
# Create any pending migrations
python manage.py makemigrations

# Apply migrations to the database
python manage.py migrate
```

### Step 6: Create a Superuser (Admin)

Create an admin account to access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to enter:

- Username
- Email
- Password

### Step 7: Running the Application 🏃

#### Start the Development Server

```bash
python manage.py runserver
```

The server will run at: **http://127.0.0.1:8000/**

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

## 🤖 AI flow

1. video_url -> get_video_transcript (from YouTube transcript API)
2. transcript -> generate_quizzes with Gemini
3. response parsed and saved as Quiz + Question set

## 🧪 Tests

```bash
pytest
```

## 📘 Admin

- Visit http://127.0.0.1:8000/admin/
- Login with superuser

## ⚠️ Security

- Cookie-based JWT tokens are secure=True (HTTPS required in production)
- Refresh token blacklist is supported via RefreshToken.blacklist()
