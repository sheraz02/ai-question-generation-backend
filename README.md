# Django RAG Project

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

## Running tests

Run Django tests or the provided test file:

```bash
python manage.py test
# or
# pytest (if pytest is installed and configured)
```

## RAG Pipelines (quick notes)

The `RAGpipelines` folder contains scripts to process documents and build/retrieve embeddings and chunks:

- `pdf_chunker.py` - utilities to split PDFs into chunks.
- `characterSplitter.py` - low-level splitting utilities.
- `ingetion_pipeline.py` - (note: file name `ingetion_pipeline.py`) orchestrates ingestion of files into the vector DB.
- `retriever_pipeline.py` - retrieval helpers for querying the vector store.
- `questionGeneratorPipeline.py` - utilities to generate questions from content.
- `geminiPrompts.py` - prompt templates used by the project.

Data and DBs
- `RAGpipelines/chroma_db/chroma.sqlite3` contains Chromadb artifacts used by the pipelines.
- `RAGpipelines/pdf-files/` is the default location for source PDFs.

To run ingestion or retrieval scripts, inspect the corresponding files in the `RAGpipelines` folder and run them via Python. They may assume local credentials or environment variables for model access — check the script headers for required configuration.

## `user_profiles` app

The `user_profiles` app provides:

- registration and activation flows (activation email template at `user_profiles/templates/account/activation_email.html`).
- custom backends or auth integration (`user_profiles/backends.py`).
- API serializers and views for user-related operations.

Check [user_profiles/urls.py](user_profiles/urls.py) to see available endpoints and integrate them with the frontend or API client.

## Common commands

- Run migrations: `python manage.py migrate`
- Run server: `python manage.py runserver`
- Create superuser: `python manage.py createsuperuser`
- Install deps: `pip install -r requirements.txt`

## Contributing

1. Create an issue describing your change.
2. Open a pull request with focused commits and tests.

## Notes and caveats

- This README is based on the repository contents; run and test locally before deploying to production.
- The RAG pipeline scripts may require external API keys or model credentials; don't commit secrets.

---

If you want, I can:

- add specific API endpoint documentation extracted from `user_profiles/urls.py` and view docstrings,
- run the test suite and fix any failing issues,
- or generate example curl requests for the main endpoints.

Tell me which follow-up you'd like next.
