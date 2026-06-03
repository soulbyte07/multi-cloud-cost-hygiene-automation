# Multi-Cloud Cost Hygiene Automation

NimbusKart assignment project for detecting and cleaning cloud waste using LocalStack, Terraform, and a Python janitor CLI.

## Repository Layout

```text
.
├── .github
│   └── workflows
│       └── cost-janitor.yml            # CI: LocalStack + Terraform + dry-run report
├── .gitignore
├── DESIGN.md                           # Part C design note
├── README.md
├── nimbuskart-janitor                  # Part B: janitor CLI
│   ├── README.md
│   ├── janitor.py
│   ├── main.py
│   ├── pyproject.toml
│   ├── report.json
│   ├── requirements.txt
│   ├── summary.md
│   └── uv.lock
└── terraform                           # Part A: IaC for baseline AWS resources
    ├── Modules
    │   └── Network
    │       ├── main.tf
    │       ├── output.tf
    │       └── variables.tf
    ├── main.tf
    ├── outputs.tf
    └── variables.tf

6 directories, 25 files

```

## What This Builds

- VPC (`10.20.0.0/16`) with two public subnets and internet routing.
- Security group allowing 80/443 and configurable SSH CIDR.
- Two `t3.micro` EC2 instances (web tier tags).
- S3 logs bucket with versioning.
- One unattached EBS volume for janitor detection testing.

## Architecture (Current)

```text
LocalStack (4566)
  ^
  |  tflocal apply
  |
Terraform root stack ---> Network module (VPC/Subnets/SG)
  |
  +--> EC2 instances
  +--> S3 logs bucket
  `--> Unattached EBS

janitor.py --dry-run/--delete ---> EC2 APIs (instances/volumes/addresses)
                               ---> report.json + summary.md
```

## Prerequisites

- Docker
- Python `3.14+` (source of truth: `nimbuskart-janitor/pyproject.toml`)
- Terraform `1.5+`
- `terraform-local` (`tflocal`)

## Quickstart (Local)

1. Start LocalStack:

```bash
docker run --rm -it -p 4566:4566 localstack/localstack
```

2. Export LocalStack AWS environment variables:

```bash
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=http://localhost:4566
```

3. Install tools:

```bash
pip install terraform-local
pip install -r nimbuskart-janitor/requirements.txt
```

4. Apply Terraform baseline (same pattern used by CI):

```bash
tflocal -chdir=terraform init
tflocal -chdir=terraform validate
tflocal -chdir=terraform apply -auto-approve -var="enable_s3_lifecycle=false"
```

5. Run janitor dry-run:

```bash
python nimbuskart-janitor/janitor.py --dry-run --summary
```

6. Optional delete mode:

```bash
python nimbuskart-janitor/janitor.py --delete
```

## Janitor Behavior

- Detects:
  - unattached EBS volumes (`available`)
  - stopped EC2 instances older than `--days` (default `14`)
  - unassociated Elastic IPs
- Deletion safety: resources tagged `Protected=true` are skipped.
- Outputs are always written to repo root:
  - `report.json`
  - `summary.md`

## CI/CD Workflow

Workflow: `.github/workflows/cost-janitor.yml`

Execution order:
1. Start LocalStack service container.
2. `tflocal fmt -check -diff`
3. `tflocal init`
4. `tflocal validate`
5. `tflocal apply -auto-approve -var="enable_s3_lifecycle=false"`
6. `python nimbuskart-janitor/janitor.py --dry-run`
7. Upload `report.json` and `summary.md` artifacts.
8. Post `summary.md` as PR comment.

## Decisions & Deviations

- **LocalStack-first provider wiring:** Terraform provider endpoints in `terraform/main.tf` are hardcoded to `http://localhost:4566` with test credentials to guarantee local reproducibility.
- **S3 lifecycle disabled in CI apply:** CI passes `-var="enable_s3_lifecycle=false"` due to LocalStack lifecycle compatibility issues; Terraform still supports enabling it.
- **CLI flag behavior differs from assignment wording:** assignment says dry-run default, but implementation currently requires explicit `--dry-run` or `--delete` and exits otherwise.
- **Python runtime bumped to 3.14:** `pyproject.toml` and CI use `3.14`, which is stricter than assignment's 3.10+ guidance.
- **Single-file janitor implementation:** `nimbuskart-janitor/janitor.py` intentionally keeps scanning, filtering, reporting, and delete logic together for assignment speed; `DESIGN.md` defines the modular multi-cloud path.

## Trade-offs

- **Fast delivery vs modularity:** single-file janitor is quicker to reason about for this assignment, but less extensible than an adapter-based design.
- **Reproducibility vs production realism:** hardcoded LocalStack endpoints simplify setup but make current Terraform unsafe for direct real-AWS use without edits.
- **Safety vs aggressive cleanup:** `Protected=true` checks and explicit delete mode reduce outage risk but may leave some waste uncleaned.
- **CI stability vs feature completeness:** disabling S3 lifecycle in CI avoids flaky failures in emulation at the cost of not continuously validating lifecycle behavior.

## Validation Commands

```bash
tflocal -chdir=terraform fmt -check -diff
tflocal -chdir=terraform validate
python nimbuskart-janitor/janitor.py --dry-run --summary
```























