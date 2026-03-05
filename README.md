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


### 1. Get CSRF Token

**Endpoint**
GET `/auth/csrf_cookie/`

**Description**

- Returns a CSRF token and sets it in cookies for secure authenticated requests.

**Response**

- 200 OK – CSRF cookie set successfully


### 2. User Registration
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

### 3. Account Activation

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



### 4. User Login

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

### 5. Generate Quiz Session

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


### 6. Access Quiz Session

**Endpoint**
GET `/quiz-session/{sessionId}/`

**Description**
- Retrieves quiz data associated with a specific session.

**Path Parameter**

### 7. User Logout
**Endpoint** POST `/auth/logout/`

**Description**
- Logs the user out and clears the session.

**Response**
- 200 OK – Logout successful






