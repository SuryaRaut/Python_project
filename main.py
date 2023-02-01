from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Person(BaseModel):
    id: int
    name: str
    age: float
    is_student: Union[bool, None]


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/person/{id}")
async def get_student(person_id: int, q: Union[str, None] = None):
    return {"person id": person_id, 'q': q}


@app.put("/items/{item_id}")
def update_person(person_id: int, person: Person):
    return {"Person name": person.name, "person_id": person_id}
