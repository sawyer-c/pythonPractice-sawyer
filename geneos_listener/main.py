"""
Geneos Active Console — webhook listener.

Receives alert events POSTed by a Geneos Gateway and forwards them to the
handler (currently a stub, to be wired to an LLM agent).

Geneos Gateway webhook configuration (setup XML snippet):
  <webhook>
    <url>http://<this-host>:<port>/webhook/alert</url>
    <method>POST</method>
    <contentType>application/json</contentType>
    <body>
      {
        "gateway":          "_gateway",
        "probe":            "_netprobe",
        "managedEntity":    "_managed_entity",
        "sampler":          "_sampler",
        "dataview":         "_dataview",
        "variable":         "_variable",
        "severity":         "_severity",
        "previousSeverity": "_previousSeverity",
        "value":            "_value",
        "message":          "_message",
        "rule":             "_rule",
        "timestamp":        "_timestamp"
      }
    </body>
  </webhook>
"""

import logging

from fastapi import FastAPI, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse

from .config import settings
from .handler import handle_alert
from .models import GeneosAlert, WebhookResponse

logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Geneos Alert Listener",
    description="Webhook receiver for ITRS Geneos Gateway alert events.",
    version="0.1.0",
)


# ---------------------------------------------------------------------------
# Webhook endpoint
# ---------------------------------------------------------------------------

@app.post(
    "/webhook/alert",
    response_model=WebhookResponse,
    status_code=status.HTTP_200_OK,
    summary="Receive a Geneos alert event",
)
async def receive_alert(
    alert: GeneosAlert,
    x_geneos_secret: str | None = Header(None, alias="X-Geneos-Secret"),
) -> WebhookResponse:
    """
    Called by the Geneos Gateway whenever an alert rule fires.

    Optional: set GENEOS_WEBHOOK_SECRET in your environment and configure
    the Gateway to send that value in the X-Geneos-Secret header for
    basic request validation.
    """
    _validate_secret(x_geneos_secret)

    await handle_alert(alert)

    return WebhookResponse(status="ok", message="Alert received")


# ---------------------------------------------------------------------------
# Health / readiness
# ---------------------------------------------------------------------------

@app.get("/health", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse({"status": "healthy"})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _validate_secret(provided: str | None) -> None:
    expected = settings.webhook_secret
    if not expected:
        return  # secret validation disabled
    if provided != expected:
        logger.warning("Webhook request rejected: bad or missing X-Geneos-Secret")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-Geneos-Secret header",
        )
