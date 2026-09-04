# Integrity, Branches, and Reader Views

Use this reference for semantic audits, alternate timelines, migrations, counterfactuals, and human-readable exports. These controls make large archives safer to change and easier to use without turning automated analysis into authorial authority.

## Integrity audit

Run `audit_invariants.py` after a major transaction, migration, import, release, or continuity concern. The current checks detect duplicate entity-like labels in a branch, mainline references to non-mainline records, impossible ISO relationship ranges, missing knowledge holders, underspecified rule exceptions, and inferred transitions without a choice boundary.

Treat a finding as a question with evidence, not a command. Use this interpretation standard:

| Finding | Meaning | Appropriate response |
|---|---|---|
| `duplicate-identity` | Two active records may represent one entity or need clearer distinction. | Compare aliases and roles; merge only by deliberate decision. |
| `branch-leak` | Mainline records directly depend on branch-only material. | Move the dependency, create a mainline counterpart, or propose a merge. |
| `invalid-validity-range` | A relationship date range is internally impossible. | Correct dates or preserve uncertainty. |
| `unknown-knowledge-holder` | A knowledge record references an absent holder. | Add/correct the holder or intentionally leave it textual. |
| `underspecified-exception` | A rule exception could become an unlimited loophole. | Define scope, mechanism, cost, and evidence. |
| `missing-choice-boundary` | An inferred state advance may have taken a choice the user/player should retain. | Add a boundary or explicitly approve the resolution. |

The audit writes a reader report to `audit/latest-invariant-audit.md`. Persist selected findings as `audit-finding` records only when they should remain part of project governance.

## Branch workflow

Use a branch for a counterfactual, alternate timeline, exploratory revision, or any scenario that must not mutate mainline canon.

1. Validate and freeze the source/mainline bundle.
2. Copy or initialize a distinct branch bundle and record its source version, divergence point, assumptions changed, assumptions retained, and branch status in the branch manifest or change record.
3. Make all branch records explicitly `alternate` or `hypothetical`; do not write them into mainline files.
4. Run simulations and audits inside the branch. Treat outcomes as provisional unless the user approves them for that branch.
5. Run `branch_compare.py <source> <branch>` to see additions, removals, and changed fields.
6. To adopt a result, draft a new mainline transaction. Do not copy branch files over mainline or automatically merge an analysis result.
7. Archive or abandon the branch when it is no longer active; preserve provenance but exclude it from default recall.

A comparison report inventories difference. It does not decide whether a branch has better canon.

## Reader views

Run `export_reader_views.py <bundle>` when the author needs browseable material outside a conversation. It generates:

| Output | Purpose |
|---|---|
| `reader/index.md` | Entry point linking to generated views and entity dossiers. |
| `reader/dossiers/` | One status-aware profile per entity with summary, aliases, links, and evidence. |
| `reader/chronicle.md` | Ordered event history with direct causes and delayed effects where recorded. |
| `reader/canon-changelog.md` | Transaction-based history of proposed, applied, rejected, and reverted changes. |

Treat exports as deterministic presentations. Never edit a reader view to make canon changes; edit or transact against the authoritative records, then rebuild the view.
