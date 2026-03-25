"""
Alert handler — the bridge between incoming Geneos webhook events and your
LLM agent (or any other downstream action).

Current behaviour:
  - Logs every received alert
  - Calls dispatch_to_llm_agent() as a clearly-marked stub

When you're ready to wire in your LLM agent, replace the body of
dispatch_to_llm_agent() with the real integration (Anthropic SDK, OpenAI,
LangChain, etc.).
"""

import logging

from .models import GeneosAlert

logger = logging.getLogger(__name__)


async def handle_alert(alert: GeneosAlert) -> None:
    """Entry point called for every inbound Geneos alert."""
    logger.info("Received alert: %s", alert.summary())

    await dispatch_to_llm_agent(alert)


# ---------------------------------------------------------------------------
# LLM agent stub — replace this when you're ready to integrate
# ---------------------------------------------------------------------------

async def dispatch_to_llm_agent(alert: GeneosAlert) -> None:
    """
    TODO: Implement LLM agent integration here.

    Suggested steps:
      1. Build a prompt from alert.summary() and any relevant context.
      2. Call your LLM agent (e.g. Anthropic SDK, Claude Agent SDK, LangChain).
      3. Parse the agent's response and take action (ticket, Slack message, auto-remediation, etc.).

    Example skeleton (Anthropic SDK):
      import anthropic
      client = anthropic.Anthropic()
      response = client.messages.create(
          model="claude-opus-4-6",
          max_tokens=1024,
          messages=[{"role": "user", "content": _build_prompt(alert)}],
      )
      _act_on_response(response, alert)
    """
    logger.debug("dispatch_to_llm_agent called for alert: %s", alert.summary())
    # -- stub: nothing happens yet --


def _build_prompt(alert: GeneosAlert) -> str:
    """Helper: turn a GeneosAlert into an LLM prompt string."""
    return (
        f"A Geneos monitoring alert has been received:\n\n"
        f"  Gateway:        {alert.gateway}\n"
        f"  Managed Entity: {alert.managed_entity}\n"
        f"  Sampler:        {alert.sampler}\n"
        f"  Variable:       {alert.variable}\n"
        f"  Severity:       {alert.severity} (was {alert.previous_severity})\n"
        f"  Value:          {alert.value}\n"
        f"  Rule:           {alert.rule}\n"
        f"  Message:        {alert.message}\n\n"
        f"Analyse the alert and suggest a remediation action."
    )
