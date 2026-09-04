# Records and Statuses

Use this reference to create, edit, reconcile, or audit records in a Living Canon bundle. The bundle is intentionally schema-light: every record is a YAML or JSON object with a stable `id`, `type`, `label`, `status`, `authority`, `confidence`, `sources`, and optional `branch` unless a template establishes otherwise.

## Record conventions

Use lower-kebab-case IDs in the form `<kind>.<slug>-<number>` or `<kind>.<slug>`. Examples include `entity.irel-001`, `event.iron-flood-017`, and `rule.soul-binding`. IDs do not change when display names or interpretations change. Record old names in `aliases`; record replacement history with `supersedes`, `redirects_to`, or an approved change set.

Use ISO dates when a real-world audit date is useful. Use the setting’s own calendar/sequence in `date_or_sequence`; do not force fictional chronology into Gregorian dates. Keep arrays explicit, even when empty. Prefer a compact sentence in `summary` or `statement` to an essay.

## Shared vocabularies

| Field | Permitted values | Meaning |
|---|---|---|
| `status` | approved, provisional, disputed, deprecated, superseded, archived | Lifecycle and canon handling. |
| `authority` | user-approved, source-backed, imported, assistant-proposed, inferred | Who established the record. |
| `confidence` | confirmed, plausible, speculative, unknown | Strength of support for the proposition. |
| `visibility` | author-only, public-world, restricted, actor-specific | Access/knowledge scope. |
| `branch` | mainline, alternate, hypothetical, abandoned | Timeline or contextual branch. |
| `truth_status` | verified, believed, contested, false, unknown | Objective status of a knowledge proposition where relevant. |
| `reliability` | high, mixed, low, unknown | Reliability of a source, observer, or information channel. |

Use `approved` only for material the user explicitly accepted, marked as established, or supplied as existing canon. Use `provisional` for promising new material that needs confirmation. Use `disputed` when conflicting records are intentionally unresolved. Use `deprecated` when an old record remains relevant for historical reference but should not drive new work. Use `superseded` only when a later record or change set identifies its successor.

> **Never collapse source reliability, claim confidence, canon approval, and in-world truth into one field.** They answer different questions.

## Manifest

Create exactly one `manifest.yaml` at the bundle root. It defines what the bundle is for and prevents feature drift.

```yaml
kind: manifest
id: manifest.<project-slug>
name: Display name
version: 0.1.0
status: active
uses: [worldbuilding]
design_promise: >-
  A sentence describing the desired experience, governing pressures, and what
  the project deliberately will not attempt.
scale: regional
reality_model:
  genre_calibration: mixed
  causality_level: calibrated
  map_status: conceptual
canon_policy:
  capture_mode: approval-required
  default_branch: mainline
  canonical_sources: []
  authority_order: [user-approved, source-backed, imported, assistant-proposed, inferred]
constraints: []
unresolved: []
decision_log: []
last_updated: 2026-08-26
```

## Entity

Use an entity for anything that persists and can have identity, aliases, attributes, or relationships: a person, place, faction, institution, culture, artifact, species, technology, language, belief system, project, concept, or recurring phenomenon.

```yaml
kind: entity
id: entity.<slug>
type: person
label: Display name
aliases: []
status: approved
authority: user-approved
confidence: confirmed
visibility: author-only
branch: mainline
summary: One precise sentence.
scope: geographic, social, temporal, or project scope
dependencies: []
relationships: []
attributes: {}
sources: []
supersedes: null
redirects_to: null
```

Do not duplicate an entity merely because its name changes. Use a relationship record when a relation needs its own validity period, evidence, or uncertainty; otherwise, a lightweight relationship object in the entity record is sufficient.

## Claim

Use a claim for a proposition that needs provenance, confidence, truth status, or separate approval. A claim may concern one or many entities and may become a rule only when it governs multiple future choices.

```yaml
kind: claim
id: claim.<slug>
label: Short statement title
statement: The proposition being asserted.
status: provisional
authority: assistant-proposed
confidence: plausible
truth_status: verified
visibility: author-only
branch: mainline
affected_ids: []
support: []
contradicts: []
notes: null
```

## Rule or constraint

