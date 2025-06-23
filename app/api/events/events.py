import os
import httpx
import logging
from fastapi import APIRouter, Query, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import SavedEvent, CachedEvent, get_db
from app.auth.auth import get_current_user

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/events")
async def get_events(
    keyword: str = Query(None),
    city: str = Query(None),
    startDateTime: str = Query(None),
    endDateTime: str = Query(None),
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    size: int = Query(20, ge=1, le=100, description="Number of events per page"),
    refresh: bool = Query(False, description="Force refresh from Ticketmaster"),
    db: Session = Depends(get_db)
):
    logger.info(f"Fetching events: page={page}, size={size}, keyword={keyword}, city={city}, refresh={refresh}")
    cache_lifetime = timedelta(hours=1)
    now = datetime.utcnow()
    cached_events = db.query(CachedEvent).all()
    if not refresh and cached_events and all((now - e.last_updated) < cache_lifetime for e in cached_events):
        logger.info("Serving events from cache.")
        start = (page - 1) * size
        end = start + size
        paginated = cached_events[start:end]
        return {
            "page": page,
            "size": size,
            "events": [
                {
                    "id": e.id,
                    "name": e.name,
                    "date": e.date,
                    "time": e.time,
                    "venue": e.venue,
                    "city": e.city,
                    "url": e.url,
                } for e in paginated
            ]
        }
    # Otherwise, fetch from Ticketmaster
    logger.info("Fetching events from Ticketmaster API.")
    api_key = os.getenv("TICKETMASTER_API_KEY")
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {"apikey": api_key, "page": page - 1, "size": size}
    if keyword:
        params["keyword"] = keyword
    if city:
        params["city"] = city
    if startDateTime:
        params["startDateTime"] = startDateTime
    if endDateTime:
        params["endDateTime"] = endDateTime

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            logger.error(f"Failed to fetch events from Ticketmaster: {response.status_code}")
            raise HTTPException(status_code=500, detail="Failed to fetch events")
        data = response.json()

        # Extract and cache relevant fields
        events = []
        db.query(CachedEvent).delete()  # Clear old cache
        for event in data.get('_embedded', {}).get('events', []):
            event_obj = CachedEvent(
                id=event.get("id"),
                name=event.get("name"),
                date=event.get("dates", {}).get("start", {}).get("localDate"),
                time=event.get("dates", {}).get("start", {}).get("localTime"),
                venue=event.get("_embedded", {}).get("venues", [{}])[0].get("name"),
                city=event.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name"),
                url=event.get("url"),
                last_updated=now
            )
            db.add(event_obj)
            events.append({
                "id": event_obj.id,
                "name": event_obj.name,
                "date": event_obj.date,
                "time": event_obj.time,
                "venue": event_obj.venue,
                "city": event_obj.city,
                "url": event_obj.url,
            })
        db.commit()
        logger.info(f"Fetched and cached {len(events)} events from Ticketmaster.")
        return {
            "page": page,
            "size": size,
            "events": events
        }

@router.post("/events/{event_id}/save")
async def save_event(
    event_id: str,
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    logger.info(f"User {user.id} is saving event {event_id}")
    api_key = os.getenv("TICKETMASTER_API_KEY")
    url = f"https://app.ticketmaster.com/discovery/v2/events/{event_id}.json"
    params = {"apikey": api_key}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            logger.warning(f"Event {event_id} not found on Ticketmaster.")
            raise HTTPException(status_code=404, detail="Event not found")
        event = response.json()

    name = event.get("name")
    date = event.get("dates", {}).get("start", {}).get("localDate")
    time = event.get("dates", {}).get("start", {}).get("localTime")
    venue = event.get("_embedded", {}).get("venues", [{}])[0].get("name")
    city = event.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name")
    url_ = event.get("url")

    saved_event = SavedEvent(
        user_id=user.id,
        event_id=event_id,
        name=name,
        date=date,
        time=time,
        venue=venue,
        city=city,
        url=url_
    )
    db.add(saved_event)
    db.commit()
    db.refresh(saved_event)
    logger.info(f"Event {event_id} saved for user {user.id}")
    return {"message": "Event saved!"}

@router.get("/my/events")
def my_events(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    logger.info(f"Fetching saved events for user {user.id}")
    events = db.query(SavedEvent).filter(SavedEvent.user_id == user.id).all()
    return [
        {
            "event_id": e.event_id,
            "name": e.name,
            "date": e.date,
            "time": e.time,
            "venue": e.venue,
            "city": e.city,
            "url": e.url,
        }
        for e in events
    ]