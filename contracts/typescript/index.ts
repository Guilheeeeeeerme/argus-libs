/** Repository-neutral ARGUS wire contracts. */

/** UUID and RFC 3339 date-time values are serialized as strings on the wire. */
export interface IngestAcceptedResponse {
  ingestion_id: string;
  status: "queued" | "duplicate";
  queued_at: string;
}

export type DecisionEventType =
  | "decision.state_changed"
  | "decision.evidence_added"
  | "decision.resolved";

export interface DecisionEvent {
  type: DecisionEventType;
  tenant_id: string;
  timestamp: string;
  payload: Record<string, unknown>;
}

export interface ErrorDetail {
  code: string;
  message: string;
  status: number;
  details?: unknown;
}

export interface ErrorEnvelope {
  error: ErrorDetail;
}
