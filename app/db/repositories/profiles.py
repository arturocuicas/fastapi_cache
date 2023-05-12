from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.errors import EntityDoesNotExist
from db.tables.profiles import Profile
from schemas.profiles import ProfileCreate, ProfilePatch, ProfileRead


class ProfileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get_instance(self, profile_id: UUID):
        statement = select(Profile).where(Profile.id == profile_id)
        results = await self.session.exec(statement)

        return results.first()

    async def create(self, profile_create: ProfileCreate) -> ProfileRead:
        db_profile = Profile.from_orm(profile_create)
        self.session.add(db_profile)
        await self.session.commit()
        await self.session.refresh(db_profile)

        return ProfileRead(**db_profile.dict())

    async def list(self, limit: int = 10, offset: int = 0) -> list[ProfileRead]:
        statement = select(Profile).offset(offset).limit(limit)
        results = await self.session.exec(statement)

        return [ProfileRead(**profile.dict()) for profile in results]

    async def get(self, profile_id: UUID) -> Optional[ProfileRead]:
        db_profile = await self._get_instance(profile_id)

        if db_profile is None:
            raise EntityDoesNotExist

        return ProfileRead(**db_profile.dict())

    async def patch(
        self, profile_id: UUID, profile_patch: ProfilePatch
    ) -> Optional[ProfileRead]:
        db_profile = await self._get_instance(profile_id)

        if db_profile is None:
            raise EntityDoesNotExist

        profile_data = profile_patch.dict(exclude_unset=True, exclude={"id"})
        for key, value in profile_data.items():
            setattr(db_profile, key, value)

        self.session.add(db_profile)
        await self.session.commit()
        await self.session.refresh(db_profile)

        return ProfileRead(**db_profile.dict())

    async def delete(self, profile_id: UUID) -> None:
        db_profile = await self._get_instance(profile_id)

        if db_profile is None:
            raise EntityDoesNotExist

        await self.session.delete(db_profile)
        await self.session.commit()
