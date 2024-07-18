from .schemas import UsersBase, PetsBase
from sqlmodel import Field, Relationship

class Users(UsersBase, table=True):
    id : int | None = Field(default=None, primary_key=True)
    pets : list[PetsBase] = Relationship(back_populates="owner")

class Pets(PetsBase, table=True):
    pet_id : int | None = Field(default=None, primary_key=True)
    owner_id : int = Field(foreign_key="users.id")
    owner : UsersBase = Relationship(back_populates="pets")