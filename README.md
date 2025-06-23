# Event Scheduler Backend

A FastAPI backend service that integrates with the Ticketmaster public API to collect events, store them locally, and allow authenticated users to save and retrieve personal favorite events.

---

## Features

- **User Authentication**: Only authenticated users (via Google OAuth or Auth0) can save and view their favorite events.
- **Public Event Browsing**: Unauthenticated users can browse public events.
- **Hybrid Event Fetching**: Events are cached locally for 1 hour for fast access; fresh data is fetched from Ticketmaster as needed.
- **RESTful API**: Clean, self-explanatory endpoints.
- **Dockerized**: Easy to run with Docker Compose.
- **Logging**: Key actions and errors are logged for observability.

---

## Table of Contents

- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Running with Docker Compose](#running-with-docker-compose)
- [Authentication Provider Setup](#authentication-provider-setup)
- [API Usage Guide](#api-usage-guide)
- [Design & Architecture](#design--architecture)
- [Event Fetching Strategy](#event-fetching-strategy)
- [Testing](#testing)
- [Technology Choices](#technology-choices)

---

## Requirements

- Python 3.11+
- Docker & Docker Compose (recommended)
- PostgreSQL database
- Ticketmaster API Key
- Google OAuth or Auth0 credentials

---

## Setup Instructions

1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/events-scheduler.git
   cd events-scheduler
   ```

2. **Create a `.env` File in the Project Root**
   ```
   DATABASE_URL=postgresql://postgres:postgres@db:5432/eventsdb
   TICKETMASTER_API_KEY=your_ticketmaster_api_key
   SECRET_KEY=your_fastapi_secret_key
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   ```

3. **(Optional) Install Python Dependencies Locally**
   ```sh
   pip install -r requirements.txt
   ```

---

## Running with Docker Compose

1. **Build and Start the Services**
   ```sh
   docker-compose up --build
   ```

2. **Access the API**
   - Open [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

---

## Authentication Provider Setup

- **Google OAuth**:  
  - Go to [Google Cloud Console](https://console.cloud.google.com/).
  - Create OAuth 2.0 credentials.
  - Set the redirect URI to `http://localhost:8000/auth/callback`.
  - Add your `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` to `.env`.

- **Auth0** (alternative):  
  - Create an Auth0 application.
  - Set callback URLs and add credentials to `.env`.

---

## API Usage Guide

### **Public Endpoints**

- `GET /events`
  - List public events (supports pagination and filtering).
  - Query params: `page`, `size`, `keyword`, `city`, `startDateTime`, `endDateTime`, `refresh`.

### **Authenticated Endpoints**

- `POST /events/{event_id}/save`
  - Save an event to your personal list (must be logged in).

- `GET /my/events`
  - Retrieve your saved events.

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

We use a **hybrid strategy**:
- Events are cached locally for 1 hour.
- If the cache is fresh, events are served from the local database for speed and reliability.
- If the cache is stale or a manual refresh is requested, events are fetched from Ticketmaster and the cache is updated.
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

## Technology Choices

- **FastAPI**: Modern, async Python web framework.
- **PostgreSQL**: Reliable relational database.
- **Docker Compose**: Simplifies deployment and local development.
- **httpx**: Async HTTP client for external API calls.
- **SQLAlchemy**: ORM for database access.
- **pytest**: Testing framework.

---





