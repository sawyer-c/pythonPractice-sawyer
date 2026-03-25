"""
Pydantic models for inbound Geneos Gateway webhook payloads.

Geneos webhooks are configured per-alert rule in the Gateway setup XML.
The exact fields included depend on your Gateway configuration — adjust
the model below to match what your Gateway is actually sending.

Reference:
  https://docs.itrsgroup.com/docs/geneos-gateway-hub/2.6.0/webconsole/webhooks/
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class GeneosAlert(BaseModel):
    """Represents a single alert event pushed from a Geneos Gateway webhook."""

    # --- Core identity fields (standard Gateway webhook variables) ---
    gateway: str = Field("", description="Name of the Gateway that fired the alert")
    probe: str = Field("", description="Netprobe name")
    managed_entity: str = Field("", alias="managedEntity", description="Managed entity name")
    sampler: str = Field("", description="Sampler name")
    dataview: str = Field("", description="Dataview name")
    variable: str = Field("", description="Row/headline variable that triggered the alert")

    # --- Severity / state ---
    severity: str = Field("", description="Alert severity: OK, Warning, Critical, etc.")
    previous_severity: str = Field("", alias="previousSeverity", description="Previous severity before this change")
    value: str = Field("", description="Current value of the variable")

    # --- Human-readable context ---
    message: str = Field("", description="Alert message / description")
    rule: str = Field("", description="Gateway rule name that triggered the alert")

    # --- Timing ---
    timestamp: datetime | None = Field(None, description="When the alert was generated (ISO 8601)")

    # --- Catch-all for any extra fields your Gateway may include ---
    extra: dict[str, Any] = Field(default_factory=dict)

    model_config = {"populate_by_name": True, "extra": "allow"}

    def is_critical(self) -> bool:
        return self.severity.lower() == "critical"

    def is_ok(self) -> bool:
        return self.severity.lower() == "ok"

    def summary(self) -> str:
        """One-line human-readable summary, useful for logging and LLM prompts."""
        ts = self.timestamp.isoformat() if self.timestamp else "unknown time"
        return (
            f"[{self.severity.upper()}] {self.managed_entity}/{self.sampler}/{self.variable}"
            f" = {self.value!r} at {ts} (rule: {self.rule or 'n/a'})"
        )


class WebhookResponse(BaseModel):
    status: str
    message: str
