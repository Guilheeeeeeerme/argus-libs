"""Repository-neutral ARGUS wire models.

These models intentionally contain no persistence, authentication, or service
client behavior.  They define only data crossing repository boundaries.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ContractModel(BaseModel):
    """Reject unknown fields so producers and consumers notice contract drift."""

    model_config = ConfigDict(extra="forbid")


class IngestAcceptedResponse(ContractModel):
    """Response returned when an ingestion request is accepted or deduplicated."""

    ingestion_id: UUID
    status: Literal["queued", "duplicate"]
    queued_at: datetime


class DecisionEvent(ContractModel):
    """WebSocket/broker envelope for a decision lifecycle event."""

    type: Literal[
        "decision.state_changed",
        "decision.evidence_added",
        "decision.resolved",
    ]
    tenant_id: UUID
    timestamp: datetime
    payload: dict[str, Any]


class ErrorDetail(ContractModel):
    """Structured error information returned inside a public API envelope."""

    code: str
    message: str
    status: int
    details: Any | None = None


class ErrorEnvelope(ContractModel):
    """Public error response shared by API consumers."""

    error: ErrorDetail
