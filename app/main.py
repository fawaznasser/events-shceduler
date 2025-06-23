import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from app.api.events.events import router as events_router
from app.auth import auth
from app.auth.oauth import oauth  # <-- Import here

load_dotenv()

app = FastAPI(
    title="Kedra API",
    description="Backend API for Ticketmaster event discovery with Google OAuth authentication.",
    version="1.0.0"
)
app.add_middleware(SessionMiddleware, secret_key="!secret")

app.include_router(events_router)
app.include_router(auth.router)

@app.get("/")
def homepage():
    return HTMLResponse('<a href="/login">Login with Google</a>')

@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)