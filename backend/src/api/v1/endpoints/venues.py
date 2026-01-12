from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.models.venue import Venue
from src.schemas.venue import VenueCreate, VenueUpdate
from src.services.venue_service import VenueService

router = APIRouter()
venue_service = VenueService()

@router.post("/", response_model=Venue)
async def create_venue(venue: VenueCreate, db: Session = Depends(get_db)):
    try:
        return await venue_service.create_venue(venue, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{venue_id}", response_model=Venue)
async def read_venue(venue_id: int, db: Session = Depends(get_db)):
    venue = await venue_service.get_venue(venue_id, db)
    if venue is None:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue

@router.put("/{venue_id}", response_model=Venue)
async def update_venue(venue_id: int, venue: VenueUpdate, db: Session = Depends(get_db)):
    try:
        updated_venue = await venue_service.update_venue(venue_id, venue, db)
        if updated_venue is None:
            raise HTTPException(status_code=404, detail="Venue not found")
        return updated_venue
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{venue_id}", response_model=dict)
async def delete_venue(venue_id: int, db: Session = Depends(get_db)):
    try:
        result = await venue_service.delete_venue(venue_id, db)
        if not result:
            raise HTTPException(status_code=404, detail="Venue not found")
        return {"detail": "Venue deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))