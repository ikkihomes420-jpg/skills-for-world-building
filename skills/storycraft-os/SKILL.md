---
name: storycraft-os
description: >
  Build, simulate, govern, audit, and publish coherent fictional worlds as
  durable causal systems. Use for worldbuilding, lore bibles, factions,
  cultures, religions, economies, ecology, geography, infrastructure,
  technology or magic systems, timelines, alternate history, maps, campaigns,
  roleplay worlds, interactive simulation, canon management, event resolution,
  and persistent world state. Trigger on worldbuilding, lore, setting, faction,
  nation, culture, history, timeline, map, economy, religion, politics, magic
  system, simulation, campaign, RPG, world bible, canon, continuity, or
  alternate history.
---

# Storycraft OS

Use Storycraft OS as a **worldbuilding operating system**, not a novel-writing workflow. Build a world as a coherent model of constraints, entities, information, history, and consequences that can support lore development, games, campaigns, interactive narration, screen settings, fiction, or any other downstream use. Preserve author authority, approved canon, and the world’s declared reality model.

Read `references/world-artifacts.md` when creating or maintaining structured records. Read `references/world-systems-and-simulation.md` for system design, factions, historical simulation, alternate history, or interactive turns. Read `references/world-audit-and-governance.md` for canon conflicts, audits, releases, or long-running project control. Read `references/world-evolution-and-state.md` when defining world rules, routes/calendars, turn deltas, research provenance, canon migrations, or release impact. Copy from `templates/` instead of retyping a schema from memory; use the worked `templates/example-world-bundle.yaml` as a small internally-consistent baseline. Use `scripts/validate_world_bundle.py` only with a local JSON or YAML bundle the user has provided or explicitly asked to create. Use `--impact ID` before materially changing an established record; its direct-reference inventory supports judgment but does not decide the migration.

## Select the Operating Mode

| Request | Mode | First action | Deliverable |
|---|---|---|---|
| “Build me a world” | Bootstrap | Define purpose, scale, reality model, and design promise. | World manifest and systems seed. |
| “Expand this lore” | Canon extension | Extract existing canon and affected dependencies. | Compatible entity/system records and impact note. |
| “Make this nation/faction/culture work” | System design | Identify material conditions, power, values, information, and constraints. | Linked systems model and entity state. |
| “What happens next?” | Simulation turn | Load active state, actor goals, knowledge, and consequences. | Resolved state plus requested presentation mode. |
| “Run an alternate history” | Counterfactual simulation | Freeze source state and divergence point. | Branch chronology and consequence ledger. |
| “Fix the contradictions” | Audit and repair | Freeze current canon and collect conflicting evidence. | Severity-ranked findings and repair options. |
| “Make a map” | Spatial world design | Define geographic purpose, scale, constraints, and canonical names. | Map brief, geographic logic, and linked records. |
| “Pressure-test this decision” | World decision council | Frame stakes, options, canon, and reversibility. | Multi-lens analysis and one decisive next artifact. |

Never start with an encyclopedia. Start with the smallest model that can answer the user’s purpose, then expand only when a missing interface blocks a decision, simulation, or output.

## Establish the World Contract

For every continuing world, create a manifest with world identity, version, intended uses, scale, reality model, design promise, canonical sources, constraints, and unresolved decisions. A design promise must describe the experience and organizing pressures of the world, along with what it will not attempt. It prevents generic accumulation.

> **World rule:** Every consequential fact must be either a documented constraint, a linked consequence, a deliberate exception, or an open decision. Decorative facts may remain light; generative facts must be traceable.

Separate these states: **approved canon**, **provisional material**, **disputed in-world account**, **deprecated record**, **contradiction**, and **open decision**. A myth can be approved canon as a myth without being world truth. Do not erase a conflicting record merely because it is inconvenient.

## Build Systems Before Surface Lore

Model interfaces among geography/ecology, material economy, power, culture, information, technology/magic, and infrastructure. For each high-leverage condition, derive capability, constraint, incentive, actor response, consequence, and changed condition. Use the system records in `references/world-artifacts.md`; they force the world to have connective tissue rather than isolated facts.

| System | Ask | Test |
|---|---|---|
| Geography and ecology | What sustains or limits settlement, travel, food, disease, and defense? | Does the map constrain daily life and power? |
| Material economy | What is scarce, produced, moved, taxed, stored, or owed? | Do institutions and factions have resource logic? |
| Power and institutions | Who can authorize, coerce, administer, or legitimize action? | Can authority fail, divide, or adapt plausibly? |
| Culture and belief | What values, kinship, ritual, taboo, status, and metaphor arise from conditions? | Do customs connect to material and historical pressures? |
| Information | Who observes, archives, edits, hides, or broadcasts? | Can knowledge travel only through plausible channels? |
| Technology or magic | What are the prerequisites, costs, access rules, bottlenecks, and failure modes? | Do new capabilities create second-order effects? |

Do not impose universal pessimism. Cost, opposition, uncertainty, institutional friction, and variation are **calibrated counterweights** to frictionless worlds, not quotas. Effective institutions, clean victories, harmony, and joy are valid when the canon supports them.

## Maintain a Canonical World Model

Use stable IDs for entities, systems, events, decisions, knowledge items, and consequences. Maintain a small entity registry for people, cultures, places, factions, institutions, technologies, belief systems, languages, and phenomena that affect active work. Preserve aliases separately from canonical names.

For each major actor, track goal, resources, capabilities, vulnerabilities, constraints, beliefs, current pressure, public position, private agenda, relationships, and knowledge state. Actors can be cooperative, mistaken, divided, or principled; do not flatten them into plot functions or universal antagonists.

