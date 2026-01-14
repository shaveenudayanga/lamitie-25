from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.schemas.venue import VenueCreate, VenueUpdate, Venue as VenueResponse
from src.services.venue_service import VenueService

router = APIRouter()

@router.post("/", response_model=VenueResponse)
def create_venue(venue: VenueCreate, db: Session = Depends(get_db)):
    try:
        service = VenueService(db)
        return service.create_venue(venue)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{venue_id}", response_model=VenueResponse)
def read_venue(venue_id: int, db: Session = Depends(get_db)):
    service = VenueService(db)
    venue = service.get_venue(venue_id)
    if venue is None:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue

@router.put("/{venue_id}", response_model=VenueResponse)
def update_venue(venue_id: int, venue: VenueUpdate, db: Session = Depends(get_db)):
    try:
        service = VenueService(db)
        updated_venue = service.update_venue(venue_id, venue)
        if updated_venue is None:
            raise HTTPException(status_code=404, detail="Venue not found")
        return updated_venue
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{venue_id}", response_model=dict)
def delete_venue(venue_id: int, db: Session = Depends(get_db)):
    try:
        service = VenueService(db)
        result = service.delete_venue(venue_id)
        if not result:
            raise HTTPException(status_code=404, detail="Venue not found")
        return {"detail": "Venue deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))