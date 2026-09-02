"""Round-trip tests for the repository-neutral ARGUS wire contracts."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
import sys
from uuid import UUID

CONTRACTS_PYTHON = Path(__file__).parents[1] / "python"
sys.path.insert(0, str(CONTRACTS_PYTHON))

from argus_contracts import DecisionEvent, ErrorEnvelope, IngestAcceptedResponse


def test_ingest_accepted_response_round_trips_uuid_and_datetime() -> None:
    """Changing a wire UUID or timestamp to a Python object must fail this test."""
    response = IngestAcceptedResponse(
        ingestion_id=UUID("11111111-1111-1111-1111-111111111111"),
        status="queued",
        queued_at=datetime(2026, 9, 2, 15, 30, tzinfo=UTC),
    )

    wire = response.model_dump(mode="json")

    assert wire == {
        "ingestion_id": "11111111-1111-1111-1111-111111111111",
        "status": "queued",
        "queued_at": "2026-09-02T15:30:00Z",
    }
    assert IngestAcceptedResponse.model_validate(wire) == response


def test_decision_event_round_trips_a_typed_envelope() -> None:
    """Accepting unknown events or losing envelope UUID/date encoding must fail."""
    event = DecisionEvent(
        type="decision.resolved",
        tenant_id=UUID("22222222-2222-2222-2222-222222222222"),
        timestamp=datetime(2026, 9, 2, 15, 35, tzinfo=UTC),
        payload={
            "decision_id": "33333333-3333-3333-3333-333333333333",
            "state": "resolved_false_positive",
            "resolved_by": "auth0|watcher123",
            "resolved_at": "2026-09-02T15:35:00Z",
        },
    )

    wire = event.model_dump(mode="json")

    assert wire["type"] == "decision.resolved"
    assert wire["tenant_id"] == "22222222-2222-2222-2222-222222222222"
    assert wire["timestamp"] == "2026-09-02T15:35:00Z"
    assert DecisionEvent.model_validate(wire) == event


def test_error_envelope_validates_the_production_validation_error_shape() -> None:
    """The independent contract package must not depend on the Core repository."""
    error = ErrorEnvelope.model_validate(
        {
            "error": {
                "code": "validation_error",
                "message": "Request validation failed",
                "status": 422,
                "details": [
                    {
                        "type": "int_parsing",
                        "loc": ["query", "quantity"],
                        "msg": "Input should be a valid integer",
                        "input": "invalid",
                    }
                ],
            }
        }
    )

    wire = error.model_dump(mode="json")

    assert wire == {
        "error": {
            "code": "validation_error",
            "message": "Request validation failed",
            "status": 422,
            "details": [
                {
                    "type": "int_parsing",
                    "loc": ["query", "quantity"],
                    "msg": "Input should be a valid integer",
                    "input": "invalid",
                }
            ],
        }
    }
    assert ErrorEnvelope.model_validate(wire) == error
