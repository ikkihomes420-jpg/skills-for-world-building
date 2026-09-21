# Integration Map

This reference maps Gradual Worldbuilding's pace-and-method layer onto the four sibling skills at the field level. Its purpose is that **every increment this skill produces is already the record a sibling skill expects** — no reformatting, no invented parallel schema, no lost provenance.

The shared vocabulary comes from `living-canon-os` and is used by all four skills. Do not introduce new status values.

| Field | Permitted values | Meaning |
|---|---|---|
| `status` | approved, provisional, disputed, deprecated, superseded, archived | Lifecycle and canon handling |
| `authority` | user-approved, source-backed, imported, assistant-proposed, inferred | Who established the record |
| `confidence` | confirmed, plausible, speculative, unknown | Strength of support for the proposition |
| `visibility` | author-only, public-world, restricted, actor-specific | Access / knowledge scope |
| `branch` | mainline, alternate, hypothetical, abandoned | Timeline or contextual branch |
| `truth_status` | verified, believed, contested, false, unknown | Objective status of a knowledge proposition |
| `reliability` | high, mixed, low, unknown | Reliability of a source, observer, or channel |

Never collapse source reliability, claim confidence, canon approval, and in-world truth into one field.

## Division of labour

| Layer | Owner | Governs |
|---|---|---|
| Pace and sequence | **gradual-worldbuilding** (this skill) | Which increment happens next, whether a stage-gate is passed, how deep to go |
| World systems, rules, simulation, release | `storycraft-os` | What the world is made of and how it behaves |
| Durable canon, statuses, transactions, recall | `living-canon-os` | What is established, how it changes, where a claim came from |
| Evidence from real-world sources | `worldbuilding-research` | What is documented, inferred, invented, and how well supported |
| Languages as testable systems | `conlang-design` | Phonology, grammar, lexicon, diachrony, glossing |

This skill never stores canon and never invents schema. It produces **proposals** in the owner's format and hands them over.

## Loop step → sibling mapping

| Loop step | Primary sibling | Record / tool | Notes |
|---|---|---|---|
| 1. Locate the current layer | `living-canon-os` | `manifest.yaml`, `state/active-snapshot.md`, newest session delta, `query_canon.py --detail brief\|context` | Read before adding. Use sibling statuses. If no bundle exists, bootstrap one. |
| 2. Select the next pressure | `storycraft-os` | `event` (if it is an occurrence) or a `decision`/`open-question` (if it is a choice) | One pressure, developed; note the runners-up as future increments. |
| 3. Establish conditions | `storycraft-os` + `worldbuilding-research` | `rule`/`world-rule` for prerequisites; `source`+`claim` for facts that need evidence | A missing prerequisite is an open question, not a silent import. |
| 4. Multiple lenses | `storycraft-os` | `system`, `world-rule`, `knowledge` (information lens) | Express lens results in the sibling's record kinds. |
| 5. Actor agency | `living-canon-os` | `actor-state`, `relationship`, `knowledge` | Asymmetry lives in resources/capabilities/vulnerabilities/knowledge. |
| 6. Plausible paths | `worldbuilding-research` + `living-canon-os` | `claim` (with calibrated `confidence`), `decision` (options + chosen option) | Calibrated language maps to `confidence` and `reliability`. |
| 7. Consequences mature | `living-canon-os` | `consequence` (`latent/developing/visible/transformed/resolved`; `personal/relational/institutional/structural/civilizational`) | Latent consequences persist; they are not lost prose. |
| 8. Stage-gate check | this skill | `templates/stage-gate.yaml` | Assessment is evidence, not canon. |
| 9. Record the increment | `living-canon-os` | `templates/development-increment.yaml` → `state-transition` + `change-set` + `consequence` + `claim` + `decision`/`open-question` | Hand to `capture_transaction.py` → `review_transaction.py` → `apply_transaction.py`. |

## Ladder → record mapping

Each ladder rung is a capacity. When a rung is reached, it usually creates or updates specific sibling records.

### Settlement and political growth
- Rungs produce `entity` records (place, institution, polity) and `rule`/`world-rule` entries for shared obligations (tax, labour, adjudication).
- The market-town threshold typically creates a `location`/`spatial-network` record in `storycraft-os` (routes, reach, seasonality) plus `consequence`s for outlying households.
- Administrative capacity is a `system` in `storycraft-os`, not an `entity` title. A "capital" without a chancery, stores, or jurisdiction is a label.

