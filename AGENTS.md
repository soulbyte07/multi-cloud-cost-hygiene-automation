# AGENTS.md

## Quick Orientation
- Core code lives in `nimbuskart-janitor/janitor.py`; `main.py` is a placeholder.
- Terraform is LocalStack-first: provider endpoints in `terraform/main.tf` are hardcoded to `http://localhost:4566` with test creds.

## Local Dev Commands (verified)
- Start LocalStack (from `README.md`): `docker run --rm -it -p 4566:4566 localstack/localstack`.
- Set AWS env for LocalStack (from `README.md`): `AWS_ACCESS_KEY_ID=test`, `AWS_SECRET_ACCESS_KEY=test`, `AWS_DEFAULT_REGION=us-east-1`.
- Terraform baseline (from `README.md`): `tflocal init` then `tflocal apply` in `terraform/`.
- Janitor dry-run: `python nimbuskart-janitor/janitor.py --dry-run`.
- Janitor delete: `python nimbuskart-janitor/janitor.py --delete` (reads `report.json`).

## Gotchas
- `janitor.py` uses a default `boto3.Session()` with no endpoint override; it will use whatever AWS credentials/profile/env are active.
- Deletion path requires `report.json` to exist; `--delete` fails if dry-run wasn’t run first.
- Python version mismatch: `nimbuskart-janitor/pyproject.toml` requires `>=3.14` while `README.md` says 3.10+; follow `pyproject.toml` when packaging or tooling is involved.
