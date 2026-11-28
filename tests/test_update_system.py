#!/usr/bin/env python3
"""Contract and regression tests for the Three-Route FreeInference update system."""

import io
import json
from pathlib import Path
import sys
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core import intake, model, scout, telemetry, verifier  # noqa: E402


class _FakeResponse:
    def __init__(self, payload, status=200):
        self._raw = payload.encode("utf-8") if isinstance(payload, str) else json.dumps(payload).encode("utf-8")
        self.status = status

    def read(self):
        return self._raw

    def getcode(self):
        return self.status

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class TestThreeRouteUpdateSystem(unittest.TestCase):
    def test_model_cascade_prioritizes_gemini_3_5_flash_lite(self):
        self.assertEqual(model.MODEL_CASCADE[0], "gemini-3.5-flash-lite")
        self.assertNotIn("gemini-2.5-flash-lite", model.MODEL_CASCADE)
        self.assertTrue(hasattr(model, "call_gemini_text"), "core.model must expose call_gemini_text")

    def test_feed_route_ovh_list_and_untruncated_items(self):
        # 60 synthetic real-shape OVH items (unpriced endpoint list) verifying NO [:50] truncation
        ovh_list = [
            {
                "name": f"model-{i}",
                "id": f"org/model-{i}",
                "available": True,
                "category": "Large Language Models (LLM)",
            }
            for i in range(60)
        ]

        def fake_urlopen(req, timeout=20):
            url = req.full_url if hasattr(req, "full_url") else str(req)
            if "catalog.endpoints.ai.ovh.net" in url:
                return _FakeResponse(ovh_list)
            return _FakeResponse("<html><body>OVHcloud AI Endpoints beta free limits 12 rpm</body></html>")

        prov = {
            "name": "OVHcloud AI Endpoints",
            "url": "https://www.ovhcloud.com/en/public-cloud/ai-endpoints/",
            "base_url": "https://endpoints.ai.cloud.ovh.net/v1",
            "channel": "feed",
            "models": [],
        }
        with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
            obs = intake.fetch_feed_route(prov)

        self.assertIsInstance(obs, dict)
        self.assertTrue(obs["ok"])
        self.assertEqual(obs["route"], "feed")
        self.assertFalse(obs["payload"]["priced"])
        self.assertEqual(len(obs["payload"]["available_models"]), 60)
        self.assertEqual(obs["payload"]["free_models"], [])
        self.assertIn("OVHcloud", obs["docs_text"])

    def test_feed_kilo_filters_free_and_flags_auto_routers(self):
        kilo_payload = {
            "data": [
                {"id": "kilo-auto/free", "name": "Kilo Auto Free", "isFree": True, "autoRouting": True, "pricing": {"prompt": "0", "completion": "0"}},
                {"id": "minimax/minimax-m2.5:free", "name": "MiniMax M2.5 Free", "isFree": True, "context_length": 200000, "pricing": {"prompt": "0", "completion": "0"}},
                {"id": "openai/gpt-5", "name": "GPT 5", "isFree": False, "pricing": {"prompt": "0.005", "completion": "0.015"}},
            ]
        }

        def fake_urlopen(req, timeout=20):
            url = req.full_url if hasattr(req, "full_url") else str(req)
            if "api.kilo.ai" in url:
                return _FakeResponse(kilo_payload)
            return _FakeResponse("<html><body>Kilo Gateway free models rate limit</body></html>")

        prov = {
            "name": "Kilo Gateway",
            "url": "https://kilo.ai/gateway",
            "base_url": "https://api.kilo.ai/v1",
            "channel": "feed",
            "models": [],
        }
        with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
            obs = intake.fetch_feed_route(prov)

        self.assertTrue(obs["ok"])
        ids = [m["id"] for m in obs["payload"]["free_models"]]
        self.assertIn("minimax/minimax-m2.5:free", ids)
        self.assertNotIn("kilo-auto/free", ids)
        self.assertNotIn("openai/gpt-5", ids)

    def test_api_route_never_leaks_gemini_key_to_third_party(self):
        captured_headers = []

        def fake_urlopen(req, timeout=20):
            url = req.full_url if hasattr(req, "full_url") else str(req)
            hdrs = {k.lower(): v for k, v in getattr(req, "headers", {}).items()}
            captured_headers.append((url, hdrs))
            if "deepinfra.com" in url:
                return _FakeResponse({"data": [{"id": "meta-llama/Llama-3.3-70B-Instruct", "pricing": {"input": 0, "output": 0}}]})
            return _FakeResponse("<html><body>DeepInfra rate limits 200 concurrent requests</body></html>")

        prov = {
            "name": "DeepInfra",
            "url": "https://docs.deepinfra.com/account/rate-limits",
            "base_url": "https://api.deepinfra.com/v1/openai",
            "channel": "api",
            "models": [],
        }
        with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
            obs = intake.fetch_api_route(prov, gemini_key="AIza_SECRET_DO_NOT_LEAK")

        self.assertTrue(obs["ok"])
        for url, hdrs in captured_headers:
            if "generativelanguage.googleapis.com" not in url:
                self.assertNotIn("authorization", hdrs, f"Gemini key leaked in Authorization header to {url}")
                self.assertNotIn("AIza_SECRET_DO_NOT_LEAK", url)

    def test_web_route_antigravity_uses_80k_budget_and_guards_incomplete(self):
        sent_bodies = []

        def fake_urlopen(req, timeout=30):
            if getattr(req, "data", None):
                sent_bodies.append(json.loads(req.data.decode("utf-8")))
                return _FakeResponse({"id": "int_123"})
            return _FakeResponse({
                "id": "int_123",
                "status": "incomplete",
                "usage": {"total_tokens": 15000},
                "steps": [{"content": [{"text": "still browsing"}]}],
            })

        prov = {
            "name": "Cerebras",
            "url": "https://inference-docs.cerebras.ai/support/rate-limits",
            "channel": "web",
            "models": [{"name": "llama3.1-8b"}],
        }
        with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen), mock.patch("time.sleep"):
            obs = intake.fetch_web_route_antigravity(prov, gemini_key="AIza_TEST", timeout=10)

        self.assertGreaterEqual(sent_bodies[0]["agent_config"]["max_total_tokens"], 60000)
        self.assertFalse(obs["ok"])
        self.assertEqual(obs["error_code"], "AGENT_INCOMPLETE")
        self.assertEqual(obs["agent_meta"]["interaction_id"], "int_123")

    def test_canonical_dedup_collapses_openrouter_display_name_twins(self):
        or_models = [
            {
                "id": "baidu/ernie-5.5-flash-preview:free",
                "name": "Baidu: ERNIE-5.5-Flash-Preview (free)",
                "context_length": 131072,
                "pricing": {"prompt": "0", "completion": "0"},
            },
            {
                "id": "openrouter/free",
                "name": "Free Models Router",
                "context_length": 200000,
                "pricing": {"prompt": "0", "completion": "0"},
            },
        ]
        catalog = {
            "providers": [
                {
                    "name": "OpenRouter",
                    "url": "https://openrouter.ai/models?max_price=0",
                    "channel": "feed",
                    "models": [
                        {
                            "name": "baidu/ernie-5.5-flash-preview:free",
                            "cost": "$0",
                            "context": "128K",
                            "rpm": "20",
                            "tpm": "Provider-dependent",
                            "rpd": "50",
                            "tpd": "Not published",
                            "verified": "2026-11-24",
                        }
                    ],
                }
            ]
        }

        def fake_urlopen(req, timeout=20):
            url = req.full_url if hasattr(req, "full_url") else str(req)
            if "openrouter.ai" in url:
                return _FakeResponse({"data": or_models})
            return _FakeResponse({})

        with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
            added = scout.expand_base_catalog_from_sources(catalog, apply_updates=True)

        names = [m["name"] for m in catalog["providers"][0]["models"]]
        self.assertEqual(names, ["baidu/ernie-5.5-flash-preview:free"], f"Duplicates/routers leaked: {names}")
        self.assertEqual(added, [])

    def test_write_gate_blocks_incomplete_drop_and_preserves_model_quotas(self):
        original_models = [
            {"name": "m1", "cost": "$0", "context": "128K", "rpm": "30", "tpm": "60K", "rpd": "14400", "tpd": "1M", "verified": "2026-11-20"},
            {"name": "m2", "cost": "$0", "context": "128K", "rpm": "30", "tpm": "60K", "rpd": "14400", "tpd": "1M", "verified": "2026-11-20"},
            {"name": "m3", "cost": "$0", "context": "128K", "rpm": "30", "tpm": "60K", "rpd": "14400", "tpd": "1M", "verified": "2026-11-20"},
            {"name": "m4", "cost": "$0", "context": "128K", "rpm": "30", "tpm": "60K", "rpd": "14400", "tpd": "1M", "verified": "2026-11-20"},
        ]
        # 1. Incomplete / blocked web observation must NOT overwrite
        prov_web = {
            "name": "Cerebras",
            "url": "https://inference-docs.cerebras.ai/support/rate-limits",
            "free_type": "Rate-limited free",
            "verified": "2026-11-20",
            "verified_method": "docs",
            "channel": "web",
            "models": [dict(m) for m in original_models],
        }
        # 2. Suspect >50% shrink + deprecation on web must NOT wipe models silently
        prov_drop = {
            "name": "Groq",
            "url": "https://console.groq.com/docs/rate-limits",
            "free_type": "Rate-limited free",
            "verified": "2026-11-20",
            "verified_method": "docs",
            "channel": "web",
            "models": [dict(m) for m in original_models],
        }
        # 3. Valid changed feed with preserved quotas + new model
        prov_feed = {
            "name": "OpenRouter",
            "url": "https://openrouter.ai/models?max_price=0",
            "free_type": "Rate-limited free",
            "verified": "2026-11-20",
            "verified_method": "live-probe",
            "channel": "feed",
            "models": [original_models[0].copy()],
        }

        cat = {"providers": [prov_web, prov_drop, prov_feed]}

        def fake_fetch(prov, gemini_key=None):
            if prov["name"] == "Cerebras":
                return {"route": "web", "provider": "Cerebras", "ok": False, "http_status": 200, "error_code": "AGENT_INCOMPLETE", "payload": {}, "docs_text": "", "agent_meta": {"steps": 4}}
            return {"route": prov["channel"], "provider": prov["name"], "ok": True, "http_status": 200, "error_code": None, "payload": {"free_models": [{"id": "m1"}, {"id": "m5"}]}, "docs_text": "ok", "agent_meta": {}}

        def fake_reason(prompt, schema, validator_fn, key=None, max_tries=3):
            if "Groq" in prompt:
                return {"status": "deprecated", "is_free_active": False, "models": [], "summary": "Suspicious single-run drop"}
            return {
                "status": "changed",
                "is_free_active": True,
                "models": [
                    {"name": "m1", "cost": "$0", "context": "128K"},
                    {"name": "m5", "cost": "$0", "context": "64K"},
                ],
                "summary": "Added m5 while retaining m1",
            }

        with mock.patch("core.verifier.acquire_observation", side_effect=fake_fetch), \
             mock.patch("core.verifier.call_with_self_correction", side_effect=fake_reason), \
             mock.patch.object(verifier.tracer, "flush", return_value={"status": "mocked"}), \
             mock.patch.object(verifier.tracer, "log_span", return_value="sp_1"):
            verifier.verify_catalog(cat, apply_updates=True, force_all=True, key="AIza_TEST")

        # Incomplete preserved
        self.assertEqual(len(prov_web["models"]), 4)
        self.assertEqual(prov_web["verified"], "2026-11-20")
        # Single-run deprecation blocked
        self.assertEqual(len(prov_drop["models"]), 4)
        self.assertEqual(prov_drop["free_type"], "Rate-limited free")
        # Valid feed change updated & preserved m1's custom RPM/TPD quotas
        self.assertEqual([m["name"] for m in prov_feed["models"]], ["m1", "m5"])
        self.assertEqual(prov_feed["models"][0]["rpm"], "30")
        self.assertEqual(prov_feed["models"][0]["tpd"], "1M")
        self.assertEqual(prov_feed["verified_method"], "live-probe")

    def test_audit_catalog_quality_catches_duplicates_and_bad_method(self):
        bad_cat = {
            "providers": [
                {
                    "name": "BadProv",
                    "url": "https://example.com",
                    "free_type": "Rate-limited free",
                    "verified": "2026-11-25",
                    "verified_method": "claim",
                    "models": [
                        {"name": "M1", "cost": "$0", "context": "32K", "rpm": "10", "tpm": "10K", "rpd": "100", "tpd": "1M", "verified": "2026-11-25"},
                        {"name": "m1", "cost": "$0", "context": "32K", "rpm": "10", "tpm": "10K", "rpd": "100", "tpd": "1M", "verified": "2026-11-25"},
                    ],
                }
            ]
        }
        issues = verifier.audit_catalog_quality(bad_cat)
        self.assertTrue(any("verified_method" in i for i in issues))
        self.assertTrue(any("duplicate model" in i for i in issues))

    def test_write_gate_blocks_partial_priced_feed_and_dedups_plus(self):
        self.assertEqual(intake.normalize_model_key("Command A+"), intake.normalize_model_key("Command A Plus"))
        prov_kilo = {
            "name": "Kilo Gateway",
            "url": "https://kilo.ai/gateway",
            "free_type": "Rate-limited free",
            "verified": "2026-11-07",
            "verified_method": "live-probe",
            "channel": "feed",
            "models": [
                {"name": "m1", "cost": "$0", "context": "128K", "rpm": "20", "tpm": "Not published", "rpd": "Not published", "tpd": "Not published", "verified": "2026-11-07"},
                {"name": "m2", "cost": "$0", "context": "128K", "rpm": "20", "tpm": "Not published", "rpd": "Not published", "tpd": "Not published", "verified": "2026-11-07"},
                {"name": "m3", "cost": "$0", "context": "128K", "rpm": "20", "tpm": "Not published", "rpd": "Not published", "tpd": "Not published", "verified": "2026-11-07"},
            ],
        }
        obs = {
            "route": "feed",
            "provider": "Kilo Gateway",
            "ok": True,
            "http_status": 200,
            "error_code": None,
            "payload": {
                "priced": True,
                "free_models": [{"id": f"org/m{i}:free"} for i in range(1, 11)],
            },
            "docs_text": "",
            "agent_meta": {},
        }
        partial_verdict = {
            "status": "active",
            "is_free_active": True,
            "models": [{"name": "org/m1:free", "cost": "$0", "context": "128K"}],
            "summary": "Only emitted 1 of 10",
        }
        self.assertIsNotNone(verifier.validate_verification_output(partial_verdict, obs=obs))
        gate = verifier.apply_write_gate(prov_kilo, obs, partial_verdict, "2026-11-26", apply_updates=True)
        self.assertTrue(gate["review_required"])
        self.assertFalse(gate["write_applied"])
        self.assertEqual(len(prov_kilo["models"]), 3)

    def test_aihubmix_free_quota_config_parses_as_priced_feed(self):
        cfg = {
            "success": True,
            "data": {
                "daily_request_limit": 100,
                "daily_token_limit": 1000000,
                "minute_limit": 10,
                "trial_unpaid_request_limit": 10,
                "weight_map": {"step-3.7-flash-free": 1, "gpt-4o-free": 5},
            },
        }

        def fake_urlopen(req, timeout=20):
            url = req.full_url if hasattr(req, "full_url") else str(req)
            if "free_quota_config" in url:
                return _FakeResponse(cfg)
            return _FakeResponse("<html><body>HTML rejected</body></html>")

        prov = {"name": "AIHubMix", "url": "https://aihubmix.com", "channel": "feed", "models": []}
        with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
            obs = intake.fetch_feed_route(prov)

        self.assertTrue(obs["ok"])
        self.assertTrue(obs["payload"]["priced"])
        self.assertEqual([m["id"] for m in obs["payload"]["free_models"]], ["step-3.7-flash-free", "gpt-4o-free"])

    def test_fetch_machine_docs_rejects_html_and_follows_llms_txt(self):
        def fake_urlopen(req, timeout=20):
            url = req.full_url if hasattr(req, "full_url") else str(req)
            if url == "https://docs.example.ai/llms.txt":
                return _FakeResponse("# Docs\n- [Pricing](https://docs.example.ai/guides/pricing.md): Free tier limits\n")
            if url == "https://docs.example.ai/guides/pricing.md":
                return _FakeResponse("# Pricing\nFree developer tier includes 20 RPM and 1M TPD.\n" + "x" * 60)
            return _FakeResponse("<!doctype html><html><body>SPA shell</body></html>")

        prov = {"name": "ExampleAI", "url": "https://docs.example.ai/start", "channel": "web", "models": []}
        with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
            obs = intake.fetch_machine_docs(prov)

        self.assertTrue(obs["ok"])
        self.assertEqual(obs["agent_meta"]["acquisition_mode"], "llms_md")
        self.assertIn("20 RPM", obs["docs_text"])

    def test_llms_inconclusive_escalates_to_antigravity_chrome(self):
        prov = {
            "name": "StubProvider",
            "url": "https://example.com/pricing",
            "free_type": "Rate-limited free",
            "verified": "2026-11-20",
            "verified_method": "docs",
            "channel": "web",
            "models": [{"name": "m1", "cost": "$0", "context": "64K", "rpm": "10", "tpm": "10K", "rpd": "100", "tpd": "1M", "verified": "2026-11-20"}],
        }
        llms_obs = {"route": "web", "provider": "StubProvider", "ok": True, "http_status": 200, "error_code": None, "payload": {"docs_kind": "machine_markdown"}, "docs_text": "# Sparse index", "agent_meta": {"acquisition_mode": "llms_md"}}
        chrome_obs = {"route": "web", "provider": "StubProvider", "ok": True, "http_status": 200, "error_code": None, "payload": {}, "docs_text": "Verified active free tier on pricing page.", "agent_meta": {"acquisition_mode": "antigravity_chrome", "steps": 5, "total_tokens": 25000}}

        verdicts = iter([
            {"status": "inconclusive", "is_free_active": False, "models": [], "summary": "Insufficient pricing detail in markdown"},
            {"status": "active", "is_free_active": True, "models": [{"name": "m1", "cost": "$0", "context": "64K"}], "summary": "Confirmed active via Chrome"},
        ])

        with mock.patch("core.verifier.acquire_observation", return_value=llms_obs), \
             mock.patch("core.verifier.fetch_web_route_antigravity", return_value=chrome_obs) as chrome_mock, \
             mock.patch("core.verifier.call_with_self_correction", side_effect=lambda *a, **kw: next(verdicts)):
            res = verifier.verify_provider(prov, key="AIza_TEST", apply_updates=False)

        self.assertEqual(chrome_mock.call_count, 1)
        self.assertEqual(res["acquisition_mode"], "llms_then_chrome")
        self.assertEqual(res["status"], "active")

    def test_mistral_fetches_required_billing_docs_and_v0_not_mapped_to_vercel_gateway(self):
        def fake_urlopen(req, timeout=20):
            url = req.full_url if hasattr(req, "full_url") else str(req)
            if "usage-limits/llms.txt" in url:
                return _FakeResponse("# Usage and limits\nFree mode doesn't include API access. Billing activation required.\n" + "x" * 60)
            if "subscriptions/llms.txt" in url:
                return _FakeResponse("# Subscription\nPay-as-you-go prepaid credits.\n" + "x" * 60)
            return _FakeResponse("<!doctype html><html></html>")

        mistral_prov = {"name": "Mistral La Plateforme", "url": "https://docs.mistral.ai", "channel": "web", "models": []}
        with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
            obs = intake.fetch_machine_docs(mistral_prov)

        self.assertTrue(obs["ok"])
        self.assertIn("doesn't include API access", obs["docs_text"])

        cat = {
            "providers": [
                {"name": "v0 (Vercel)", "url": "https://v0.app/docs/pricing", "models": [{"name": "v0 Mini"}]},
                {"name": "Google Colab", "url": "https://research.google.com/colaboratory/faq.html", "models": []},
                {"name": "Google AI Studio (Gemini API)", "url": "https://ai.google.dev", "models": []},
            ]
        }
        mdev = {
            "vercel": {"models": {"gateway-model": {"name": "Gateway", "cost": {"input": 0, "output": 0}}}},
            "google": {"models": {"gemini-test": {"name": "gemini-test", "cost": {"input": 0, "output": 0}}}},
        }

        def fake_expand_urlopen(req, timeout=20):
            url = req.full_url if hasattr(req, "full_url") else str(req)
            if "models.dev" in url:
                return _FakeResponse(mdev)
            return _FakeResponse({})

        with mock.patch("urllib.request.urlopen", side_effect=fake_expand_urlopen):
            added = scout.expand_base_catalog_from_sources(cat, apply_updates=True)

        self.assertEqual([m["name"] for m in cat["providers"][0]["models"]], ["v0 Mini"])
        self.assertEqual(cat["providers"][1]["models"], [])
        self.assertEqual([a["provider"] for a in added], ["Google AI Studio (Gemini API)"])

    def test_telemetry_redacts_secrets_and_tags_run_context(self):
        tr = telemetry.ArizeTracer(endpoint="https://otlp.arize.com/v1/traces", space_id="sp", api_key="ak")
        tid = tr.start_trace("run", metadata={"run_id": "r123", "entry_point": "cli"})
        tr.log_span(
            tid,
            "verify.OpenRouter",
            1.0,
            2.0,
            attributes={
                "route": "feed",
                "status_class": "2xx",
                "verdict": "active",
                "api_key": "SHOULD_BE_REDACTED",
                "target_url": "https://example.com?key=AIzaSECRET123",
            },
        )
        attrs = {a["key"]: next(iter(a["value"].values())) for a in tr.spans_queue[0]["attributes"]}
        self.assertNotIn("api_key", attrs)
        self.assertNotIn("AIzaSECRET123", attrs.get("target_url", ""))
        self.assertEqual(attrs.get("route"), "feed")


if __name__ == "__main__":
    unittest.main(verbosity=2)