### Security growth
- A **warrant** is a `rule` with scope and exceptions; a **captain** is an `entity` plus `actor-state`; equipment custody is a `system` (maintenance, resupply, loss).
- Distinguish in the records: escort ≠ conquest; protection ≠ sovereignty; taxation ≠ occupation.
- Security failures become `consequence`s and `audit-finding`s, not retroactive rule edits.

### Religious growth
- Doctrines are `knowledge` records (`truth_status: believed|contested`) — belief and world-truth stay separate.
- Institutions are `entity` + `actor-state`; welfare and conversion networks are `relationship`s with `valid_from`/`valid_to`.
- Competing rites are `disputed` or `rule` with `strength: disputed`, never silently merged.

### Character growth
- An actor is `entity` (`type: person`) + `actor-state` + `relationship`s + `knowledge`.
- Reputation change is a `state-transition` outcome, not a rewritten `entity.summary`.
- "Later remembered as important" is not a reason to make them important now — importance emerges from recorded choices and effects.

### Technology and infrastructure
- Capability is a `rule`/`world-rule` (`layer: technological`, with prerequisites, costs, failure modes) plus a `system`.
- Every rung above "prototype" needs a maintenance record: who repairs it, with what, at whose cost.
- Wider adoption is an `event` with `immediate_effects`/`delayed_effects` and a `change-set` if it alters established canon.

### Communication, literacy, and language
- Naming conventions, borrowed terms, and registers that affect multiple decisions become `world-rule`s (`layer: social|informational`).
- Actual language design is delegated to `conlang-design`: record its hard constraints as `C-` records and mirror the world-facing ones as `world-rule`s so a later change cannot silently violate them.
- A written register requires scribes, material, reason, and readers — model those as `entity`/`system` before declaring literacy.

### Knowledge and information
- All of this ladder is `knowledge` records: `proposition`, `holders`, `channel`, `reliability`, `truth_status`, `visibility`.
- Delay, distortion, and competing accounts are content, not noise. Conflicting accounts coexist as separate `knowledge` records linked to the same `event`.

## Handoff contract to the canon system

When a canon bundle is in use, a completed increment is delivered as a proposal, never applied silently:

1. **Assemble** the increment with `templates/development-increment.yaml`.
2. **Capture** it with `capture_transaction.py` (operations: `create`, `update`, `deprecate`, `redirect`).
3. **Impact-check** material targets with `impact_report.py` before touching consequential records; use `change-set` actions (`add`, `modify`, `deprecate`, `redirect`, `split`, `merge`) for high-impact moves.
4. **Render** it with `review_transaction.py` so the author approves a readable diff, not raw YAML.
5. **Apply** only after explicit approval with `apply_transaction.py <bundle> <transaction-id> --approve-by <authority>`.
6. **Rebuild** derived views (`build_snapshot.py`, `build_index.py`, `export_reader_views.py`) — these are never canon.

If the author has not approved, the increment stays `provisional` with `authority: assistant-proposed`. A stage-gate pass does not imply canon approval.

## Research hook

Any plausibility question that a real-world fact would settle routes to `worldbuilding-research`:

- Form the question as a decision-relevant comparison, not a curiosity.
- Collect `source` records (`source_type`, `locator`, `scope`, `reliability: high|mixed|low`, `use_status: verified|interpreted|adapted|inspiration-only`).
- Synthesize `claim` records linking support, with `confidence` calibrated to the evidence.
- Return with the limits and unknowns attached. The owning skill (usually `storycraft-os` for rules/systems, `living-canon-os` for storage) decides whether the claim becomes canon.

A source grounds an invention; it is never cited as proof of the invention.

## Conlang hook

World-level language facts this skill controls:

- **Which rung** of the communication/literacy ladder the setting has reached (this constrains what a language may plausibly be).
- **What the language must satisfy**: names that fit the culture's sound world, registers for ritual vs trade, a script that its material and literate class can support.
- **What is hard**: constraints a later design must not violate, expressed as `conlang-design` `C-` records and mirrored as `world-rule`s.

The language's internal coherence is `conlang-design`'s responsibility; its place in the world is this skill's.

## Failure to integrate

Warning signs that the pace layer is drifting from the suite:

- Records with status or confidence values not in the shared vocabulary.
- A stage-gate passed with no `state-transition` or `change-set` record behind it.
- Consequences that exist only in prose and will never resurface.
- A claim presented as fact with no `source` record and no stated `confidence`.
- A world rule that contradicts a `conlang-design` constraint because the constraint was never mirrored.
- Canon advanced without a transaction and an explicit author decision.
