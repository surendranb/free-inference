"""Slack notifications for FreeInference engine runs."""
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import List, Optional

IST = timezone(timedelta(hours=5, minutes=30))
DEFAULT_CHANNEL = "C0BLW648J3T"  # #build


def get_slack_token() -> str:
    """Retrieve SLACK_BOT_TOKEN from environment or macOS keychain."""
    token = os.environ.get("SLACK_BOT_TOKEN")
    if token:
        return token.strip()
    try:
        res = subprocess.run(
            ["security", "find-generic-password", "-s", "agent-core", "-a", "SLACK_BOT_TOKEN", "-w"],
            capture_output=True, text=True, check=True
        )
        return res.stdout.strip()
    except Exception:
        return ""


def post_slack_message(text: str, channel: Optional[str] = None) -> bool:
    """Send formatted message to Slack channel."""
    token = get_slack_token()
    if not token:
        print("[slack] Notice: No SLACK_BOT_TOKEN found; skipping alert", file=sys.stderr)
        return False
    chan = channel or os.environ.get("SLACK_CHANNEL_ID") or DEFAULT_CHANNEL
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    payload = json.dumps({"channel": chan, "text": text}).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            if not data.get("ok"):
                print(f"[slack] Slack API error: {data.get('error')}", file=sys.stderr)
                return False
            return True
    except Exception as e:
        print(f"[slack] Failed to deliver notification: {e}", file=sys.stderr)
        return False


def notify_job_started(catalog_count: int, flags: str, models: List[str]) -> bool:
    """Alert Slack that the daily update engine has started."""
    now_ist = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S IST")
    models_str = ", ".join(f"`{m}`" for m in models[:4])
    text = (
        f"🚀 *FreeInference Daily Update Started*\n"
        f"• *Time:* {now_ist}\n"
        f"• *Catalog Inventory:* {catalog_count} providers\n"
        f"• *Mode:* `{flags or '--verify --all'}`\n"
        f"• *Model Cascade:* {models_str}"
    )
    return post_slack_message(text)


def notify_job_completed(
    duration_s: float,
    verified_count: int,
    active_count: int,
    changed_count: int,
    deprecated_count: int,
    inconclusive_count: int,
    discovered_count: int,
    contradictions: Optional[List[str]] = None
) -> bool:
    """Alert Slack that the daily update engine finished, summarizing results and contradictions."""
    now_ist = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S IST")
    status_emoji = "⚠️" if deprecated_count > 0 or changed_count > 0 else "✅"

    lines = [
        f"{status_emoji} *FreeInference Daily Update Completed* ({duration_s:.1f}s)",
        f"• *Time:* {now_ist}",
        f"• *Verification:* {verified_count} audited (`{active_count}` active, `{changed_count}` changed, `{deprecated_count}` deprecated, `{inconclusive_count}` inconclusive)",
        f"• *Frontier Discovery:* `{discovered_count}` candidate models queued",
    ]

    if contradictions:
        lines.append("• *Contradictions & Changes Detected:*")
        for c in contradictions[:10]:
            lines.append(f"  - {c}")
        if len(contradictions) > 10:
            lines.append(f"  - ...and {len(contradictions) - 10} more")
    else:
        lines.append("• *Contradictions:* None. Catalog verified consistent with live endpoints.")

    text = "\n".join(lines)
    return post_slack_message(text)


def notify_job_failed(error_message: str, stage: str = "Execution") -> bool:
    """Alert Slack that the daily update engine encountered a failure."""
    now_ist = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S IST")
    text = (
        f"🚨 *FreeInference Daily Update Failed*\n"
        f"• *Time:* {now_ist}\n"
        f"• *Stage:* {stage}\n"
        f"• *Error:* ```{error_message[:1000]}```"
    )
    return post_slack_message(text)
