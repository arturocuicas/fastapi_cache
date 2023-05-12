import pickle
from random import shuffle
from typing import Dict, Optional
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status

from api.dependencies.redis import cache
from api.dependencies.repositories import get_repository
from db.errors import EntityDoesNotExist
from db.repositories.profiles import ProfileRepository
from schemas.profiles import ProfileCreate, ProfilePatch, ProfileRead

router = APIRouter()


@router.get(
    "/get_size",
    status_code=status.HTTP_200_OK,
    name="get_size",
)
async def get_size(
    limit: int = Query(default=1000000, lte=1000000),
    offset: int = Query(default=0),
    repository: ProfileRepository = Depends(get_repository(ProfileRepository)),
) -> Dict:
    profiles_list = await repository.list(limit=limit, offset=offset)

    return {"Size": len(profiles_list)}


@router.get(
    "/get_random_profile",
    status_code=status.HTTP_200_OK,
    name="get_random_profile",
)
async def get_random_profile(
    limit: int = Query(default=1000000, lte=1000000),
    offset: int = Query(default=0),
    repository: ProfileRepository = Depends(get_repository(ProfileRepository)),
) -> Dict:
    profiles_list = await repository.list(limit=limit, offset=offset)
    shuffle(profiles_list)

    return {"Profile ID": f"{profiles_list[0].id}"}


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
    redis_client: cache = Depends(cache),
    repository: ProfileRepository = Depends(get_repository(ProfileRepository)),
) -> ProfileRead:
    if (cached_profile := redis_client.get(f"profile_{profile_id}")) is not None:
        return pickle.loads(cached_profile)

    try:
        profile = await repository.get(profile_id=profile_id)
        redis_client.set(f"profile_{profile_id}", pickle.dumps(profile))

        return profile

    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found!"
        )


@router.delete(
    "/profiles/{profile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="delete_profile",
)
async def delete_profile(
    profile_id: UUID,
    redis_client: cache = Depends(cache),
    repository: ProfileRepository = Depends(get_repository(ProfileRepository)),
) -> None:
    try:
        await repository.delete(profile_id=profile_id)
        redis_client.delete(f"profile_{profile_id}")

    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found!"
        )


@router.put(
    "/profiles/{profile_id}",
    response_model=ProfileRead,
    status_code=status.HTTP_200_OK,
    name="delete_profile",
)
async def update_profile(
    profile_id: UUID,
    redis_client: cache = Depends(cache),
    profile_patch: ProfilePatch = Body(...),
    repository: ProfileRepository = Depends(get_repository(ProfileRepository)),
) -> ProfileRead:
    try:
        updated_profile = await repository.patch(
            profile_id=profile_id, profile_patch=profile_patch
        )
        redis_client.delete(f"profile_{profile_id}")

        return updated_profile

    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found!"
        )
