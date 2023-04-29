from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status

from api.dependencies.repositories import get_repository
from db.errors import EntityDoesNotExist
from db.repositories.profiles import ProfileRepository
from schemas.profiles import ProfileCreate, ProfilePatch, ProfileRead

router = APIRouter()


@router.post(
    "/profiles",
    response_model=ProfileRead,
    status_code=status.HTTP_201_CREATED,
    name="create_profile",
)
async def create_profile(
    profile_create: ProfileCreate = Body(...),
    repository: ProfileRepository = Depends(get_repository(ProfileRepository)),
) -> ProfileRead:
    return await repository.create(profile_create=profile_create)


@router.get(
    "/profiles",
    response_model=list[Optional[ProfileRead]],
    status_code=status.HTTP_200_OK,
    name="get_profiles",
)
async def get_profiles(
    limit: int = Query(default=10, lte=100),
    offset: int = Query(default=0),
    repository: ProfileRepository = Depends(get_repository(ProfileRepository)),
) -> list[Optional[ProfileRead]]:
    return await repository.list(limit=limit, offset=offset)


@router.get(
    "/profiles/{profile_id}",
    response_model=ProfileRead,
    status_code=status.HTTP_200_OK,
    name="get_profile",
)
async def get_profile(
    profile_id: UUID,
    repository: ProfileRepository = Depends(get_repository(ProfileRepository)),
) -> ProfileRead:
    try:
        await repository.get(profile_id=profile_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found!"
        )

    return await repository.get(profile_id=profile_id)


@router.delete(
    "/profiles/{profile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="delete_profile",
)
async def delete_profile(
    profile_id: UUID,
    repository: ProfileRepository = Depends(get_repository(ProfileRepository)),
) -> None:
    try:
        await repository.get(profile_id=profile_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found!"
        )

    return await repository.delete(profile_id=profile_id)


@router.put(
    "/profiles/{profile_id}",
    response_model=ProfileRead,
    status_code=status.HTTP_200_OK,
    name="delete_profile",
)
async def update_profile(
    profile_id: UUID,
    profile_patch: ProfilePatch = Body(...),
    repository: ProfileRepository = Depends(get_repository(ProfileRepository)),
) -> ProfileRead:
    try:
        await repository.get(profile_id=profile_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found!"
        )

    return await repository.patch(
        profile_id=profile_id, profile_patch=profile_patch
    )