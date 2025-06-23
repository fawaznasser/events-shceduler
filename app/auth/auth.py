from fastapi import Depends, Request, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app.models import User, get_db
from app.auth.oauth import oauth  # <-- Import here

router = APIRouter()

@router.get("/auth")
async def auth(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    userinfo = token.get('userinfo')
    email = userinfo["email"]

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email)
        db.add(user)
        db.commit()
        db.refresh(user)

    # Store email in session
    request.session["user_email"] = email

    return {"message": "Logged in", "user": user.email}

def get_current_user(request: Request, db: Session = Depends(get_db)):
    email = request.session.get("user_email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return user