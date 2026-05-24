<a id="readme"></a>
<div align="center">
  <h1>Multi-Cloud Cost Hygiene Automation</h1>
  <p>Detect and clean idle cloud resources with LocalStack, Terraform, and a janitor CLI.</p>
  <p>
    <img alt="License" src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" />
    <img alt="CI" src="https://img.shields.io/github/actions/workflow/status/USER/REPO/cost-janitor.yml?style=flat-square" />
    <img alt="Coverage" src="https://img.shields.io/codecov/c/github/USER/REPO?style=flat-square" />
  </p>
</div>

<a id="toc"></a>
## Table of Contents
- [Description](#description)
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Roadmap](#roadmap)
- [FAQ](#faq)
- [License](#license)

<a id="description"></a>
## Description
This project provides a local-first workflow to detect and clean up cost-wasting resources using LocalStack for AWS emulation, Terraform for baseline infra, and a Python janitor CLI for discovery and cleanup. It is built for the NimbusKart scenario and is designed to be extended to multi-cloud cost hygiene. Current status: LocalStack setup, Terraform baseline, and janitor script are implemented; CI/CD and tests are pending, and janitor testing is in progress.

[⬆ back to top](#readme)

<a id="features"></a>
## Features
- LocalStack-ready Terraform stack (VPC, public subnets, EC2, S3 logs, orphan EBS)
- Consistent resource tagging (Project, Environment, Owner, ManagedBy)
- Janitor CLI for detecting stopped instances, unattached volumes, and unassociated EIPs
- Safe deletion controls with `Protected=true` tag enforcement
- JSON report output for auditability

[⬆ back to top](#readme)

<a id="installation"></a>
## Installation
**Prerequisites**
- Docker (for LocalStack)
- Terraform 1.5+
- Python 3.10+

**Steps**
1. Clone the repository.
2. Start LocalStack:
   ```bash
   docker run --rm -it -p 4566:4566 localstack/localstack
   ```
3. Set local AWS credentials (LocalStack defaults):
   ```bash
   export AWS_ACCESS_KEY_ID=test
   export AWS_SECRET_ACCESS_KEY=test
   export AWS_DEFAULT_REGION=us-east-1
   ```
4. Install Python dependencies for the janitor CLI:
   ```bash
   pip install -r nimbuskart-janitor/requirements.txt
   ```

[⬆ back to top](#readme)

<a id="usage"></a>
## Usage
### Apply Terraform baseline
```bash
cd terraform
tflocal init
tflocal apply
```

### Run janitor in dry-run mode (default)
```bash
python nimbuskart-janitor/janitor.py --dry-run
```

### Delete flagged resources
```bash
python nimbuskart-janitor/janitor.py --delete
```

[⬆ back to top](#readme)

<a id="configuration"></a>
## Configuration
### Terraform variables
| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `region` | string | `us-east-1` | AWS region (LocalStack default). |
| `project` | string | `NimbusKart` | Project tag value. |
| `environment` | string | `dev` | Environment tag value. |
| `owner` | string | `cost-hygiene` | Owner tag value. |
| `vpc_cidr` | string | `10.20.0.0/16` | VPC CIDR block. |
| `public_subnet_cidrs` | list(string) | `10.20.1.0/24,10.20.2.0/24` | Public subnet CIDRs. |
| `azs` | list(string) | `us-east-1a,us-east-1b` | Availability zones. |
| `ssh_cidr` | string | `0.0.0.0/0` | CIDR allowed for SSH. |
| `instance_type` | string | `t3.micro` | EC2 instance type. |
| `instance_count` | number | `2` | Web tier instance count. |
| `ami_id` | string | `ami-12345678` | AMI ID placeholder for LocalStack. |
| `logs_bucket_name` | string | `nimbuskart-logs` | S3 logs bucket name. |
| `orphan_volume_size` | number | `8` | Unattached EBS size (GiB). |

### Janitor CLI flags
| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `--dry-run` | boolean | `true` | Scan and generate `report.json` without deletions. |
| `--delete` | boolean | `false` | Delete resources listed in `report.json`. |
| `--days` | integer | `14` | Minimum stopped days for EC2 cleanup. |

[⬆ back to top](#readme)

<a id="api-reference"></a>
## API Reference
### `janitor.py`
```
python nimbuskart-janitor/janitor.py --dry-run
python nimbuskart-janitor/janitor.py --delete --days 30
```
Detects and optionally deletes cost-wasting resources based on the configured thresholds and safety rules.

[⬆ back to top](#readme)

<a id="roadmap"></a>
## Roadmap
- [ ] Add GitHub Actions CI/CD (LocalStack + Terraform apply + janitor dry-run)
- [ ] Implement janitor tests and fix LocalStack test harness
- [ ] Publish report schema and Markdown summary output
- [ ] Add multi-cloud abstraction for GCP/Azure scanners

[⬆ back to top](#readme)

<a id="faq"></a>
## FAQ
### Why does the janitor not delete protected resources?
Resources tagged with `Protected=true` are always skipped to reduce the risk of accidental outages.

### Why am I stuck on janitor tests?
The test harness and LocalStack fixtures are not wired yet. The roadmap includes a dedicated step to build test scaffolding and reliable LocalStack execution.

### Can this run against real AWS?
Yes, but you must provide valid AWS credentials and carefully review the `--delete` output before running destructive actions.

[⬆ back to top](#readme)

<a id="license"></a>
## License
MIT. See `LICENSE` for details.

[⬆ back to top](#readme)
