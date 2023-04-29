from uuid import uuid4, UUID
from typing import List

from sqlmodel import SQLModel, Field, Column, JSON
from datetime import date


class ProfileBase(SQLModel):
    username: str = Field(default=None, nullable=True)
    mail: str = Field(default=None, nullable=True)
    name: str = Field(default=None, nullable=True)
    ssn: str = Field(default=None, nullable=True)
    sex: str = Field(default=None, nullable=True)
    birthdate: date = Field(default=None, nullable=True)
    blood_group: str = Field(default=None, nullable=True)
    address: str = Field(default=None, nullable=True)
    residence: str = Field(default=None, nullable=True)
    website: List[str] = Field(default=None, nullable=True, sa_column=Column(JSON))
    current_location: List[str] = Field(default=None, nullable=True, sa_column=Column(JSON))
    job: str = Field(default=None, nullable=True)
    company: str = Field(default=None, nullable=True)


class Profile(ProfileBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False,)

    __tablename__ = "profiles"
