---
name: living-canon-os
description: Build, maintain, recall, audit, simulate, branch, and hand off durable living knowledge bases with transaction-governed canon changes and grounded retrieval. Use for persistent world bibles, lore/canon systems, campaign or series state, continuity memory across conversations, canon approval and retcons, evidence-backed recall, relationships, factions, rules, timelines, consequences, alternate branches, and universal project or research knowledge bases that need inspectable long-term state.
---

# Living Canon OS

Use this skill as a **durable continuity and memory engine**, not as an encyclopedia generator. Preserve a small linked source of truth that can answer what is established, what changed, why it changed, where a claim came from, what remains uncertain, and what needs an author decision.

The system has five distinct layers. The project-owned canonical records are authoritative; tracked discussions preserve valuable non-canon exploration; transactions govern changes; indexes, graphs, and snapshots are rebuildable derived views; reader views make the state usable. Never let a generated summary, a search match, an exploratory discussion, or an inferred relationship become canon by itself.

## Non-negotiable principles

- Treat the user as the final authority. Never describe an inference, convenient repair, semantic match, or generated detail as user-approved canon.
- Separate **world truth**, **in-world knowledge/belief**, and **presented narrative**. A myth or faction doctrine may be canon as a belief without being true in the setting.
- Keep **approved**, **provisional**, **disputed**, **deprecated**, **superseded**, and **unknown** material visibly distinct.
- Preserve stable IDs and history. Use a transaction, change set, redirect, split, merge, deprecation, or branch rather than silently rewriting established material.
- Link consequential material to conversation locators, author decisions, sources, or explicit evidence. State uncertainty plainly.
- Capture only consequential or decision-relevant material. Do not convert conversational decoration into permanent records.
- Treat ordinary possibility discussions as conversation, not as canon proposals. Preserve them as detailed discussion records only when the user asks to track them.
- Retrieve selectively. Load a compact snapshot and a grounded evidence packet, never the entire archive by default.
- Preserve detail in layers: a brief summary for orientation, rich context for reasoning, and source detail for exact evidence. Never let a compact summary overwrite the detail it represents.

> **Canon rule:** Every consequential fact must be a documented constraint, linked consequence, deliberate exception, approved decision, source-backed claim, or explicitly open question.

## Set up the bundle

Store each user’s durable data in a **project-owned bundle**, never in this skill directory. Use a user-supplied path when available; otherwise propose a clear project path before creating it. Keep authoritative records in the bundle and derived artifacts in `.canon/`, `reader/`, and `audit/` so they can be rebuilt safely.

Start with a manifest, the minimum entity/claim/event records, and `state/active-snapshot.md`. Add rules, actor states, knowledge states, consequences, locations, transitions, branches, and change sets only when they constrain active work. Create `transactions/` when persistent capture begins and `state/session-deltas/` when approved changes occur.

Read `references/records-and-statuses.md` before creating or modifying records. Read `references/fast-and-rich-context.md` before handling exploratory discussion, setting update depth, or answering a detailed request. Read `references/workflows.md` for worldbuilding, simulations, branches, audits, and handoffs. Read `references/transaction-governance.md` before proposing, approving, rejecting, or rolling back a material update. Read `references/retrieval-and-evidence.md` before recall or evidence-based answers. Read `references/integrity-branches-and-views.md` before a semantic audit, branch comparison, or reader export. Read `references/domain-packs.md` when adapting the engine beyond fictional worlds.

## Choose an operating mode

