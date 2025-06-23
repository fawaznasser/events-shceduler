import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()  # Load environment variables from .env

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    saved_events = relationship("SavedEvent", back_populates="user")

class SavedEvent(Base):
    __tablename__ = "saved_events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(String)
    name = Column(String)
    date = Column(String)
    time = Column(String)
    venue = Column(String)
    city = Column(String)
    url = Column(String)
    user = relationship("User", back_populates="saved_events")

class CachedEvent(Base):
    __tablename__ = "cached_events"
    id = Column(String, primary_key=True, index=True)  # Ticketmaster event ID
    name = Column(String)
    date = Column(String)
    time = Column(String)
    venue = Column(String)
    city = Column(String)
    url = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow)

# Create tables in the database 
Base.metadata.create_all(bind=engine)