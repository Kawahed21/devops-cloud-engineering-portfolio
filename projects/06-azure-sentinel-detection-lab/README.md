# 06: Azure Sentinel Detection Lab

## Objective
Build and test two Microsoft Entra ID sign-in detections with Kusto Query Language (KQL): a burst of failed sign-ins and a low-volume source-IP hunting query. The repository includes synthetic fixtures, deterministic Python reference tests, and analyst guidance.

## Safety and scope
Use a dedicated non-production Log Analytics workspace and synthetic events only. The checked-in fixture uses `example.invalid` identities and RFC 5737 documentation IP ranges. Never upload customer logs, credentials, personal data, or production incident records. Sentinel ingestion and retention may incur charges.

## Data source and schema
The queries assume the Microsoft Entra ID `SigninLogs` table is populated by the appropriate connector. Confirm the table and field types in the target workspace before deployment. In particular, confirm that `ResultType` is represented as a string and that `UserPrincipalName`, `IPAddress`, and `TimeGenerated` are available. The local tests validate the query contract and an equivalent reference calculation; they do **not** compile or execute KQL.

## Detection 1: failed-sign-in burst
File: `queries/failed-signins.kql`

- Hypothesis: five or more failed sign-ins for one user from one IP within the same 15-minute bucket may indicate password spraying or brute-force activity.
- Lookback: 24 hours; aggregation: user, source IP, 15-minute bucket; threshold: at least five failures.
- ATT&CK mapping: MITRE ATT&CK `T1110` (Brute Force). This is a starting hypothesis, not proof of compromise.
- Suggested scheduled rule: run every 5 minutes with a 1-day query period, then tune threshold, exclusions, severity and incident grouping against a known baseline.
- Investigation: review user risk, MFA outcomes, device/location context, successful sign-ins after the burst, and whether the source is a known corporate egress or identity provider.

## Hunting query: low-volume source IPs
File: `queries/rare-ip-signins.kql`

This returns IPs with one to three sign-in events in seven days. Low volume alone is not malicious. Use it as a hunting pivot alongside unfamiliar geography, user novelty, threat intelligence, device state, or impossible-travel context. It is deliberately not presented as a standalone high-confidence alert.

## Reproduce local tests
From this directory, with Python 3.10+:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

The tests check expected KQL clauses and compare the detections with a small deterministic synthetic dataset. They are regression tests for the intended query contract, not a Kusto parser or Sentinel integration test.

## Validate in Microsoft Sentinel
1. Select a dedicated test Log Analytics workspace and enable Microsoft Sentinel.
2. Enable the Microsoft Entra ID connector and confirm `SigninLogs` receives the required fields.
3. Run each query in Logs. If the workspace schema differs, adapt the query and record the connector/table mapping.
4. For the failed-sign-in query, create a scheduled analytics rule with a five-minute frequency and one-day lookup period. Map `UserPrincipalName` and `IPAddress` to the supported account/IP entities.
5. Keep the low-volume IP query as a hunting query until corroborating signals and a defensible alert threshold exist.
6. Generate only synthetic sign-in events in the test tenant, verify the expected rows, then tune false positives and document the outcome.
7. Record workspace region, connector version, rule ID, query execution time and test evidence without publishing tenant IDs or user data.

## Detection engineering checklist
- [ ] Confirm the table and field types in the target workspace.
- [ ] Run KQL in Logs and save the successful query result/evidence.
- [ ] Validate time windows, aggregation bins and threshold boundaries.
- [ ] Establish a baseline and document exclusions.
- [ ] Configure entity mappings and incident grouping.
- [ ] Tune severity and suppression to avoid alert fatigue.
- [ ] Document false positives, response steps and query cost.

## Remaining cloud-only validation
A real Sentinel workspace, connector configuration, ingestion of synthetic Entra sign-in events and analytics-rule execution are required to prove live KQL behaviour. Those steps are intentionally not automated here and require an authorized Azure test tenant and explicit cost approval.
