<!-- # Django RAG Project

Project description: A Django-based backend that combines user management APIs with utilities and scripts to support Retrieval-Augmented Generation (RAG) workflows. It provides tools to ingest, chunk, and retrieve document content (e.g., PDFs) and an API-driven `user_profiles` app for authentication and account management.

Purpose: Enable developers to build RAG applications by providing an integrated backend for user handling and a set of pipelines to prepare and query document embeddings for LLM-driven retrieval and generation.

## Repository layout

- `manage.py` - Django management entry.
- `scorpian/` - Django project settings and WSGI/ASGI config. See [scorpian/settings.py](scorpian/settings.py).
- `user_profiles/` - Django app handling user accounts, auth backends, serializers, and views. Key files: [user_profiles/views.py](user_profiles/views.py), [user_profiles/serializers.py](user_profiles/serializers.py), [user_profiles/urls.py](user_profiles/urls.py).
- `RAGpipelines/` - RAG-related scripts and utilities. See the folder [RAGpipelines](RAGpipelines) for: `characterSplitter.py`, `pdf_chunker.py`, `ingetion_pipeline.py`, `retriever_pipeline.py`, `questionGeneratorPipeline.py`, `geminiPrompts.py`, and other helpers.
- `db.sqlite3` - default SQLite DB (development).
- `requirements.txt` - Python dependencies.
- `test_api.py` - test(s) present at repo root.


## Overview

This project combines a Django REST/API backend with scripts to ingest, chunk, and retrieve content (PDFs and other documents) to support RAG-style functionality. The `user_profiles` app contains registration, activation email templates, and authentication/backends to integrate with the API.

## Requirements

- Python 3.10+ (or compatible with listed `requirements.txt`)
- pip

Install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

## Setup

1. Configure environment variables (recommended):
   - `SECRET_KEY` (if overriding settings)
   - any DB or external API keys used by RAG pipelines

2. Apply migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

3. Run the development server:

```bash
python manage.py runserver
```



## API Routes Documentation
The following endpoints handle user authentication, session generation, and quiz access.

- GET `/auth/csrf_cookie/` - Retrieves and sets a CSRF token cookie required for secure form submissions and authenticated requests.

- POST `/auth/registration/` - Registers a new user account using the provided user details.
- POST `/auth/activate/` - Activates a newly registered user account using a verification token or code.
- POST `/auth/signin/` - Authenticates a user and creates a login session using their credentials.
- POST `/generate/` – Generates a new quiz session based on the provided parameters or topic.
- GET `/quiz-session/<sessionId>/` – Retrieves the details and current state of a specific quiz session.
- POST `/auth/logout/` – Logs out the authenticated user and invalidates the current session.

### 1. User Registration
**Endpoint**
POST `/auth/registration/`

**Description**
- Registers a new user account.

**Request Body Example**
```json
{
  "email": "user@example.com",
  "password": "your_password",
  "username": "your_username"
}
```

**Response**
- 201 Created – User registered successfully
- 400 Bad Request – Invalid input or user already exists

### 2. Account Activation

**Endpoint**
POST `/auth/activate/`

**Description**

- Activates a user account using the activation token sent via email after registration.

**Request Body Example**
```json
{
  "uid": "user_id",
  "token": "activation_token"
}
```
**Response**

- 200 OK – Account activated successfully
- 400 Bad Request – Invalid or expired token

### 3. Get CSRF Token

**Endpoint**
GET `/auth/csrf_cookie/`

**Description**

- Returns a CSRF token and sets it in cookies for secure authenticated requests.

**Response**

- 200 OK – CSRF cookie set successfully

**4. User Login**

**Endpoint**
POST `/auth/signin/`

Description
- Authenticates a user and creates a login session.

**Request Body Example**

```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```
**Response**
- 200 OK – Login successful
- 401 Unauthorized – Invalid credentials

### 5. User Logout
**Endpoint** POST `/auth/logout/`

**Description**
- Logs the user out and clears the session.

**Response**
- 200 OK – Logout successful

### 6. Generate Quiz Session

**Endpoint**
POST `/generate/`

**Description**

- Creates a new quiz session and returns a unique session ID.

**Response Example**
```json
{
  "sessionId": "abc123xyz"
}
```
**Response**
- 200 OK – Quiz session generated successfully

