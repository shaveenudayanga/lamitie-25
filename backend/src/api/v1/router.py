from fastapi import APIRouter
from .endpoints import events, users, registrations, venues, auth

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(events.router, prefix="/events", tags=["events"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(registrations.router, prefix="/registrations", tags=["registrations"])
router.include_router(venues.router, prefix="/venues", tags=["venues"])