| User intent | Mode | Required deliverable |
|---|---|---|
| Start a world, setting, series, project, or research base | **Bootstrap** | Manifest, minimum registry, active snapshot, and explicit open questions. |
| Save what emerged in conversation | **Capture** | A proposed transaction and concise reviewable memory update. |
| Keep ideas, alternatives, or analysis without making canon | **Tracked discussion** | Rich discussion record marked `not-proposed`; no canon effect. |
| Approve, reject, or undo a canon update | **Transaction review** | Human-readable diff, decision record, and applied/rejected/reverted outcome. |
| Ask what has been established or where work stopped | **Grounded recall** | Compact evidence packet with status, basis, and relevant linked records. |
| Add or revise lore, a rule, entity, or event | **Canon extension** | Candidate records, impact note, and transaction where material. |
| Ask what happens next | **Simulation** | Provisional state transition, active consequences, and a clear decision boundary. |
| Check continuity or logic | **Audit and repair** | Severity-ranked findings, exact evidence, and repair paths. |
| Explore alternate history or a possible change | **Branching** | Frozen source state, branch divergence, comparison, and merge proposal if requested. |
| End a session or prepare for later use | **Handoff or release** | Snapshot, session delta, index rebuild, audit status, and reader views if useful. |

## Execute the Version 2 loop

### 1. Load purposefully

Read the manifest, active snapshot, newest session delta, and the records directly related to the request. If a bundle is substantial, run `query_canon.py` to assemble an evidence packet rather than scanning every file. Report relevant status, authority, branch, and uncertainty before relying on a record. If no bundle exists, bootstrap instead of pretending to remember prior work.

### 2. Retrieve before generating

Use the **fast path** for local work: load the active snapshot, run an exact/narrow query for the named subject, retrieve zero hops unless a direct dependency matters, and update only the affected records. Do not read the full archive, run a broad audit, or export reader views for an ordinary local addition.

Use the deep path only for a cross-cutting rule, major event, retcon, branch change, relationship change, identity collision, significant exception, or a user request for detailed reasoning. For recall, filter by branch, status, type, visibility, and scope before ranking. Use graph expansion only when a linked cause, relationship, dependency, or consequence affects the question. Answer from the evidence packet and label **Established**, **Provisional**, **Contested**, and **Unknown** explicitly.

Use `query_canon.py --detail brief` for ordinary continuity, `--detail context` for nuanced reasoning, and `--detail full` only for close reading of selected records. A derived index is never canon. Rebuild it with `build_index.py` after bulk changes, imports, or repairs. Do not manually edit `.canon/index.json`.

### 3. Separate discussion from canon capture

Default to ordinary conversation when the user is exploring possibilities, comparing options, debating implications, or thinking aloud. Do not manufacture a canon proposal. When the user asks to retain the exploration without choosing it, save it with `capture_discussion.py` as a detailed or verbatim `discussion` record marked `not-proposed`.

Create a canon candidate only when the user clearly asks to establish, revise, promote, or use the material going forward. Identify its evidence, authority, affected records, and possible impact. At a natural boundary, create a concise capture proposal that states what is new, what changes, what conflicts, and what requires a decision. Default to explicit approval for canon-level changes. Auto-capture only if the manifest authorizes it and the change is within that stated policy.

### 4. Reconcile and review

Compare candidates with stable IDs, aliases, rules, chronology, active state, branches, relationships, and prior transactions. Identify duplicates, contradictions, missing prerequisites, information-horizon breaches, unintended consequences, and affected records. Use `impact_report.py` before a material change; use `audit_invariants.py` for a broader integrity check.

Create a proposed transaction with `capture_transaction.py`, then render it with `review_transaction.py`. A review must show what changes, why, supporting evidence, affected records, and stale-draft warnings. Do not ask the user to approve opaque raw YAML.

### 5. Apply through governed transactions

Apply an approved transaction with `apply_transaction.py <bundle> <transaction-id> --approve-by <authority>`. This makes targeted record edits, appends a session delta, rebuilds the snapshot and index, and preserves the transaction as an audit trail. Reject an unwanted proposal with a review note. Roll back only through the guarded rollback path; never overwrite a record changed by a later transaction.

Use a change set or branch for major retcons, splits, merges, and alternate histories. Do not disguise a high-impact migration as a routine field edit.

### 6. Keep derived views current

Use `build_snapshot.py` for focused conversational handoff; `build_index.py` for full-text, alias, and relationship retrieval; and `export_reader_views.py` for dossiers, chronicle, and changelog. These outputs are derived and can be deleted/rebuilt without losing canon.

