# Phase 2 Implementation Plan: Code Review Remediation

Ordered by priority. Items 1–4 are **submission blockers**; 5–7 are quick hygiene; 8–9 are polish.

---

## 2. `nimbuskart-janitor/constants.py` — Pricing constants

Create pricing module and wire into report/summary:

- Per-unit costs: `EC2_T3_MICRO_HOURLY`, `EBS_GP2_GB_MONTHLY`, `EIP_HOURLY`
- Function `estimate_monthly_waste(resources)` returning `{total_usd, by_type}`
- Add `estimated_monthly_waste_usd` to `report.json`
- Add waste `$` column to `summary.md` tables

**Files:** `nimbuskart-janitor/constants.py` (new), `nimbuskart-janitor/janitor.py` (edit)

---

## 3. Missing-tags detection

Assignment §4.1 item 4 requires flagging resources missing mandatory tags.

- Define `REQUIRED_TAGS = {"Project", "Environment", "Owner", "ManagedBy"}`
- Add `missing_tags` key to each resource in filter output
- Add `untagged` resource list to report and summary

**Files:** `nimbuskart-janitor/janitor.py` (edit)

---

## 4. Tests — `nimbuskart-janitor/tests/test_janitor.py`

Unit tests for core functions:

| Test | What it covers |
|------|---------------|
| `test_tags_to_dict` | Empty, single, multi tag lists |
| `test_is_protected` | True/False/absent/mixed case |
| `test_parse_stop_time` | Valid GMT, invalid, None |
| `test_filter_resources_state` | Mock data: stopped EC2, available EBS, unassociated EIP, protected skips |
| `test_is_stopped_long_enough` | Boundary: exactly N days, < N days, no stop time |

**Files:** `nimbuskart-janitor/tests/__init__.py` (new), `nimbuskart-janitor/tests/test_janitor.py` (new)

---

## 5. `--markdown` flag bug fix

Current: `action="store_true", default=True"` → can never disable markdown.

Fix: rename to `--no-markdown` with `action="store_false", dest="markdown", default=True`.

Alternatively: rename CLI flag to `--summary` (more intuitive) and update README accordingly.

**Files:** `nimbuskart-janitor/janitor.py` (edit), `README.md` (edit)

---

## 6. Quickstart fix in README

Line 105 shows `--summary` but CLI uses `--markdown`. Fix the command. Also sync Python version (3.14 not 3.10).

**Files:** `README.md` (edit)

---

## 7. Cleanup sweep

| Task | Details |
|------|---------|
| Remove `main.py` | Dead code stub |
| Expand `.gitignore` | Add `.venv/`, `report.json`, `summary.md`, `.terraform/`, `.terraform.lock.hcl`, `__pycache__/`, `*.pyc` |
| Trim trailing blank lines | `terraform/main.tf`, `terraform/Modules/Network/main.tf`, `janitor.py` |
| Add `Size` to EBS scan output | So summary table isn't empty |

**Files:** `main.py` (delete), `.gitignore` (edit), `janitor.py` (edit), `terraform/main.tf` (edit), `terraform/Modules/Network/main.tf` (edit)

---

## 8. Pagination (recommended)

Add `NextToken` loop to `describe_instances()`, `describe_volumes()`, `describe_addresses()` so scan works on real AWS accounts.

**Files:** `nimbuskart-janitor/janitor.py` (edit)

---

## 9. Validation sweep

```bash
terraform fmt -recursive
terraform validate
pytest nimbuskart-janitor/tests/
python nimbuskart-janitor/janitor.py --help
python nimbuskart-janitor/janitor.py --dry-run --markdown
```

**Files:** none (commands to run)





