Create a rule only when a fact constrains multiple future decisions. Use `invariant` only when violation is impossible or a deliberate paradox; use `default` when exceptions require explanation; use `local-custom` for culture/region/institution-specific norms; use `disputed` for competing in-world models.

```yaml
kind: rule
id: rule.<slug>
label: Short rule name
statement: What is normally true.
layer: physical
strength: default
scope: []
triggers: []
consequences: []
exceptions: []
authority_type: author-decision
status: approved
authority: user-approved
confidence: confirmed
visibility: author-only
branch: mainline
sources: []
supersedes: null
```

Every material exception must state its scope, mechanism, cost/limit, and source. A convenient loophole is not an exception record.

## Event

Use an event for historical occurrences, current incidents, releases, decisions, or changes with identifiable causes or effects.

```yaml
kind: event
id: event.<slug>
label: Event name
date_or_sequence: null
status: approved
authority: user-approved
confidence: confirmed
branch: mainline
summary: What occurred.
causes: []
immediate_effects: []
delayed_effects: []
affected_ids: []
sources: []
knowledge_accounts: []
counterfactual_branch: null
```

An event without a cause can be valid if it is intentionally marked as a mystery or unknown condition. Store competing historical accounts as knowledge records, not by overwriting the event.

## Knowledge item

Use a knowledge record when it matters what a particular actor, audience, public, or user believes or can access.

```yaml
kind: knowledge
id: knowledge.<slug>
label: Short proposition title
proposition: The knowledge or belief.
truth_status: believed
holders: []
channel: rumor
reliability: mixed
date_or_sequence: null
visibility: actor-specific
status: approved
authority: user-approved
confidence: confirmed
branch: mainline
sources: []
```

Keep **world truth**, **holder belief**, and **presented output** separate. Information must travel through a plausible channel when timing, secrecy, or deception constrains action.

## Relationship

Create a standalone relationship when direction, duration, strength, status, or evidence matters to continuity.

```yaml
kind: relationship
id: relationship.<slug>
from_id: entity.<source>
to_id: entity.<target>
relation_type: alliance
direction: directed
status: approved
authority: user-approved
confidence: confirmed
valid_from: null
valid_to: null
strength: null
summary: null
sources: []
branch: mainline
```

## Decision and open question

Use a decision to record user authority, choices, rationale, and the effect of resolution. Use an open question for a material unknown that should resurface rather than be forgotten.

```yaml
kind: decision
id: decision.<slug>
question: What needs an author decision?
options: []
chosen_option: null
rationale: null
affected_ids: []
status: provisional
authority: user-approved
confidence: confirmed
sources: []
branch: mainline

kind: open-question
id: question.<slug>
question: What remains unknown?
importance: high
related_ids: []
next_review: null
status: provisional
authority: user-approved
confidence: unknown
branch: mainline
sources: []
```

## Actor state and consequence

Use actor state only for active actors or organizations whose independent agency affects the current work. Use consequence records to retain unfinished effects that should surface later.

```yaml
kind: actor-state
id: actor-state.<entity-slug>
entity_id: entity.<slug>
objective_now: null
long_horizon: null
capabilities: []
vulnerabilities: []
resources: []
constraints: []
internal_divisions: []
public_position: null
private_agenda: null
current_pressure: null
knowledge_ids: []
status: approved
authority: user-approved
confidence: confirmed
branch: mainline
sources: []

kind: consequence
id: consequence.<slug>
origin: event.<slug>
scale: institutional
affected_ids: []
current_state: latent
next_surface: A condition, trigger, or likely window.
author_intent: optional
status: approved
authority: user-approved
confidence: confirmed
branch: mainline
sources: []
```

Valid consequence states are `latent`, `developing`, `visible`, `transformed`, and `resolved`. Valid scales are `personal`, `relational`, `institutional`, `structural`, and `civilizational`.

## State transition, change set, and audit finding

Use a transition for a resolved simulation turn, historical interval, campaign action, or major project-state update. Use a change set before modifying material canon. Use audit findings to preserve evidence and repair options.

