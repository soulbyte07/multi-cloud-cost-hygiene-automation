# Execution Plan: Multi-Cloud Cost Hygiene & Automation Challenge

This plan outlines the step-by-step process to complete the DevOps Engineer assignment for NimbusKart.

## Phase 1: Environment Setup & Initialization
- [x] **1.1 Docker & LocalStack:** Ensure Docker is running. Start LocalStack using the provided docker run command.
- [x] **1.2 Repository Structure:** Initialize the Git repository and create the required directory layout:
    ```
    ├── terraform/
    │   └── modules/network/
    ├── janitor/
    │   └── tests/
    ├── .github/workflows/
    ├── docs/
    └── samples/
    ```
- [x] **1.3 Dependencies:** Create `janitor/requirements.txt` with `boto3`, `pytest`, and any CLI frameworks (e.g., `click`).

## Phase 2: Part A - Infrastructure as Code (Terraform)
- [x] **2.1 Network Module:** Develop a reusable module for VPC, two public subnets, and security groups.
    *   *Note:* Address the security group "judgment call" (port 22 exposure).
- [x] **2.2 Baseline Resources:** Define EC2 instances, S3 bucket (with lifecycle rules), and the intentional orphan EBS volume in `terraform/main.tf`.
- [x] **2.3 Tagging Policy:** Implement a consistent tagging map to be applied to all resources (Project, Environment, Owner, ManagedBy).
- [x] **2.4 Validation:** Run `terraform fmt` and `terraform validate`. Verify deployment against LocalStack using `tflocal`.

## Phase 3: Part B - "Cost Janitor" Scripting
- [ ] **3.1 Scaffolding:** Create `janitor/janitor.py` with argument parsing (`--dry-run`, `--delete`, `--days`).
- [ ] **3.2 Core Logic - Orphan Detection:** Implement functions to detect:
    *   Unattached EBS volumes.
    *   Stopped EC2 instances (> N days).
    *   Unassociated Elastic IPs.
    *   Resources missing mandatory tags.
- [ ] **3.3 Pricing & Calculations:** Create `janitor/constants.py` with per-unit pricing to calculate estimated monthly waste.
- [ ] **3.4 Output Generation:** Implement JSON reporting (matching the required schema) and a Markdown summary generator.
- [ ] **3.5 Safety Features:** Implement the `Protected=true` tag check to skip deletion.

## Phase 4: Part B - CI/CD Wiring
- [ ] **4.1 GitHub Action:** Create `.github/workflows/cost-janitor.yml`.
    *   Configure LocalStack as a service container.
    *   Setup Python and Terraform environments.
    *   Execute Terraform apply -> Run Janitor (dry-run) -> Upload Artifacts.
- [ ] **4.2 PR Automation:** Add logic to post the Markdown summary as a comment on the Pull Request.

## Phase 5: Part C - Design & Documentation
- [ ] **5.1 DESIGN.md:** Draft the design note covering:
    *   Multi-cloud restructuring (GCP/Azure).
    *   Minimal IAM policies.
    *   Safety guardrails and failure modes.
    *   Observability metrics and alerting.
- [ ] **5.2 README.md:** Populate all required sections including "Decisions & deviations" and "Trade-offs".
- [ ] **5.3 SUBMISSION.md:** Complete the fixed-format index.

## Phase 6: Finalization & Submission
- [ ] **6.1 Quality Check:** Verify all "Automatic Disqualifiers" are avoided (init works, no crashes, git history cadence).
- [ ] **6.2 Walkthrough Video:** Record a <5 min demo covering the required points (LocalStack start, Janitor run, design pride, future change).
- [ ] **6.3 Final Polish:** Ensure `terraform fmt` and `terraform validate` pass across the board.
- [ ] **6.4 Submission:** Push to public GitHub and send the URL/Video link.
