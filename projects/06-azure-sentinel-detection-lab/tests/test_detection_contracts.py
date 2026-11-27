"""Static KQL contract checks and deterministic reference tests.

These tests do not execute KQL. Run the queries in an authorized Sentinel
workspace to validate the live connector schema and Kusto execution semantics.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUERY_DIR = ROOT / "queries"
FIXTURE_PATH = ROOT / "fixtures" / "signin-events.json"


def load_fixture() -> tuple[datetime, list[dict[str, str]]]:
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    reference_time = datetime.fromisoformat(payload["reference_time"].replace("Z", "+00:00"))
    return reference_time, payload["events"]


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def failed_signin_bursts(
    events: list[dict[str, str]], reference_time: datetime
) -> set[tuple[str, str, datetime, int]]:
    cutoff = reference_time - timedelta(days=1)
    counts: Counter[tuple[str, str, datetime]] = Counter()
    for event in events:
        timestamp = parse_timestamp(event["TimeGenerated"])
        user = event.get("UserPrincipalName", "")
        ip = event.get("IPAddress", "")
        if timestamp <= cutoff or event.get("ResultType") == "0" or not user or not ip:
            continue
        bucket = timestamp.replace(
            minute=(timestamp.minute // 15) * 15, second=0, microsecond=0
        )
        counts[(user, ip, bucket)] += 1
    return {
        (user, ip, bucket, count)
        for (user, ip, bucket), count in counts.items()
        if count >= 5
    }


def low_volume_ips(
    events: list[dict[str, str]], reference_time: datetime
) -> dict[str, int]:
    cutoff = reference_time - timedelta(days=7)
    counts: Counter[str] = Counter()
    for event in events:
        timestamp = parse_timestamp(event["TimeGenerated"])
        ip = event.get("IPAddress", "")
        if timestamp > cutoff and ip:
            counts[ip] += 1
    return {ip: count for ip, count in counts.items() if 1 <= count <= 3}


def test_failed_signin_kql_contract() -> None:
    query = (QUERY_DIR / "failed-signins.kql").read_text(encoding="utf-8")
    assert re.search(r"SigninLogs\s*\| where TimeGenerated > ago\(1d\)", query)
    assert '| where ResultType != "0"' in query
    assert "isnotempty(UserPrincipalName)" in query
    assert "isnotempty(IPAddress)" in query
    assert re.search(
        r"summarize FailedAttempts\s*=\s*count\(\) by UserPrincipalName, IPAddress, "
        r"bin\(TimeGenerated, 15m\)",
        query,
    )
    assert "| where FailedAttempts >= 5" in query


def test_rare_ip_kql_contract() -> None:
    query = (QUERY_DIR / "rare-ip-signins.kql").read_text(encoding="utf-8")
    assert re.search(r"SigninLogs\s*\| where TimeGenerated > ago\(7d\)", query)
    assert "| where isnotempty(IPAddress)" in query
    assert (
        "summarize SignInCount = count(), DistinctUsers = dcount(UserPrincipalName) by IPAddress"
        in query
    )
    assert "| where SignInCount between (1 .. 3)" in query
    assert "triage lead" in query.lower()


def test_synthetic_events_trigger_only_the_five_failure_burst() -> None:
    reference_time, events = load_fixture()
    findings = failed_signin_bursts(events, reference_time)
    assert findings == {
        (
            "lab-user-a@example.invalid",
            "198.51.100.10",
            datetime(2026, 11, 27, 11, 0, tzinfo=timezone.utc),
            5,
        )
    }


def test_low_volume_ip_reference_result_excludes_empty_and_four_plus_counts() -> None:
    reference_time, events = load_fixture()
    assert low_volume_ips(events, reference_time) == {
        "203.0.113.7": 1,
        "203.0.113.8": 2,
    }


def test_fixture_uses_reserved_documentation_addresses_and_fake_identities() -> None:
    _, events = load_fixture()
    allowed_prefixes = ("192.0.2.", "198.51.100.", "203.0.113.")
    assert all(event["UserPrincipalName"].endswith("@example.invalid") for event in events)
    assert all(
        not event["IPAddress"] or event["IPAddress"].startswith(allowed_prefixes)
        for event in events
    )
