from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from .database import Base, engine, SessionLocal
from .models import URL
from .utils import generate_short_code 

Base.metadata.create_all(bind=engine)
app = FastAPI(title="URL Shortener API")

BASE_URL = "http://localhost:8000"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ShortenRequest(BaseModel):
    long_url: HttpUrl
    expires_in_seconds: Optional[int] = None  
    custom_alias: Optional[str] = None        


class ShortenResponse(BaseModel):
    short_code: str
    short_url: str


@app.get("/")
def root():
    return {"message": "URL Shortener API is running"}


@app.post("/api/shorten", response_model=ShortenResponse)
def shorten_url(payload: ShortenRequest, db: Session = Depends(get_db)):
    if payload.custom_alias:
        existing = db.query(URL).filter(URL.short_code == payload.custom_alias).first()
        if existing:
            raise HTTPException(status_code=400, detail="Custom alias already in use")
        short_code = payload.custom_alias
    else:
        short_code = generate_short_code(db)

    expires_at = None
    if payload.expires_in_seconds:
        expires_at = datetime.utcnow() + timedelta(seconds=payload.expires_in_seconds)

    url_entry = URL(
        long_url=str(payload.long_url),
        short_code=short_code,
        expires_at=expires_at,
    )
    db.add(url_entry)
    db.commit()
    db.refresh(url_entry)

    return ShortenResponse(
        short_code=short_code,
        short_url=f"{BASE_URL}/{short_code}",
    )



@app.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")

    if url_entry.expires_at and url_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Short URL has expired")

    url_entry.clicks += 1
    db.commit()

    return RedirectResponse(url=url_entry.long_url, status_code=307)


class StatsResponse(BaseModel):
    long_url: str
    short_code: str
    clicks: int
    created_at: datetime
    expires_at: Optional[datetime]


@app.get("/api/stats/{short_code}", response_model=StatsResponse)
def stats(short_code: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return StatsResponse(
        long_url=url_entry.long_url,
        short_code=url_entry.short_code,
        clicks=url_entry.clicks,
        created_at=url_entry.created_at,
        expires_at=url_entry.expires_at,
    )
