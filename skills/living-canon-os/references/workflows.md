# Operating Workflows

Follow the workflow that matches the user’s actual need. Keep each workflow proportional: do not create empty registries, audit decorative details, or simulate outcomes when the user only asks for a small lore idea.

## 1. Bootstrap a living bundle

Use this when the user starts a persistent world, setting, series, project, research space, or ongoing campaign.

1. Establish the purpose, scale, and intended downstream uses. Ask only for the smallest missing decision that blocks progress.
2. Create `manifest.yaml` from the template. Record the design promise, reality model or domain assumptions, canon/capture policy, authoritative inputs, constraints, and open questions.
3. Create a minimal seed registry containing only actors, places, systems, concepts, or events already needed for the user’s purpose.
4. Create `state/active-snapshot.md` and identify the present state, active threads, consequences, and first decision boundary.
5. Validate the bundle. Report what is established, provisional, and intentionally unknown.

Do not begin with an encyclopedia. Add a record only when it answers a current question, constrains a decision, supports continuity, or will be needed by a known output.

## 2. Capture conversation memory

Use this when the conversation has introduced potentially durable material, or the user asks to save an exchange.

1. Identify candidate entities, aliases, claims, events, rules, relationships, decisions, knowledge changes, consequences, and open questions.
2. Record a conversation source locator if available. If no precise locator is available, say so and preserve the candidate as lower-confidence material.
3. Compare each candidate with existing records. Detect same-entity aliases, duplicate names, contradictory claims, and dependent records.
4. Classify candidates as new, confirmation, revision, contradiction, deliberate exception, branch divergence, or unresolved.
5. Present a concise proposed update with the affected IDs and status changes. Do not silently convert a candidate into approved canon.
6. On user approval, write records, append a dated session delta, validate the bundle, and rebuild the snapshot.

Use this response shape for a checkpoint:

```markdown
## Proposed memory update

| Change | Status | Evidence | Action needed |
|---|---|---|---|
| `entity.irel-001` gains alias “The Ash Regent” | Confirmation | Session locator | Approve / adjust / discard |
| `rule.soul-binding` gains a pre-death exception | Revision | Session locator | Decide whether it is world-wide or local |
| `event.crownless-night` date conflicts with `event.red-tide` | Contradiction | Linked records | Choose chronology or mark disputed |
```

## 3. Recall and briefing

Use this when the user asks “what do we know,” “where did we leave off,” “who is this,” “what changed,” or “where did that idea come from.”

1. Load the manifest and active snapshot first. Then load only the records directly related to the request and the newest relevant delta.
2. Answer in reader view. Distinguish **Established**, **Provisional**, **Contested**, and **Unknown** material.
3. Cite record IDs and source/decision locators in a compact “Basis” line. Do not present archived or superseded material as current without explaining its status.
4. If the record set is too broad, give a concise map and offer focused follow-up areas instead of dumping raw data.
5. Mention active consequences or unresolved decisions only when they affect the requested subject.

Use this response shape:

```markdown
## [Subject] — current briefing

**Established.** …

**Provisional.** …

**Contested.** …

**Unknown.** …

**Basis:** `entity.…`, `event.…`, `decision.…`.
```

## 4. Canon extension

Use this when new lore, a new system, a character, a location, a world rule, or a major fact is added or revised.

1. Determine whether the material is decorative, consequential, or cross-cutting. Use a normal entity/claim for decorative and local facts; use a rule/system/event/change set for material with broader effects.
2. Identify applicable world constraints, actor knowledge limits, time/space constraints, related systems, and relevant existing entities.
3. Derive at least the immediate implications. For high-leverage changes, trace incentives, capacity, opposition, second-order effects, and what must now become different.
4. Produce the smallest coherent addition: records, a brief impact note, and any open decision. Keep generated causal links plausible rather than treating every implication as a mandatory negative consequence.
5. Require approval for a material change to approved canon. After approval, validate and rebuild the snapshot.

