# Sentinel detection matrix

| Use case | Query | Signal | Suggested handling | ATT&CK |
|---|---|---|---|---|
| Failed sign-in burst | `queries/failed-signins.kql` | At least 5 failures for one user and IP in a 15-minute bucket | Scheduled analytics rule; review MFA, subsequent successes, user risk and source reputation | T1110 - Brute Force |
| Low-volume source IP | `queries/rare-ip-signins.kql` | 1-3 sign-ins from an IP in 7 days | Hunting pivot only; correlate with additional signals before alerting | No direct mapping asserted |

## Tuning notes

- A shared NAT, VPN, secure web gateway or identity proxy can aggregate many users behind one IP. Do not treat IP counts as user counts.
- A low-volume IP may be normal for a travelling user, a new employee or a rarely used service account.
- The failed-sign-in query groups by user and IP. Distributed attacks that rotate source IPs may evade this simple threshold and need a separate per-user or per-ASN analytic.
- Validate `ResultType` type and semantics in the workspace. The sample compares it to string `"0"`, the expected success code in the Entra `SigninLogs` schema.
- Keep alert frequency shorter than the lookback window and configure suppression/grouping deliberately to avoid duplicate incidents.
