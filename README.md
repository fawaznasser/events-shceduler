# Event Scheduler Backend

A FastAPI backend service that integrates with the Ticketmaster public API to collect events, store them locally, and allow authenticated users to save and retrieve personal favorite events.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup & Run Instructions](#setup--run-instructions)
- [Docker Compose Usage](#docker-compose-usage)
- [Authentication Provider Setup](#authentication-provider-setup)
- [API Usage Guide](#api-usage-guide)
- [Design & Architecture](#design--architecture)
- [Event Fetching Strategy](#event-fetching-strategy)
- [Testing](#testing)
- [Technology Choices & Justification](#technology-choices--justification)
- [Security Note](#security-note)
- [License](#license)
- [Contact](#contact)

---

## Features

- **User Authentication**: Secure login using Google OAuth (or Auth0).
- **Personal Event Lists**: Authenticated users can save and retrieve their favorite events.
- **Public Event Browsing**: Anyone can browse public events.
- **Hybrid Event Fetching**: Events are cached locally for fast access and periodically refreshed from Ticketmaster.
- **RESTful API**: Clean, self-explanatory endpoints.
- **Dockerized**: Easy to run with Docker Compose.
- **Logging**: Key actions and errors are logged for observability.

---

## Requirements

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL database (managed by Docker)
- Ticketmaster API Key
- Google OAuth or Auth0 credentials

---

## Setup & Run Instructions

### 1. **Clone the Repository**

```sh
git clone https://github.com/yourusername/events-scheduler.git
cd events-scheduler
```

### 2. **Create a `.env` File in the Project Root**

```
SECRET_KEY=your_secret_key
TICKETMASTER_API_KEY=your_ticketmaster_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

> **Never commit your `.env` file! It is already in `.gitignore`.**

### 3. **Build and Start the Project with Docker Compose**

Make sure Docker Desktop is running, then:

```sh
docker-compose up --build
```

### 4. **Access the API**

Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser for the Swagger UI.

---

## Docker Compose Usage

- **Start services:**  
  ```sh
  docker-compose up --build
  ```
- **Stop services:**  
  Press `Ctrl+C` in the terminal, then run:
  ```sh
  docker-compose down
  ```
- **Rebuild after code changes:**  
  ```sh
  docker-compose up --build
  ```

---

## Authentication Provider Setup

### **Google OAuth**

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create OAuth 2.0 credentials.
3. Set the redirect URI to `http://localhost:8000/auth/callback`.
4. Add your `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` to your `.env` file.

### **Auth0 (Alternative)**

1. Create an Auth0 application.
2. Set callback URLs and add credentials to `.env`.

---

## API Usage Guide

### **Endpoints**

| Method | Path                    | Description                                 |
|--------|-------------------------|---------------------------------------------|
| GET    | `/events/`              | List public events (paginated, filterable)  |
| POST   | `/events/{event_id}/save` | Save an event to the user's list           |
| GET    | `/my/events/`           | Retrieve the user's saved events            |

### **Example: Fetch Events**

```sh
curl "http://localhost:8000/events?page=1&size=10"
```

### **Example: Save Event (Authenticated)**

- Log in via Swagger UI or your frontend to get a session.
- Use `/events/{event_id}/save` with a valid event ID.

---

## Design & Architecture

- **FastAPI** for async, modern API development.
- **SQLAlchemy** for ORM and database access.
- **Hybrid event fetching**: Cached events are served if fresh; otherwise, new data is fetched from Ticketmaster.
- **Separation of concerns**: Models, API routes, and authentication are modular.
- **Logging**: All major actions and errors are logged.

---

## Event Fetching Strategy

- **Hybrid strategy**:  
  - Events are cached locally for 1 hour.
  - If the cache is fresh, events are served from the local database for speed and reliability.
  - If the cache is stale or a manual refresh is requested, events are fetched from Ticketmaster and the cache is updated.
- **Justification**:  
  - This balances performance, API rate limits, and data freshness.

---

## Testing

- Unit tests are located in the `tests/` directory.
- To run tests:
  ```sh
  pytest
  ```
- Focus is on data access and business logic.

---

## Technology Choices & Justification

- **FastAPI**: Modern, async Python web framework.
- **PostgreSQL**: Reliable relational database.
- **Docker Compose**: Simplifies deployment and local development.
- **httpx**: Async HTTP client for external API calls.
- **SQLAlchemy**: ORM for database access.
- **pytest**: Testing framework.
- **Authlib**: Secure OAuth integration.

---

## Security Note

**Never commit your `.env` file or secrets to version control.**  
Your `.env` is in `.gitignore` by default.

---
