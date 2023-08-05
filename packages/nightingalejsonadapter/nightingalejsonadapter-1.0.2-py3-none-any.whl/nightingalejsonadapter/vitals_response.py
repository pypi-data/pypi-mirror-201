from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel
from datetime import datetime
from uuid_generator import UUIDGenerator


class VitalPredictions(BaseModel):
    HR: float
    RR: float
    SBP: float
    DBP: float
    SPO2: float


class VitalEarlyWarningScore(BaseModel):
    HR: int
    RR: int
    SBP: int
    DBP: int
    SPO2: int


class ShockIndex(BaseModel):
    Value: float
    EarlyWarningScore: int


class ProcedureMessage(BaseModel):
    PredictedInterventionTimestamp: Optional[datetime.datetime] = None
    Message: Optional[str] = None


class ProcedureMessagesABC(BaseModel):
    a: ProcedureMessage
    b: ProcedureMessage
    c: ProcedureMessage


class Prediction(BaseModel):
    Timestamp: str
    VitalPredictions: VitalPredictions
    VitalEarlyWarningScore: VitalEarlyWarningScore
    ShockIndex: ShockIndex
    ProcedureMessagesABC: ProcedureMessagesABC


class Model(BaseModel):
    UUID: str
    LastMeasurementTimestamp: str
    PredictionTimestampId: str
    PredictionTimeDeltaMinutes: int
    PatientId: str
    ProcedureMessageCount: int
    Predictions: List[Prediction]