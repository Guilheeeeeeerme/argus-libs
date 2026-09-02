# ARGUS shared contracts

`contracts/` is the staging tree for the future `argus-libs` repository. It
contains only versioned API and event wire contracts:

- `openapi/`: normalized OpenAPI 3.1 schemas for ingestion, errors, and
  decision-event envelopes;
- `python/argus_contracts/`: Pydantic models for Python producers/consumers;
- `typescript/`: TypeScript declarations for browser and Node consumers.

UUIDs and timestamps are strings on the wire. The Python models expose them as
`UUID` and `datetime` values, and serialize them through Pydantic JSON mode.

This tree must not contain business logic, ORM models, authentication,
infrastructure clients, or tenant data access.
