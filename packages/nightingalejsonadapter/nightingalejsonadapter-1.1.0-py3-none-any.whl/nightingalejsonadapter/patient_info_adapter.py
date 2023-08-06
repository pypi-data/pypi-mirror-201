from __future__ import annotations

from pydantic import BaseModel


class DateObserved(BaseModel):
    type: str
    value: str


class Payload(BaseModel):
    name: str
    surname: str
    sex: str
    dob: str
    age: int
    nationality: str
    job: str
    injury: str
    transport: int
    destination: str
    service: str
    vector: str
    color: str
    identifier: str
    device: str
    incident: str
    latitude: int
    longitude: int


class Model(BaseModel):
    id: str
    type: str
    dateObserved: DateObserved
    payload: Payload