## Memory and canon governance

| Field | Meaning |
|---|---|
| `authority` | Who or what established a record: user-approved, source-backed, imported, assistant-proposed, or inferred. |
| `status` | Lifecycle state: approved, provisional, disputed, deprecated, superseded, archived, proposed, applied, rejected, or reverted where applicable. |
| `confidence` | Evidentiary strength: confirmed, plausible, speculative, or unknown. |
| `visibility` | Who can know/use it: author-only, public-world, restricted, or actor-specific. |
| `branch` | Mainline, alternate, hypothetical, or abandoned timeline/context. |
| `transaction` | A reviewable change proposal and decision trail; it is not itself canon. |

Never promote a record merely because it appears in an assistant summary or similarity search. A conversation-derived claim should cite its session/turn locator when available. If evidence is vague, keep the material provisional or as an open question.

## Worldbuilding-specific controls

Model systems before surface lore. Connect geography/ecology, material economy, institutions, culture/belief, information, technology or magic, and infrastructure through incentives, constraints, and consequences. Create a rule record only when a claim constrains multiple downstream choices.

For active actors or factions, track objective, resources, capabilities, vulnerabilities, constraints, public position, private agenda, relationships, and knowledge state. For events, track causes, immediate and delayed effects, affected records, evidence, and branch. For consequences, track origin, scale, current state, and the condition under which they surface again.

In interactive work, preserve meaningful user/player choice. Do not resolve a high-impact decision without authorization. Record provisional simulations as state transitions showing forces, actions, knowledge limits, rules/resources applied, uncertainty, outcomes, changed records, and the next choice boundary.

## Branches, audits, and reader views

Before a branch or major migration, freeze and validate the source state. Keep branch records separate from mainline. Use `branch_compare.py` to identify additions, removals, and changed fields; treat its output as an impact inventory, not an automatic merge. Bring selected branch material to mainline only through a new reviewed transaction.

Use integrity audits to surface real problems: duplicate identities, branch leakage, invalid relationship dates, missing knowledge holders, underspecified exceptions, or a missing choice boundary. Cite exact IDs and offer repair options. Do not “repair” canon by deleting awkward history.

Default to reader view in user-facing outputs. Use raw record views when the user requests direct editing or inspection. Generate deterministic dossiers, chronicles, and changelogs when a human needs to browse the archive outside a conversation.

## Quality gate

Before completing a material update, verify that:

- Consequential records have stable IDs, appropriate statuses, authority, confidence, branch, and evidence links.
- World truth, belief, public knowledge, and presented narrative have not been collapsed together.
- The transaction shows exact changes, rationale, sources, and current assumptions; no stale draft is applied.
- Rules state scope, strength, triggers, consequences, and bounded exceptions where they matter.
- Events, actors, and simulated outcomes respect plausible causes, resources, relationships, time, and information horizons.
- Mainline records do not unintentionally depend on alternate, hypothetical, or abandoned branches.
- Active consequences, open threads, decisions, and recent deltas appear in the snapshot.
- Derived indexes and reader views are current or explicitly marked stale.
- The output remains proportionate to the user’s goal; do not build an encyclopedia merely because the schema permits it.

## Utilities

Run `validate_bundle.py <bundle>` for structural validation. Use `capture_discussion.py` to retain rich non-canon exploration. Run `impact_report.py <bundle> <record-id>` before changing a consequential record. Use `capture_transaction.py`, `review_transaction.py`, and `apply_transaction.py` for governed canon updates. Use `build_index.py` and `query_canon.py --detail <brief|context|full>` for grounded retrieval at the right depth. Use `audit_invariants.py` for integrity checks, `branch_compare.py` for branch divergence, `build_snapshot.py` for handoffs, and `export_reader_views.py` for readable exports. Read each tool’s `--help` output before extending its use.

Do not add a README, changelog, or user-facing documentation to this skill package. Keep concise operating rules in `SKILL.md`, deeper procedures in `references/`, reusable inputs in `templates/`, and deterministic utilities in `scripts/`.
