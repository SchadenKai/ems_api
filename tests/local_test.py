from pydantic import BaseModel, UUID1

class User(BaseModel):
    first_name : str
    last_name : str


externdal_data_sample = {
    "first_name" : "kairus",
    "last_name" : "tecson"
}

user = User(**externdal_data_sample)

print(user.model_dump())