### 7. Access Quiz Session

**Endpoint**
GET `/quiz-session/{sessionId}/`

**Description**
- Retrieves quiz data associated with a specific session.

**Path Parameter**






 -->


# AI-Based MCQ Quiz Generator

## Project Overview

The AI-Based MCQ Quiz Generator is an interactive web application that allows users to generate practice quizzes on various topics using a language model (LLM) like Gemini. This project combines user authentication, dynamic quiz generation, and database management to create a seamless learning experience.

Users can sign up, log in, and generate quizzes tailored to their chosen topics and difficulty levels. The system leverages AI to generate multiple-choice questions (MCQs) in real-time, storing them in a database and delivering them based on the user's session for practice.

This project is ideal for anyone looking to learn about:
- User authentication and session management
- Integrating LLMs into practical applications
- Dynamic content generation and storage
- Creating educational tools using AI

### Features

User Authentication: Secure signup and login system with session management.

Custom Quiz Generation: Users can specify:
  - Topics
  - Difficulty level
  - Number of questions

**AI-Powered Question Generation:** Uses Gemini LLM to generate high-quality MCQs dynamically.
**Database Integration:** Saves generated quizzes and retrieves them based on user session IDs.
**Interactive Practice:** Users can practice generated quizzes directly within the platform.


## How It Works

1. Sign Up / Login: Users create an account and log in.
2. Quiz Configuration: Users choose topics, difficulty level, and number of questions.
3. AI Generation: The application sends the inputs to the Gemini LLM, which generates MCQs.
4. Save & Retrieve: Generated quizzes are saved to the database with a session ID.
5. Practice Quiz: Users access their quiz using the session ID and start practicing.



# API Routes Documentation
The following endpoints handle user authentication, session generation, and quiz access.

- GET `/auth/csrf_cookie/` - Retrieves and sets a CSRF token cookie required for secure form submissions and authenticated requests.

- POST `/auth/registration/` - Registers a new user account using the provided user details.
- POST `/auth/activate/` - Activates a newly registered user account using a verification token or code.
- POST `/auth/signin/` - Authenticates a user and creates a login session using their credentials.
- POST `/generate/` – Generates a new quiz session based on the provided parameters or topic.
- GET `/quiz-session/<sessionId>/` – Retrieves the details and current state of a specific quiz session.
- POST `/auth/logout/` – Logs out the authenticated user and invalidates the current session.

### 1. User Registration
**Endpoint**
POST `/auth/registration/`

**Description**
- Registers a new user account.

**Request Body Example**
```json
{
  "email": "user@example.com",
  "password": "your_password",
  "username": "your_username"
}
```

**Response**
- 201 Created – User registered successfully
- 400 Bad Request – Invalid input or user already exists

### 2. Account Activation

**Endpoint**
POST `/auth/activate/`

**Description**

- Activates a user account using the activation token sent via email after registration.

**Request Body Example**
```json
{
  "uid": "user_id",
  "token": "activation_token"
}
```
**Response**

- 200 OK – Account activated successfully
- 400 Bad Request – Invalid or expired token

### 3. Get CSRF Token

**Endpoint**
GET `/auth/csrf_cookie/`

**Description**

- Returns a CSRF token and sets it in cookies for secure authenticated requests.

**Response**

- 200 OK – CSRF cookie set successfully

**4. User Login**

**Endpoint**
POST `/auth/signin/`

Description
- Authenticates a user and creates a login session.

**Request Body Example**

```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```
**Response**
- 200 OK – Login successful
- 401 Unauthorized – Invalid credentials

### 5. User Logout
**Endpoint** POST `/auth/logout/`

**Description**
- Logs the user out and clears the session.

**Response**
- 200 OK – Logout successful

### 6. Generate Quiz Session

**Endpoint**
POST `/generate/`

**Description**

- Creates a new quiz session and returns a unique session ID.

**Response Example**
```json
{
  "sessionId": "abc123xyz"
}
```
**Response**
- 200 OK – Quiz session generated successfully

### 7. Access Quiz Session

**Endpoint**
GET `/quiz-session/{sessionId}/`

**Description**
- Retrieves quiz data associated with a specific session.

**Path Parameter**



