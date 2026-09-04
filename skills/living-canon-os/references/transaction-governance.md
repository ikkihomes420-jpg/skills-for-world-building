# Transaction Governance

Use transactions for any material canon or project-memory update: creating a consequential record, changing an approved fact, deprecating material, redirecting an identity, changing a rule, resolving a major state transition, or importing a source-backed decision. A transaction is the reviewable bridge between conversation and durable canon.

## Lifecycle

| Status | Meaning | Permitted action |
|---|---|---|
| `proposed` | A draft capture exists but has not changed canon. | Review, reconcile, approve, reject. |
| `applied` | An approved transaction changed target records and created a session delta. | Query, audit, or guarded rollback. |
| `rejected` | The proposal was intentionally declined with a review note. | Retain as evidence; do not apply. |
| `reverted` | An applied transaction was safely reversed. | Retain as history; do not reapply directly. |

Every transaction must state a title, rationale, authority, branch, source locators, time of creation, and structured operations. The transaction itself is not canon; it documents the decision path that created or changed canon.

## Operation types

| Operation | Use for | Required safeguards |
|---|---|---|
| `create` | Add a new record. | Stable new ID; source/evidence; status appropriate to authority. |
| `update` | Change specific fields of an existing record. | Record prior values for every changed field; do not replace unrelated fields. |
| `deprecate` | Stop a record from driving future work while retaining history. | Record a successor when one exists; do not delete provenance. |
| `redirect` | Rename or redirect a stable identity to an existing replacement. | Confirm the replacement is the same canon subject, not merely similar. |

Use a `change-set` or a branch workflow for a high-impact split, merge, migration, or counterfactual. Do not disguise a large retcon as a routine update.

## Capture workflow

1. Extract only potentially durable candidates from the conversation.
2. Identify evidence and authority. A conversational mention is not automatically an approved decision.
3. Compare candidates with aliases, current records, active rules, timeline, relationships, and branches.
4. Draft operations with exact before/after values.
5. Create a `proposed` transaction with `capture_transaction.py`.
6. Render it with `review_transaction.py` in reader view.
7. Ask for approval whenever the capture policy or change impact requires it.
8. Apply with `apply_transaction.py` only after approval. Validate and rebuild the snapshot afterward.

## Review standard

A review should make four distinctions visible: **what changes**, **why it changes**, **what supports it**, and **what it could affect**. Do not ask a user to approve raw YAML without a human-readable diff. Flag a draft as stale when the records it expected have changed since proposal.

For a material canon change, include a short impact note and at least two integration or repair options when there is a real choice. A fast approval is appropriate for low-risk factual capture only when the project’s manifest explicitly permits it.

## Reversal standard

Rollback is intentionally guarded. It should restore only records whose last change was the transaction being reversed. If a later transaction changed a target, stop and require a new reconciliation transaction rather than overwriting newer history. Never delete the transaction, its source locators, or its session delta.

## Transaction input shape

```yaml
title: Formalize reserve repayment pressure
rationale: Record the repayment mechanism and its political consequence.
authority: assistant-proposed
branch: mainline
source_locators:
  - conversation:session-002#turn-18
operations:
  - op: update
    target_id: entity.reed-compact
    set:
      attributes.current_priority: Secure a repayment framework.
```

The tools materialize the prior values when the proposal is captured. A proposed update is not a hidden edit; it is an explicit candidate for the author’s decision.

## Fingerprint safeguard

When a transaction is drafted, each existing target stores a baseline fingerprint of its canonical content. Review and approval compare the current target against that fingerprint, so a transaction becomes stale if **any** target field changes—not only a field the transaction intended to edit. After application, each affected record stores the applying transaction and a post-application fingerprint.

Rollback performs a full preflight across every target before changing any file. It proceeds only when each record still identifies the transaction as its last governed change and still matches its post-application fingerprint. If any target was changed afterward, the entire rollback stops and a new reconciliation transaction is required. This prevents partial reversal and protects later author work from an unsafe overwrite.
