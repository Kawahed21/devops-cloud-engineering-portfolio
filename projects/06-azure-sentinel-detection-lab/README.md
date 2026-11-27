# 06: Azure Sentinel Detection Lab

## Objective
Practise cloud security monitoring with Microsoft Sentinel and Kusto Query Language (KQL), using synthetic events and documented detection logic.

## Lab safety
Use a dedicated non-production Log Analytics workspace and synthetic data. Do not upload customer logs, credentials, personal data or production incident records. Sentinel ingestion and retention may incur charges.

## Lab workflow
1. Create or select a dedicated test Log Analytics workspace.
2. Enable Microsoft Sentinel for the workspace.
3. Identify the data tables available in the selected connector.
4. Ingest synthetic events using a supported test method.
5. Write and validate KQL queries against the actual table schema.
6. Convert validated queries into scheduled analytics rules.
7. Configure severity, entity mapping, incident grouping and suppression.
8. Test incidents and document false-positive handling.

## Example KQL pattern
The following is a schema-neutral illustration. Replace table and column names with those present in your workspace.

```kusto
// Inspect recent records in a table after confirming its name.
SecurityEvent
| where TimeGenerated > ago(24h)
| take 50
```

Example failed sign-in investigation (table/fields depend on connector):
```kusto
SigninLogs
| where TimeGenerated > ago(1d)
| where ResultType != "0"
| summarize FailedAttempts=count() by UserPrincipalName, IPAddress, bin(TimeGenerated, 15m)
| where FailedAttempts >= 5
| order by FailedAttempts desc
```

## Detection engineering checklist
- [ ] State the threat hypothesis and expected attacker behaviour.
- [ ] Confirm source table and field semantics.
- [ ] Establish a baseline and tune thresholds.
- [ ] Exclude known test identities only with documented justification.
- [ ] Map user, host and IP entities where supported.
- [ ] Assign severity based on impact and confidence.
- [ ] Include investigation steps and response guidance.
- [ ] Test query cost and execution frequency.

## Deliverables
KQL query files, analytics-rule documentation, synthetic event examples, test cases, investigation runbooks and tuning notes.

## Next improvements
Add MITRE ATT&CK mapping, watchlists, automation rules, Logic Apps playbooks and detection-as-code deployment.
