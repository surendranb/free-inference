"""Distributed execution tracing for FreeInference via OpenTelemetry (OTLP).

Streams Route 1/2/3 verification and scout spans to Arize Cloud (https://otlp.arize.com/v1/traces)
or local Phoenix using Python stdlib only. Thread-safe, secret-redacting, and strictly non-blocking.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import threading
import time
from typing import Any, Dict, List, Optional
import urllib.request
import uuid

_SECRET_KEY_RE = re.compile(
    r"(?:^|[._-])(api_?key|authorization|auth|secret|password|bearer|access_token|refresh_token|bot_token|private_key)$|^token$",
    re.I,
)
_URL_KEY_RE = re.compile(r"([?&](?:key|api_key|token)=)[^&\s]+", re.I)
_BEARER_RE = re.compile(r"(Bearer\s+)[A-Za-z0-9._\-]+", re.I)


def _get_keychain_secret(account: str) -> Optional[str]:
    """Fallback to macOS Keychain service 'agent-core' if environment variable is unset."""
    try:
        cmd = ["security", "find-generic-password", "-s", "agent-core", "-a", account, "-w"]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout.strip()
    except Exception:
        pass
    return None


def classify_http_status(http_status: Optional[int] = None, error_code: Optional[str] = None) -> str:
    """Return low-cardinality status class label for bounded telemetry dimensions."""
    if error_code == "AGENT_INCOMPLETE":
        return "incomplete"
    if error_code in ("TIMEOUT", "AGENT_TIMEOUT"):
        return "timeout"
    if http_status is not None:
        if 200 <= http_status < 300:
            return "2xx"
        if 400 <= http_status < 500:
            return "4xx"
        if 500 <= http_status < 600:
            return "5xx"
    if error_code:
        return "error"
    return "2xx"


def _sanitize_value(val: str) -> str:
    scrubbed = _URL_KEY_RE.sub(r"\1[REDACTED]", val)
    return _BEARER_RE.sub(r"\1[REDACTED]", scrubbed)


def _to_otlp_attr(key: str, value: Any) -> Optional[Dict[str, Any]]:
    if value is None or _SECRET_KEY_RE.search(key):
        return None
    if isinstance(value, bool):
        return {"key": key, "value": {"boolValue": value}}
    if isinstance(value, int):
        return {"key": key, "value": {"intValue": value}}
    if isinstance(value, float):
        return {"key": key, "value": {"doubleValue": value}}
    return {"key": key, "value": {"stringValue": _sanitize_value(str(value))}}


class ArizeTracer:
    """Thread-safe, resilient OTLP HTTP tracer for FreeInference verification runs."""

    def __init__(
        self,
        endpoint: Optional[str] = None,
        space_id: Optional[str] = None,
        api_key: Optional[str] = None,
        project_name: str = "free-inference",
        service_name: str = "freeinference-engine",
    ):
        self.api_key = api_key or os.getenv("ARIZE_API_KEY") or _get_keychain_secret("arize-api-key")
        self.space_id = space_id or os.getenv("ARIZE_SPACE_ID") or _get_keychain_secret("arize-space-id")

        cloud_ep = "https://otlp.arize.com/v1/traces"
        local_ep = "http://127.0.0.1:4318/v1/traces"
        raw_ep = (
            endpoint
            or os.getenv("ARIZE_OTLP_ENDPOINT")
            or _get_keychain_secret("ARIZE_OTLP_ENDPOINT")
            or (cloud_ep if (self.api_key and self.space_id) else os.getenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT") or local_ep)
        )
        self.endpoint = raw_ep if raw_ep.endswith("/v1/traces") else f"{raw_ep.rstrip('/')}/v1/traces"

        self.project_name = project_name
        self.service_name = service_name
        self.spans_queue: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
        self._trace_context: Dict[str, Dict[str, str]] = {}

    def start_trace(
        self,
        name: str,
        metadata: Optional[Dict[str, Any]] = None,
        run_id: Optional[str] = None,
        entry_point: Optional[str] = None,
    ) -> str:
        """Generate a new 32-hex trace ID and attach run correlation defaults."""
        trace_id = uuid.uuid4().hex
        meta = metadata or {}
        ep = entry_point or meta.get("entry_point") or (
            "nightly_ci" if os.getenv("GITHUB_ACTIONS") == "true" else "cli"
        )
        rid = run_id or meta.get("run_id") or trace_id[:12]
        with self._lock:
            self._trace_context[trace_id] = {"run_id": str(rid), "entry_point": str(ep)}
        return trace_id

    def log_span(
        self,
        trace_id: str,
        name: str,
        start_time_s: float,
        end_time_s: float,
        attributes: Optional[Dict[str, Any]] = None,
        status_ok: bool = True,
        status_message: str = "",
    ) -> str:
        """Record an OpenTelemetry span safely, scrubbing secrets and adding run correlation."""
        span_id = uuid.uuid4().hex[:16]
        with self._lock:
            ctx = dict(self._trace_context.get(trace_id, {}))

        merged: Dict[str, Any] = {**ctx, **(attributes or {})}
        otlp_attrs = []
        for k, v in merged.items():
            encoded = _to_otlp_attr(k, v)
            if encoded is not None:
                otlp_attrs.append(encoded)

        span = {
            "traceId": trace_id,
            "spanId": span_id,
            "name": name,
            "kind": 1,
            "startTimeUnixNano": str(int(start_time_s * 1e9)),
            "endTimeUnixNano": str(int(end_time_s * 1e9)),
            "attributes": otlp_attrs,
            "status": {
                "code": 1 if status_ok else 2,
                "message": _sanitize_value(status_message) if status_message else "",
            },
        }
        with self._lock:
            self.spans_queue.append(span)
        return span_id

    def flush(self) -> Dict[str, Any]:
        """Flush queued spans to the configured OTLP endpoint."""
        with self._lock:
            if not self.spans_queue:
                return {"status": "skipped", "message": "Empty spans queue"}
            spans = list(self.spans_queue)
            self.spans_queue.clear()

        payload = {
            "resourceSpans": [
                {
                    "resource": {
                        "attributes": [
                            {"key": "service.name", "value": {"stringValue": self.service_name}},
                            {"key": "project_name", "value": {"stringValue": self.project_name}},
                            {"key": "openinference.project.name", "value": {"stringValue": self.project_name}},
                        ]
                    },
                    "scopeSpans": [
                        {
                            "scope": {"name": "freeinference.engine"},
                            "spans": spans,
                        }
                    ],
                }
            ]
        }

        data = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "FreeInference-OTLP-Tracer/1.0",
            "x-project-name": self.project_name,
        }
        if self.space_id and self.api_key:
            headers["arize-space-id"] = self.space_id
            headers["arize-api-key"] = self.api_key

        req = urllib.request.Request(self.endpoint, data=data, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return {"status": "ok", "spans_exported": len(spans), "http_code": resp.status}
        except Exception as e:
            return {"status": "error", "error": _sanitize_value(str(e))}


tracer = ArizeTracer()
