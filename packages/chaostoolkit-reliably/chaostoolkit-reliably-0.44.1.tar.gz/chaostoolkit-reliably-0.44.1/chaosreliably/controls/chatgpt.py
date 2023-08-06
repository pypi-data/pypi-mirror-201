import os
from typing import Any, Dict, Union

import httpx
from chaoslib.types import Configuration, Experiment, Journal, Secrets
from logzero import logger

from chaosreliably.controls import find_extension_by_name

__all__ = ["after_experiment_control"]
OPENAI_URL = "https://api.openai.com/v1/chat/completions"


def after_experiment_control(
    context: Experiment,
    state: Journal,
    openai_model: Union[str, Dict[str, str]] = "gpt-3.5-turbo",
    configuration: Configuration = None,
    secrets: Secrets = None,
    **kwargs: Any,
) -> None:
    experiment = state["experiment"]
    extension = find_extension_by_name(experiment, "chatgpt")
    if not extension:
        return None

    if isinstance(openai_model, dict):
        openai_model = os.getenv(
            openai_model["key"], openai_model.get("default", "gpt-3.5-turbo")
        )

    secrets = secrets or {}
    openapi_secrets = secrets.get("openai", {})

    org = openapi_secrets.get("org") or os.getenv("OPENAI_ORG")
    if not org:
        logger.warning("Cannot call OpenAI: missing org")
        return None

    key = openapi_secrets.get("key") or os.getenv("OPENAI_API_KEY")
    if not key:
        logger.warning("Cannot call OpenAI: missing secret key")
        return None

    logger.debug(
        f"Asking OpenAPI for chat completions using model '{openai_model}'"
    )

    results = []
    chat = []
    suffix = ". Render in unrendered markdown."
    for message in extension.get("messages", [])[:]:
        message["content"] += suffix
        chat.append(message)
        try:
            r = httpx.post(
                OPENAI_URL,
                timeout=60,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {key}",
                    "OpenAI-Organization": org,
                },
                json={
                    "model": openai_model,
                    "temperature": 0.3,
                    "messages": chat,
                },
            )
        except httpx.ReadTimeout:
            logger.debug("OpenAI took too long to respond unfortunately")
        else:
            message["content"] = message["content"].replace(suffix, "")
            if r.status_code > 399:
                logger.debug(f"OpenAI chat failed: {r.status_code}: {r.json()}")
                break

            results.append(r.json())
            chat.append(results[-1]["choices"][0]["message"])

    extension["results"] = results
