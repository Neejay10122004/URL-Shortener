URL Shortener – FastAPI + Streamlit

This project is a simple full-stack URL Shortener application built using FastAPI for the backend, Streamlit for the frontend, and SQLite as the persistent database.
Users can shorten long URLs, open the short URLs to trigger redirection, and view statistics such as total click count and creation time.

1. Project Structure
url_short/
│
├── app/                    # Backend (FastAPI)
│   ├── main.py             # API routes and core logic
│   ├── models.py           # SQLAlchemy models
│   ├── database.py         # Database setup (SQLite)
│   ├── utils.py            # Utility functions (short code generator)
│   └── __init__.py
│
├── frontend/               # Frontend (Streamlit)
│   └── app.py              # UI implementation
│
├── requirements.txt        # Dependencies
└── shortener.db            # SQLite database (auto created)

2. How to Run the Project
This project requires Python 3.9 or later.

Step 1: Install dependencies

Open a terminal inside the project folder and run:

pip install -r requirements.txt

Step 2: Start the FastAPI backend

Navigate to the project root and run:

uvicorn app.main:app --reload


FastAPI will start at:

http://localhost:8000

Step 3: Start the Streamlit frontend

Open a new terminal and run:

streamlit run frontend/app.py


Streamlit will start at:

http://localhost:8501

Step 4: Use the application

Open the Streamlit URL

Enter a long URL

Receive a short URL

Click the short URL to test redirect

View statistics in the Stats tab

3. How the Application Works

The application follows a simple client-server architecture.

Frontend (Streamlit)

User enters a long URL.

Streamlit sends the input to FastAPI through a POST request.

Streamlit displays the short URL returned by the backend.

Users can also enter a short code to retrieve its statistics.

Backend (FastAPI)

Validates the input using Pydantic.

Generates a unique short code or accepts a custom alias.

Saves the long URL, short code, timestamps, and click count in SQLite using SQLAlchemy.

When a user visits /<short_code>:

The backend retrieves the corresponding long URL.

Increments the click counter.

Redirects the user to the original page.

Exposes an API route to return statistics for any short URL.

Database (SQLite + SQLAlchemy)

A single URL table stores long URLs, short codes, creation time, expiry time, and click count.

SQLAlchemy ORM is used for querying and updating the database.

4. Core Functionalities Implemented
1. Create Short URL

Users can submit any valid URL and optionally provide:

Expiry time (in minutes)

Custom alias for the short URL

FastAPI generates or verifies the short code and stores it in the database.

2. Redirect on Short URL Access

Visiting a short URL such as:

http://localhost:8000/abc123


Triggers:

Database lookup

Click count increment

Immediate redirect to the original long URL

3. Persistent URL Storage

All data is stored in shortener.db, meaning URLs remain functional even after restarting the server.

4. Click Tracking

Each time a short URL is visited, the click counter in the database increases.

5. Statistics Endpoint

Users can retrieve:

Long URL

Short code

Creation time

Expiry time

Total clicks

from a dedicated API route and through the Streamlit UI.

6. Validation and Error Handling

The frontend checks if the URL begins with http:// or https://.

The backend uses Pydantic HttpUrl type to ensure strict validation.

Custom error messages are displayed in the UI.

5. Design Decisions
FastAPI as Backend

FastAPI provides:

Built-in validation through Pydantic

Very high performance

Clean and simple route definitions
This makes it ideal for a REST API–based project.

Streamlit as Frontend

Streamlit was chosen because:

It allows building a UI quickly using only Python

It eliminates the need for HTML, CSS, or JavaScript

Interaction with backend APIs is simple using the requests library

SQLite Database with SQLAlchemy

SQLite was selected for:

Light-weight and file-based storage

Zero configuration
SQLAlchemy simplifies work by allowing ORM models instead of raw SQL queries.

Separation of Frontend and Backend

Using Streamlit (port 8501) and FastAPI (port 8000) allows:

Clear separation of concerns

Independent deployment of frontend and backend

Easy testing and debugging

Clean Error Handling

To improve the user experience:

Frontend performs basic validation

Backend returns structured error messages

Streamlit displays readable alerts instead of raw JSON
