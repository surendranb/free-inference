"""core/telemetry.py - Distributed execution tracing for FreeInference.dev via OpenTelemetry (OTLP).

Streams agent verification runs, steps, and verdicts directly to Arize Phoenix / OTLP collectors.
Follows the zero-dependency standard library pattern (urllib.request, json, time, os, uuid).
Resilient by design: Telemetry errors are non-blocking and never halt catalog verification.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
import uuid
from typing import Any, Dict, List, Optional


class PhoenixTracer:
    """Lightweight, resilient OTLP HTTP tracer for FreeInference verification runs."""

    def __init__(
        self,
        endpoint: Optional[str] = None,
        project_name: str = "free-inference",
        service_name: str = "freeinference-engine",
    ):
        self.endpoint = (
            endpoint
            or os.getenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT")
            or os.getenv("PHOENIX_COLLECTOR_ENDPOINT", "http://127.0.0.1:4318/v1/traces")
        )
        if not self.endpoint.endswith("/v1/traces") and "v1/traces" not in self.endpoint:
            self.endpoint = f"{self.endpoint.rstrip('/')}/v1/traces"

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
        req = urllib.request.Request(
            self.endpoint,
            data=data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "FreeInference-OTLP-Tracer/1.0",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                count = len(self.spans_queue)
                self.spans_queue.clear()
                return {"status": "ok", "spans_exported": count, "http_code": resp.status}
        except Exception as e:
            # Telemetry error is strictly non-blocking
            # print(f"  [telemetry] OTLP export error: {e}")
            self.spans_queue.clear()
            return {"status": "error", "error": str(e)}


# Singleton default tracer instance
tracer = PhoenixTracer()
