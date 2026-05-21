# DevOps Engineer Assignment: Multi-Cloud Cost Hygiene & Automation Challenge

* **Company:** Code & Conscience [cite: 1, 8]
* **Role:** DevOps Engineer [cite: 2]
* **Time Budget:** 6-10 hours over up to 5 calendar days [cite: 5]
* **Cost:** Zero (Uses LocalStack, Docker, and Open Source tools) [cite: 5]

---

## 1. Context
Code & Conscience is launching a business vertical focused on cost optimization for cloud and AI infrastructure[cite: 8]. As AI workloads and multi-cloud sprawl increase, clients are losing money on idle or orphaned resources[cite: 9]. This role involves building automation to find, fix, and prevent such waste[cite: 10, 11].

**The Scenario:** You are working for a fictional client, **NimbusKart**, whose AWS bill grew from \$400 to \$2,100/month due to orphaned resources[cite: 14, 15, 16]. Your goal is to build a foundation to manage this waste using local tooling[cite: 17].

---

## 2. Deliverables at a Glance
| Part | Deliverable | What it Proves |
| :--- | :--- | :--- |
| **A** | Terraform stack for baseline infra (VPC, EC2, S3) [cite: 20] | Ability to write modular, tagged, and clean IaC [cite: 20] |
| **B** | "Cost Janitor" script (Python/Bash) + GitHub Actions [cite: 20] | Ability to automate waste detection and integrate with CI/CD [cite: 20] |
| **C** | Design Note (Max 2 pages) [cite: 20] | Ability to think about security, scaling, and multi-cloud production [cite: 20] |

---

## 3. Part A: Infrastructure as Code (Terraform)
Write Terraform configuration to run against **LocalStack**[cite: 24].

### 3.1 Resources to Create
* **VPC:** `10.20.0.0/16` with two public subnets in two AZs[cite: 26].
* **Security Group:** Inbound 80/443 (anywhere) and 22 (configurable CIDR)[cite: 27].
* **EC2:** Two `t3.micro` instances tagged as "web tier"[cite: 28].
* **S3:** Bucket for logs, versioning enabled, 30-day lifecycle rule for non-current versions[cite: 29].
* **EBS:** One unattached volume (to be used as an "orphan" for Part B)[cite: 30].

### 3.2 Conventions
* **Modular:** Use at least one reusable module (e.g., network)[cite: 32].
* **Tagging:** Every resource must have: `Project`, `Environment`, `Owner`, and `ManagedBy: terraform`[cite: 34].
* **Variables:** Use `variables.tf` (no hard-coding); provide `outputs.tf` for VPC ID, subnets, and bucket name[cite: 35, 36].
* **Validation:** Must pass `terraform fmt` and `terraform validate`[cite: 37].

---

## 4. Part B: The "Cost Janitor" Automation
Build a script to scan the environment and report wasteful resources[cite: 55].

### 4.1 Requirements
* **Language:** Python 3.10+ (preferred) or Bash[cite: 58].
* **Detection Patterns:**
    1.  Available (unattached) EBS volumes[cite: 60].
    2.  Stopped EC2 instances (> N days, default 14)[cite: 61].
    3.  Unassociated Elastic IPs[cite: 62].
    4.  Resources missing required tags[cite: 63].
* **Flags:** Must support `--dry-run` (default) and `--delete`[cite: 65].
* **Safety:** `--delete` must skip resources tagged `Protected=true`[cite: 66].
* **Output:** A `report.json` (specific schema required) and a Markdown summary[cite: 64, 78].

### 4.2 CI/CD (GitHub Actions)
The workflow must[cite: 69, 70, 71, 72, 73, 74]:
1.  Spin up LocalStack.
2.  Apply Part A Terraform.
3.  Run Janitor in `--dry-run`.
4.  Upload reports as artifacts and post the Markdown summary as a PR comment.

---

## 5. Part C: Design Note (`DESIGN.md`)
Address the following in a specific, opinionated document[cite: 102, 103]:
* **Multi-cloud:** How to add GCP/Azure without rewriting the core[cite: 105].
* **Permissions:** Minimal IAM policy (JSON) for read-only mode[cite: 107, 108].
* **Safety:** Describe two failure modes where auto-deletion causes an outage and suggest guardrails[cite: 109].
* **Observability:** List 3-5 metrics with sources and alert thresholds[cite: 110, 111].

---

## 6. Submission Guidelines
### 6.1 Repository Structure
Your repository must follow this exact layout[cite: 118, 119]:
```text
your-repo/
├── terraform/          # IaC files
├── janitor/            # Script, requirements, constants
├── .github/workflows/  # CI/CD
├── README.md           # Overview, run commands, diagram, decisions
├── SUBMISSION.md       # Fixed-format checklist and links
└── DESIGN.md           # Part C document

```

### 6.2 Mandatory Components

* 
**Walkthrough Video:** A max 5-minute screen capture applying Terraform and walking through code/decisions.


* 
**AI Disclosure:** Honestly document tools used (e.g., ChatGPT/Copilot), what they got wrong, and what you wrote manually.



### 6.3 Evaluation & Disqualifiers

Submissions are scored on Terraform structure (20), Janitor quality (20), CI/CD (15), Design (15), and Documentation (10).
**Disqualifiers include:** failing to initialize, missing video, identical copy-pasted code, or poor git history (1-2 total commits).

```

```
