from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, Field


Severity = Literal[
    "AUTO_RECOVERABLE",
    "NEED_OPERATOR_CONFIRMATION",
    "REQUIRE_STOPPAGE",
]


class PLCPoint(BaseModel):
    tag: str
    value: str
    ts: Optional[str] = None


class OperationRecord(BaseModel):
    ts: str
    action: str
    operator: str = "system"


class AlarmEvent(BaseModel):
    line_id: str
    station_id: str
    equipment_id: str
    timestamp: str
    alarm_code: str
    alarm_message: Optional[str] = None
    mode: str = "AUTO"
    plc_snapshot: List[PLCPoint] = Field(default_factory=list)
    recent_operations: List[OperationRecord] = Field(default_factory=list)
    process_context: Dict[str, str] = Field(default_factory=dict)


class RetrievedDoc(BaseModel):
    source: str
    title: str
    snippet: str
    score: float
    metadata: Dict[str, str] = Field(default_factory=dict)


class CandidateCause(BaseModel):
    title: str
    score: float
    evidence: List[str] = Field(default_factory=list)
    missing_checks: List[str] = Field(default_factory=list)


class RootCauseResult(BaseModel):
    alarm_code: str
    alarm_message: str
    top_cause: CandidateCause
    alternatives: List[CandidateCause] = Field(default_factory=list)
    evidence_docs: List[RetrievedDoc] = Field(default_factory=list)


class ActionPlan(BaseModel):
    severity: Severity
    rationale: str
    steps: List[str]
    escalation: str
    auto_reset_allowed: bool = False


class PostmortemReport(BaseModel):
    report_id: str
    summary: str
    timeline: List[str]
    root_cause: str
    evidence: List[str]
    actions_taken: List[str]
    preventive_actions: List[str]


class DiagnosisResponse(BaseModel):
    alarm_code: str
    alarm_message: str
    root_cause: Dict
    alternatives: List[Dict]
    severity: Severity
    recommended_actions: List[str]
    report_id: str
    retrieved_knowledge: List[Dict]
