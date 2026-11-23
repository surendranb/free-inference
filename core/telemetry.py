"""core/telemetry.py - Distributed execution tracing for FreeInference.dev via OpenTelemetry (OTLP).

Streams agent verification runs, steps, and verdicts directly to Arize Cloud and Phoenix collectors.
Supports both Cloud Arize (https://otlp.arize.com/v1) and local Phoenix (http://127.0.0.1:4318/v1/traces).
Follows the zero-dependency standard library pattern (urllib.request, json, time, os, uuid).
Resilient by design: Telemetry errors are non-blocking and never halt catalog verification.
"""
from __future__ import annotations

import json
import os
import subprocess
import time
import urllib.error
import urllib.request
import uuid
from typing import Any, Dict, List, Optional


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


class ArizeTracer:
    """Lightweight, resilient OTLP HTTP tracer for FreeInference verification runs."""

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
        if not raw_ep.endswith("/v1/traces"):
            self.endpoint = f"{raw_ep.rstrip('/')}/v1/traces"
        else:
            self.endpoint = raw_ep

        self.project_name = project_name
        self.service_name = service_name
        self.spans_queue: List[Dict[str, Any]] = []

    def start_trace(
        self,
        name: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Generate and return a new 32-hex trace ID."""
        return uuid.uuid4().hex

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
        """Record an OpenTelemetry span under the trace."""
        span_id = uuid.uuid4().hex[:16]
        start_ns = int(start_time_s * 1e9)
        end_ns = int(end_time_s * 1e9)

        attrs = attributes or {}
        otlp_attrs = []
        for k, v in attrs.items():
            if isinstance(v, bool):
                otlp_attrs.append({"key": k, "value": {"boolValue": v}})
            elif isinstance(v, int):
                otlp_attrs.append({"key": k, "value": {"intValue": v}})
            elif isinstance(v, float):
                otlp_attrs.append({"key": k, "value": {"doubleValue": v}})
            else:
                otlp_attrs.append({"key": k, "value": {"stringValue": str(v)}})

        span = {
            "traceId": trace_id,
            "spanId": span_id,
            "name": name,
            "kind": 1,  # SPAN_KIND_INTERNAL
            "startTimeUnixNano": str(start_ns),
            "endTimeUnixNano": str(end_ns),
            "attributes": otlp_attrs,
            "status": {
                "code": 1 if status_ok else 2,  # 1 = OK, 2 = ERROR
                "message": status_message,
            },
        }
        self.spans_queue.append(span)
        return span_id

    def flush(self) -> Dict[str, Any]:
        """Send queued spans to the OTLP collector."""
        if not self.spans_queue:
            return {"status": "skipped", "message": "Empty spans queue"}

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
                            "scope": {"name": "freeinference.antigravity"},
                            "spans": list(self.spans_queue),
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
            with urllib.request.urlopen(req, timeout=10) as resp:
                count = len(self.spans_queue)
                self.spans_queue.clear()
                return {"status": "ok", "spans_exported": count, "http_code": resp.status}
        except Exception as e:
            # Telemetry error is strictly non-blocking
            self.spans_queue.clear()
            return {"status": "error", "error": str(e)}


# Singleton default tracer instance
tracer = ArizeTracer()
