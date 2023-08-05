from __future__ import annotations
from typing import List
from pydantic import BaseModel
from enum import Enum
import datetime

class triageColour(Enum):
    red = 1
    yellow = 2
    green = 3
    purple = 4

class vitals(BaseModel):
    heartRate: int
    oxygenSaturation: int
    diastolicBloodPressure: int
    systolicBloodPressure: int
    respiratoryRate: int
    temperature: int
    heartRateVariability: int
    GCS: int
    glucose: int
    treatment: str
    triageColour: triageColour
    date: datetime.datetime

class Model(BaseModel):
    victimID: str
    vitals: List[vitals]