```yaml
kind: state-transition
id: transition.<slug>
from_state: state.<slug>
date_or_sequence: null
inputs:
  world_forces: []
  actor_actions: []
  user_or_player_action: null
  knowledge_constraints: []
resolution_basis:
  rules: []
  resources: []
  uncertainties: []
outcomes: []
state_delta:
  records_changed: []
  consequences_created: []
  consequences_resolved: []
next_state: state.<slug>
player_choice_boundary: null
status: provisional
authority: inferred
confidence: plausible
branch: mainline
sources: []

kind: change-set
id: change.<slug>
from_version: 0.1.0
to_version: 0.2.0
status: proposed
changes: []
verification: []
author_decision: null
sources: []
branch: mainline

kind: audit-finding
id: audit.<slug>
severity: moderate
type: contradiction
evidence: []
impact: null
repair_options: []
decision_needed: true
status: provisional
authority: inferred
confidence: plausible
branch: mainline
sources: []
```

For a change-set entry, use an action of `add`, `modify`, `deprecate`, `redirect`, `split`, or `merge`. Include the target ID, replacement IDs where applicable, rationale, expected impacts, and migration notes. A redirect preserves identity after a rename; split and merge require explicit author approval.

## Session state and source records

Use `state/active-snapshot.md` for reader-oriented handoff. Use a source record only when a claim depends on an external source, imported work, or a specific conversation locator.

```yaml
kind: source
id: source.<slug>
source_type: author-decision
locator: conversation:session-01#turn-12
scope: What this source supports or limits.
reliability: high
use_status: verified
license_or_permission: null
```

A source supports a claim; it is not itself a claim. For a real-world research source, distinguish `verified`, `interpreted`, `adapted`, and `inspiration-only`. Do not make research material into setting canon without an explicit author decision.

## Transaction

Use a transaction to propose, approve, reject, apply, or revert a material update. It is a governance and provenance record, not a canon fact. Keep transactions under `transactions/`; record resulting canonical state separately in the affected records.

```yaml
kind: transaction
id: transaction.<timestamp>-<slug>
title: Short human-readable change title
rationale: Why this update is needed.
status: proposed
authority: assistant-proposed
branch: mainline
source_locators: []
created_at: 2026-08-26T00:00:00Z
operations:
  - op: update
    target_id: entity.<slug>
    before:
      summary: Previous value
    after:
      summary: Proposed value
review_notes: []
approval: null
```

Use `proposed` until the author explicitly accepts the change. On approval, retain the transaction as `applied`, add approver/time metadata, write a session delta, and update the relevant records. On rejection, retain it as `rejected` with a review note. Use `reverted` only after the guarded rollback procedure successfully restores affected records without overwriting later changes.

The permitted transaction operations are `create`, `update`, `deprecate`, and `redirect`. Use a `change-set` or a branch for a high-impact split, merge, migration, or counterfactual; do not force those operations into a routine field update.

## Detail preservation convention

Every consequential record may include an optional `detail` field or linked context record. Use it for nuance that a one-sentence `summary` or `statement` cannot safely carry: exceptions, motivations, causal reasoning, examples, historical texture, edge cases, unresolved ambiguities, and exact terminology. The `summary` is a retrieval index, not a replacement for `detail`.

Use three retrieval layers: `brief` for the core identity/proposition, `context` for selected rich fields and direct dependencies, and `full` for close reading of a selected record. Keep exact source wording in source/evidence records when wording itself is meaningful. Do not remove detail merely because an active snapshot needs to stay compact.

## Discussion record

Use a discussion record for valuable non-canon exploration, analysis, comparisons, option sets, and possibility space that should be retained without asking the user to treat it as an update proposal.

```yaml
kind: discussion
id: discussion.<timestamp>-<slug>
title: What the discussion explored
summary: Optional short index only
content: Full retained exploration
disposition: exploratory
canonical_status: not-proposed
detail_level: detailed
status: provisional
authority: user-approved
confidence: unknown
visibility: author-only
branch: mainline
source_locators: []
related_ids: []
tags: []
created_at: 2026-08-26T00:00:00Z
```

Valid dispositions are `exploratory`, `analysis`, `reference`, `draft`, and `rejected`. Valid detail levels are `verbatim`, `detailed`, and `summary`. A discussion does not become a canon candidate unless the user explicitly asks to promote its contents; preserve that boundary in recall and generation.