For each event, record causes, immediate effects, delayed effects, affected entities, status, and source. For each knowledge item, distinguish proposition, truth status, holder, channel, reliability, date, and public status. For each consequence, track origin, scale, affected entities, current state, and next surfacing condition.

## Govern Rules, Space, Evidence, and Change

Read `references/world-evolution-and-state.md` when a constraint governs multiple downstream decisions. Record its scope, strength, triggers, consequences, exceptions, authority, evidence, and supersession path. Treat an invariant, a default, a local custom, and a disputed model differently. For every exception, record why it is possible and what limits it.

Create calendar, location, and connection records only when space or time constrains access, travel, communication, jurisdiction, resources, or simulation. For research-grounded worlds, distinguish source records from claims, and mark whether a claim is verified, interpreted, adapted, or speculative. Before changing established canon, create a change set and run `validate_world_bundle.py <bundle> --impact <id>`; preserve redirects, splits, merges, and migration notes rather than silently rewriting a world’s past.

## Simulate Without Railroading

Use simulation mode for campaigns, roleplay, interactive fiction, or ongoing world turns. First load the active session state, consequences, actor goals, and information horizons. Advance systems and off-screen actors based on their own constraints. Apply the user/player action. Update entities, resources, beliefs, relationships, timeline, knowledge, and consequences.

Preserve the player’s meaningful high-impact decisions. When such a decision arrives, render the pressure and stop naturally; do not decide for the player or present branches that secretly converge. Record the resolution as a state transition: input forces, actor actions, information limits, rules/resources applied, uncertainty, state delta, and next decision boundary. Keep simulation mechanics, audits, ledgers, and probability reasoning out of immersive narration unless the user requests a game-facing or planning interface.

Run a light world-health check across recent turns: continuity; information plausibility; actor agency; active but varied pressure; and specific material/social presence. At arc breaks, contradictions, or drift flags, run a deeper audit using the governance reference. Correct drift by re-grounding in established state and maturing existing pressures—not by adding random crisis or enforcing constant darkness.

## Build Histories and Counterfactual Branches

Freeze the source state before making a historical change. Define the divergence point, immediate conditions changed, assumptions that remain stable, and uncertainty. Then trace personal, relational, institutional, structural, and civilizational consequences. Let downstream changes depend on capacity, communication, incentives, and time rather than treating history as a sequence of guaranteed milestones.

For historical research, identify which details require external verification and separate documented evidence from creative extrapolation. Use contemporary voices for lived uncertainty and material texture; use reliable analysis for causality and disagreement. Do not give people knowledge, language, technology, or social categories that their declared context cannot plausibly supply.

## Design Spatial Worlds and Maps

Create a map only after establishing the spatial question it must answer: settlement, route, watershed, biome, border, campaign geography, political reach, trade, migration, or cosmology. For reproducible fantasy territory maps, read and use `opengs-map-generator`. For language systems or writing systems, read and use `conlang-design`; link language entities back to the world canon. Treat a beautiful map or lexicon as canon only after it satisfies the world’s material, cultural, and historical constraints.

## Pressure-Test World Decisions

For a high-stakes choice, run a decision council with five lenses: downside, first principles, possibility, fresh outsider, and execution. Make trade-offs and missing evidence visible, then provide a conditional recommendation and one concrete next artifact. Do not convene a council for routine lore generation or factual lookups.

## Audit, Repair, and Release

Audit from reality rules through systems, entities, timeline, knowledge, active state, and terminology. Classify findings as contradiction, unsupported link, underspecification, scale mismatch, drift, or deliberate exception. Cite specific records. Preserve previous canon until an author-approved decision selects a repair.

For every material repair, state dependencies and at least two viable options where practical. Before release, freeze the version and deliver a manifest, effective rules, changed records, a formal change set, decisions, audit result, unresolved questions, compatibility note, and active-state handoff. A world can be incomplete; it must not pretend to be more settled than it is.

## Quality Gate

Before completing work, verify that:

- The output supports the world’s stated purpose, scale, and reality model.
- Systems connect facts to incentives, constraints, and consequences.
- Entities, events, knowledge, consequences, rules, locations, and change sets have distinct IDs and states where they matter.
- Cross-cutting rules state their scope, strength, authority, and exceptions.
- Information does not travel or become certain without an in-world channel or a documented enabling rule.
- Actors have agency, constraints, and beliefs instead of serving as worldbuilding labels.
- Interactive work preserves user/player meaningful choices and a stable state handoff.
- Maps, languages, histories, and lore satisfy declared dependencies rather than existing as unlinked decoration.
- Contradictions, assumptions, author decisions, sources, and claim confidence remain visible.
- Material canon changes have an impact inventory, migration record, and release compatibility note.

## Provenance

Storycraft OS is an original, Manus-compatible worldbuilding system developed from the user-supplied Storycraft Engine’s useful world-simulation concepts and from prior canon, causality, continuity, and evidence-management work. It intentionally excludes fiction-first drafting as the default and restructures the material around durable world state, systems, and author-governed simulation.

### Upgrade log

- **0.3.0** — Added explicit rule, spatial-temporal, state-transition, provenance/claim, and canon change-set artifacts. Extended JSON/YAML validation with semantic status checks, alias collision diagnostics, rule/location/transition/change-set reference checks, and `--impact ID` direct-reference reporting. Added reusable starter templates for every new artifact and a dedicated reference for governed world evolution.
- **0.2.0** — `templates/` was present but empty, forcing every record to be retyped from the schema examples in `references/world-artifacts.md`. Added one starter file per record type (manifest, entity, system, faction state, event, knowledge item, consequence/session state, decision/audit finding, world release) plus a worked `example-world-bundle.yaml` that validates clean. `scripts/validate_world_bundle.py` accepted only JSON while every documented schema is written in YAML; it now auto-detects and validates YAML bundles directly (`--format` to override detection).
