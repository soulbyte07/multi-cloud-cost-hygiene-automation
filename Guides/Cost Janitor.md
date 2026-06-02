## 1. Project Architecture

Instead of one massive file, I recommend a functional structure to keep the code clean and testable.

### Functional Categories

* **The Scanner:** Functions that use `boto3` clients to describe resources (EC2, EBS, EIP).
* **The Filter:** Logic to check for "waste" criteria (e.g., `state == 'stopped'`, `AttachmentSet == []`).
* **The Reporter:** Logic to aggregate findings into the required `report.json` and Markdown formats.
* **The Executor:** Logic that handles the `--dry-run` vs `--delete` logic.

---

## 2. Detection Logic Strategies

For each resource type, you'll need a specific filtering strategy.

### Resource Filtering Table

| Resource | Boto3 Method | Waste Condition |
| --- | --- | --- |
| **EBS Volumes** | `ec2.describe_volumes()` | `State == 'available'` (means unattached). |
| **EC2 Instances** | `ec2.describe_instances()` | `State == 'stopped'` AND `LaunchTime` vs Current Time. |
| **Elastic IPs** | `ec2.describe_addresses()` | `InstanceId` or `NetworkInterfaceId` is missing/null. |
| **Tagging** | All of the above | Check `Tags` list for your 4 mandatory keys. |

---

## 3. Implementation Steps

### Step 1: Handle Configuration & CLI

Use the `argparse` library to handle your flags.

* Define `--dry-run` with `action="store_true"` and set it as the default.
* Define `--delete` as a separate flag.
* Define an argument for the "N days" threshold for stopped instances.

### Step 2: The Safety Engine

Before any deletion logic is executed, create a **Safety Gate** function.

1. **Tag Check:** Scan the resource's tags for `Protected=true`.
2. **Logic:** If the tag exists, the resource is immediately removed from the "To Delete" list and moved to a "Skipped" list in your report.
3. **Flag Check:** Even if a resource isn't protected, only call `.delete()` or `.terminate()` if `args.delete` is True.

### Step 3: LocalStack Compatibility

Since this runs against LocalStack, your `boto3` client initialization needs an `endpoint_url`.

> **Pro-Tip:** Use an environment variable (like `LOCALSTACK_ENDPOINT_URL`) to toggle between LocalStack for dev and real AWS for production.

---

## 4. Generating the Outputs

### The JSON Report

Initialize a dictionary at the start of your script. As you find orphaned resources, append them to a list grouped by type:

```json
{
  "orphaned_ebs": [...],
  "stopped_ec2": [...],
  "unassociated_eip": [...],
  "untagged_resources": [...]
}

```

### The Markdown Summary

This is what gets posted as a PR comment. Focus on high-level impact:

* **Total Savings (Estimated):** Use dummy values for now (e.g., $X/month saved).
* **Count:** "Found 3 unattached volumes."
* **Action Taken:** "Dry-run mode: No resources were harmed."

---

## 5. Potential Pitfalls to Watch For

* **Pagination:** If NimbusKart grows, `describe_instances` only returns the first page. For the assignment, standard calls are fine, but mentioning `Paginators` in your `DESIGN.md` shows senior-level thinking.
* **Date Comparisons:** `LaunchTime` from AWS is timezone-aware. Make sure your "N days" calculation uses `timezone.utc` to avoid "offset-naive vs offset-aware" errors.
* **Missing Tags:** If a resource has *no* tags at all, the `Tags` key might not even exist in the Boto3 response. Always use `.get('Tags', [])` to avoid `KeyError`.






















