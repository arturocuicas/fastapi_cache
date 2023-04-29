from uuid import UUID

from db.tables.profiles import ProfileBase


class ProfileCreate(ProfileBase):
    ...


class ProfileRead(ProfileBase):
    id: UUID


class ProfilePatch(ProfileBase):
    ...
