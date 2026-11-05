#!/usr/bin/env python3
"""CI failure alert script for freeinference.dev.

Sends failure notification to Slack (#build) and opens/updates a GitHub Issue.
Zero external dependencies (pure Python standard library).
"""
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))


def notify_slack(token, channel, text):
    try:
        url = "https://slack.com/api/chat.postMessage"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        }
        payload = json.dumps({"channel": channel, "text": text}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            if not data.get("ok"):
                print(f"[alert] Slack API error: {data.get('error')}", file=sys.stderr)
            else:
                print(f"[alert] Slack alert delivered to {channel}")
    except Exception as e:
        print(f"[alert] Failed to send Slack alert: {e}", file=sys.stderr)


def notify_github_issue(token, repo, run_url, run_number, commit_sha, now_str):
    if not token or not repo:
        return
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "free-inference-bot",
    }
    label = "ci-failure"
    try:
        # Check for open issue with this label
        list_url = f"https://api.github.com/repos/{repo}/issues?state=open&labels={label}"
        req = urllib.request.Request(list_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            issues = json.loads(resp.read().decode())

        body_text = (
            f"### 🚨 Nightly Probe CI Run #{run_number} Failed\n\n"
            f"- **Run:** [{run_number}]({run_url})\n"
            f"- **Commit:** `{commit_sha}`\n"
            f"- **Time:** {now_str}\n\n"
            f"Inspect the GitHub Actions workflow logs to diagnose and resolve."
        )

        if issues:
            # Comment on existing open issue
            issue_num = issues[0]["number"]
            comment_url = f"https://api.github.com/repos/{repo}/issues/{issue_num}/comments"
            payload = json.dumps({"body": body_text}).encode("utf-8")
            req = urllib.request.Request(comment_url, data=payload, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                print(f"[alert] Appended comment to existing issue #{issue_num}")
        else:
            # Create new issue
            create_url = f"https://api.github.com/repos/{repo}/issues"
            payload = json.dumps({
                "title": f"[CI Failure] Nightly Probe failed on {now_str.split(' ')[0]}",
                "body": body_text,
                "labels": [label, "automated"],
            }).encode("utf-8")
            req = urllib.request.Request(create_url, data=payload, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                created = json.loads(resp.read().decode())
                print(f"[alert] Created GitHub issue #{created.get('number')}")
    except Exception as e:
        print(f"[alert] Failed to manage GitHub issue: {e}", file=sys.stderr)


def main():
    token = os.environ.get("SLACK_BOT_TOKEN")
    channel = os.environ.get("SLACK_CHANNEL_ID", "C0BLW648J3T")  # #build
    gh_token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("REPO", "reachsuren/free-inference")
    run_id = os.environ.get("RUN_ID", "")
    run_number = os.environ.get("RUN_NUMBER", "manual")
    run_url = os.environ.get("RUN_URL", f"https://github.com/{repo}/actions/runs/{run_id}" if run_id else f"https://github.com/{repo}/actions")
    sha = os.environ.get("SHA", "")
    now_ist = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S IST")

    sha_short = sha[:7] if sha else "local"
    slack_text = (
        f"🚨 *FreeInference Nightly Probe FAILED*\n"
        f"• *Run:* <{run_url}|#{run_number}>\n"
        f"• *Repository:* `{repo}`\n"
        f"• *Commit:* `<https://github.com/{repo}/commit/{sha}|{sha_short}>\n"
        f"• *Time:* `{now_ist}`\n"
        f"• *Action:* Check workflow run logs for probe or verification error."
    )

    if token:
        notify_slack(token, channel, slack_text)
    else:
        print("[alert] SLACK_BOT_TOKEN not configured; skipping Slack notification")

    if gh_token:
        notify_github_issue(gh_token, repo, run_url, run_number, sha, now_ist)
    else:
        print("[alert] GITHUB_TOKEN not configured; skipping GitHub Issue creation")


if __name__ == "__main__":
    main()
