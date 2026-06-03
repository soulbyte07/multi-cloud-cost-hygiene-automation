# Cost Janitor Report

**Timestamp:** 2026-06-03 06:10:51 UTC  
**Mode:** dry-run  
**Stopped Threshold:** 14 days  

## Summary

| Resource Type | Count |
|---|---|
| Stopped EC2 (>14d) | 0 |
| Unattached EBS | 1 |
| Unassociated EIP | 0 |
| **Total wasteful** | **1** |

## Unattached EBS Volumes

| VolumeId | Size | Created | Tags |
|---|---|---|---|
| vol-7875b0b587a5b6f7b |  | 2026-06-03 | Environment=dev, ManagedBy=terraform, Name=nimbuskart-ebs_volume-1, Owner=cost-hygiene, Project=NimbusKart, Tier=ebs_volume |

