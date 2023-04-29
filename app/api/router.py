from fastapi import APIRouter

from api.routes.profiles import router as profiles_router

router = APIRouter()


router.include_router(profiles_router, tags=["Profiles"], prefix="/profiles")
