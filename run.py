"""
Entrypoint — start the Geneos alert listener.

Usage:
    python run.py

Environment variables (all optional):
    GENEOS_HOST             Bind address          (default: 0.0.0.0)
    GENEOS_PORT             Listen port           (default: 8000)
    GENEOS_LOG_LEVEL        Logging verbosity     (default: info)
    GENEOS_WEBHOOK_SECRET   Shared secret header  (default: disabled)
"""

import uvicorn

from geneos_listener.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "geneos_listener.main:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
        reload=False,
    )
