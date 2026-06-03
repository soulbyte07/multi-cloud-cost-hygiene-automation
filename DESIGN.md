# DESIGN.md

## NimbusKart Cost Janitor Design Note

## 1) Multi-cloud restructuring (AWS now, GCP/Azure next)

### Current state
The current implementation is AWS-specific (`boto3` in `nimbuskart-janitor/janitor.py`) and directly couples:
- resource discovery
- waste rules
- report rendering
- delete execution

This works for the assignment but will not scale cleanly to GCP/Azure.

### Target architecture
Refactor into a provider-agnostic core with cloud adapters:

- `core/models.py`
  - Common resource model: `id`, `cloud`, `type`, `region`, `state`, `tags`, `created_at`, `metadata`
- `core/rules.py`
  - Rules independent of provider SDK:
  - `unattached_volume`
  - `stopped_compute_older_than_n_days`
  - `unassociated_public_ip`
  - `missing_required_tags`
- `core/engine.py`
  - Scans via adapter, applies rules, emits findings
- `core/reporter.py`
  - Writes `report.json` and `summary.md`
- `core/executor.py`
  - Handles `--dry-run` / `--delete`, idempotency and safety gates

- `providers/aws_adapter.py`
  - Uses `boto3` mapping AWS objects to canonical model
- `providers/gcp_adapter.py` (future)
  - Uses Google Cloud SDK mapping GCP resources
- `providers/azure_adapter.py` (future)
  - Uses Azure SDK mapping Azure resources

### Interface contract
Each provider adapter implements:
- `scan() -> list[Resource]`
- `delete(resource: Resource) -> DeleteResult`
- `supports(resource_type: str) -> bool`

This avoids rewriting core logic when adding cloud providers; only adapter mapping and cloud-specific delete calls change.

### Data normalization strategy
Normalize cloud-specific fields:
- compute instance states (`stopped`, `terminated`, etc.) mapped to canonical states
- timestamps converted to UTC before age checks
- tags/labels converted to a dictionary
- resource IDs preserved in metadata for audit/debug

### Rollout plan
1. Extract AWS code into adapter but keep behavior unchanged.
2. Add canonical model + rules engine.
3. Add provider selector (`--cloud aws|gcp|azure|all`, default `aws`).
4. Add GCP read-only scan adapter.
5. Add Azure read-only scan adapter.
6. Enable delete per provider only after integration tests and guardrails are validated.

---

## 2) Minimal IAM policies

Two permission modes are recommended.

### A. Read-only mode (default)
Use this for discovery and reporting.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "JanitorReadOnlyEC2",
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeVolumes",
        "ec2:DescribeAddresses",
        "ec2:DescribeTags"
      ],
      "Resource": "*"
    },
    {
      "Sid": "JanitorReadOnlyS3",
      "Effect": "Allow",
      "Action": [
        "s3:ListAllMyBuckets",
        "s3:GetBucketTagging",
        "s3:GetBucketLocation"
      ],
      "Resource": "*"
    }
  ]
}
```

### B. Delete mode (elevated, opt-in)
Attach only when cleanup is approved.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "JanitorDeleteEC2",
      "Effect": "Allow",
      "Action": [
        "ec2:TerminateInstances",
        "ec2:DeleteVolume",
        "ec2:ReleaseAddress"
      ],
      "Resource": "*"
    }
  ]
}
```

### IAM guardrails
- Separate roles for read-only and delete operations.
- Short-lived credentials for delete mode.
- Restrict delete role usage by CI branch/environment conditions.
- Log all delete API calls in CloudTrail and retain for audit.

---

## 3) Safety guardrails and failure modes

### Failure mode 1: false positive deletion of recoverable but intentionally stopped instances
Example: weekend shutdown policy for non-prod workers gets flagged by age threshold.

**Guardrails**
- Keep `--dry-run` as operational default in pipelines.
- Require `Protected=true` tag skip in delete path.
- Add allowlist tag gate: only delete when `JanitorEligible=true`.
- Enforce a minimum age + two-pass confirmation (resource must appear in 2 consecutive scans).

### Failure mode 2: deleting shared resources with hidden dependencies
Example: seemingly unattached EIP or volume still referenced by scripts, DNS, or pending workflows.

**Guardrails**
- Add pre-delete dependency checks where API supports it.
- Add cooldown window (`first_seen_waste_at + 24h`) before delete eligibility.
- Use staged execution:
  1) scan-only
  2) approve
  3) limited delete batch (max N resources per run)
- Persist deletion decisions and rollback hints in report artifacts.

### Additional operational guardrails
- Abort delete if scan completeness is suspicious (API errors, partial pages, low coverage).
- Idempotency keys in delete run to prevent duplicate cleanup attempts.
- Block delete in unknown account/region unless explicitly allowed by config.
- Emit a post-delete summary with counts of deleted, skipped, failed.

---

## 4) Observability metrics and alerting

Metrics should measure detection quality, safety, and runtime reliability.

| Metric | Source | Suggested Alert |
|---|---|---|
| `janitor_scan_duration_seconds` | script runtime / CI step timing | warn if > 2x 7-day baseline |
| `janitor_waste_resources_total{type}` | `report.json` counts per type | warn if +50% day-over-day |
| `janitor_estimated_monthly_waste_usd` | rule output + pricing constants | critical if > budget threshold (e.g., $500/mo dev, $2000/mo prod) |
| `janitor_delete_attempts_total` and `janitor_delete_failures_total` | delete executor logs | critical if failure rate > 5% per run |
| `janitor_protected_skips_total` | safety gate counters | warn if sudden drop to 0 (possible tag ingestion bug) |

### Alert routing
- CI comment on PR for every dry-run.
- Slack/Teams alert for threshold breaches.
- Ticket auto-create for persistent breach over 3 consecutive runs.

### Dashboards
- Time series of waste count and estimated savings.
- Delete success/failure by resource type.
- Safety outcomes: protected skips, policy denials, dependency blocks.

---

## 5) Trade-offs and deviations

- Current implementation is intentionally AWS-first for assignment scope and LocalStack reproducibility.
- Lifecycle behavior in LocalStack may differ from real AWS; CI already disables S3 lifecycle during apply to avoid false negatives.
- Multi-cloud support is designed as an adapter extension, not a full rewrite.
- Deletion is intentionally conservative; lower immediate savings is acceptable to reduce outage risk.

---

## 6) Next concrete implementation steps

1. Extract AWS scan/delete code into `providers/aws_adapter.py` without changing outputs.
2. Introduce canonical `Resource` model and move rules into `core/rules.py`.
3. Add `JanitorEligible=true` gate and two-pass confirmation before delete.
4. Add metrics emitter (JSON logs first; Prometheus/OpenTelemetry later).
5. Add integration tests for safety guardrails in LocalStack.