## 5. Simulation or interactive state transition

Use this for campaign turns, interactive fiction, “what happens next,” or author-led state advancement.

1. Load active state, relevant world rules, active consequences, actor states, actor knowledge, and the latest decisions.
2. State assumptions, time advanced, scope, and whether the result is an author proposal or a resolved player-authorized action.
3. Advance off-screen actors from goals, resources, capabilities, constraints, relationships, and information—not from a need to force a plot.
4. Apply user/player action only at the granted level of authority. Do not resolve a high-impact player decision without explicit permission.
5. Record a `state-transition`: inputs, actor actions, knowledge constraints, resolution basis, uncertainty, outcomes, record changes, created/resolved consequences, and a next choice boundary.
6. Present immersive material separately from ledger material. The user should not need to read mechanics to enjoy a scene.
7. Capture the transition as provisional unless the user’s governance policy specifies an automatic approval rule.

## 6. Audit and repair

Use this for continuity checks, logic checks, terminology clean-up, canon drift, or pre-release review.

1. Freeze the relevant current version and define the audit scope. Do not audit the entire world when the user asks about one faction or a single era.
2. Inspect from governing constraints downwards: manifest/design promise, rules and systems, entities/relationships, timeline, knowledge states, active state, terminology, and changes.
3. Classify each finding as one of: contradiction, duplicate, underspecification, unsupported-link, scale mismatch, stale record, terminology collision, drift, or deliberate exception.
4. Cite the specific affected records and explain actual impact. “Could be richer” is not an audit finding unless it blocks the declared use.
5. For material problems, offer two or more viable repair paths when practical. Mark which option retains current canon, which performs a retcon/migration, and which leaves an ambiguity as intentional.
6. Create `audit-finding` records only after the user asks to preserve the audit or the work is a formal release. Do not make an audit itself canon.

Severity guide:

| Severity | Use when | Example |
|---|---|---|
| Blocker | It prevents required work or invalidates a core rule. | Teleportation’s travel constraints contradict a mandatory war plot without an exception. |
| Major | It materially confuses history, agency, or active state. | Two approved records give a capital to different factions in the same period. |
| Moderate | It creates a meaningful but locally repairable inconsistency. | An alias is used as two separate people in one chapter plan. |
| Minor | It is a presentation, naming, or detail issue with low impact. | Inconsistent spelling of a non-conflicting minor place name. |

## 7. Migration, retcon, and branch

Use a migration for a deliberate revision to mainline canon. Use a branch for a counterfactual, alternative, hypothetical, or exploratory timeline.

1. Freeze and validate the current source state.
2. Run the impact report on each material ID to change. Inspect both direct references and semantic dependencies; the report is evidence, not an automatic decision.
3. For a migration, create a proposed change set containing the action, target, replacement IDs, rationale, impacts, migration notes, verification, and author decision.
4. For a branch, create a branch manifest containing source version, divergence point, conditions changed, conditions held constant, uncertainty, and new branch ID. Do not mutate mainline records.
5. Preserve old records as deprecated or superseded when appropriate. Use redirects for renamed identities, splits for conflated records, and merges only by explicit decision.
6. After approval, update the manifest version, rebuild the snapshot, and produce a short compatibility note.

## 8. Session handoff and release

Use this at the end of a significant session, before a long pause, or before sharing work with another collaborator.

1. Validate the bundle and resolve structural errors. Leave legitimate uncertainty visible rather than falsely resolving it.
2. Append a session delta that names approved additions, provisional items, decisions, altered state, contradictions discovered, and deferred work.
3. Rebuild `state/active-snapshot.md`.
4. Include effective rules, active entities, present time/state, active consequences, open threads, author choices pending, latest decisions, and drift-watch items.
5. For a formal release, include manifest version, change set, audit status, unresolved questions, and compatibility note.

A handoff is successful when a later conversation can begin with the snapshot, identify what is authoritative, and resume work without inventing missing history.
