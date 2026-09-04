# World Rules, State Evolution, and Change Impact

Read this reference when defining hard or soft world rules, creating a calendar or route network, resolving a simulation turn, changing established canon, branching history, or preparing a major release. This layer makes the world’s **governing assumptions, transitions, and impacts** inspectable without demanding scientific precision from every genre.

## 1. Maintain an Explicit Rule Registry

Use a world rule for any claim that constrains multiple future decisions. A lore fact does not need a rule record unless a contradiction would affect several entities, systems, events, or outputs.

```yaml
world_rule:
  id: rule-001
  layer: physical | metaphysical | social | technological | magical | informational | temporal
  statement: What is normally true in the world.
  scope: Entities, regions, eras, or conditions governed by this rule.
  strength: invariant | default | local-custom | disputed
  triggers: When this rule must be evaluated.
  consequences: What follows when the rule applies.
  exceptions: []
  authority: natural-law | institution | culture | technology | magic | author-decision
  status: approved | provisional | deprecated
  evidence: []
  supersedes: null
```

Use **invariant** only when violating the rule is impossible or creates a deliberate paradox. Use **default** when exceptions are possible but require a causal explanation. Use **local-custom** for region-, culture-, or institution-specific norms. Use **disputed** for competing in-world models. Every exception must name its scope, mechanism, cost, and source; it is not a loophole placeholder.

## 2. Model Space and Time Only When They Constrain Action

Create a spatial-temporal model when route length, terrain, communication latency, seasonal access, jurisdiction, map scale, calendar, or travel capacity affects world state. Do not convert every map label into a simulated network.

```yaml
calendar:
  id: cal-001
  name: Flood Reckoning
  units: [day, season, year]
  epochs: []
  conversion_notes: null

location:
  id: loc-001
  type: settlement | region | route-node | landmark | realm | orbit | plane
  parent: null
  terrain_or_medium: null
  access_constraints: []
  controlling_entities: []
  status: approved

connection:
  id: con-001
  from: loc-001
  to: loc-002
  mode: foot | road | river | sea | rail | air | portal | relay
  availability: constant | seasonal | conditional | disputed
  travel_cost: null
  communication_cost: null
  hazards: []
  rules: []
```

Treat time and distance as **inputs to decision quality**, not arbitrary delays. If information arrives instantly because of magic or technology, record the enabling rule and the political, economic, or cultural effects of that capability.

## 3. Resolve State Transitions as Deltas

Do not replace a session ledger with a recap. Store a transition from a known state to a new state, including why it happened and what changed. A transition can represent one roleplay turn, one season, one political crisis, or one historical period.

```yaml
state_transition:
  id: turn-001
  from_state: state-001
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
    entities_changed: []
    systems_changed: []
    knowledge_changed: []
    consequences_created: []
    consequences_resolved: []
  next_state: state-002
  player_choice_boundary: null
  canon_status: provisional | approved
```

Keep three layers separate: **world truth**, **actor knowledge**, and **presented output**. In an interactive turn, do not resolve a high-impact player decision without explicit authorization. In an author-led simulation, label any inferred actor action provisional until the author approves it when that distinction matters.

## 4. Track Sources, Claims, and Confidence

Use provenance records for research-grounded settings, adaptation work, collaborative lore, or any project where it matters whether a claim is confirmed, interpreted, or invented.

```yaml
source_record:
  id: src-001
  kind: author-decision | primary-source | secondary-source | reference-work | project-note | generated-inference
  citation_or_locator: null
  access_date: null
  scope: What the source supports or limits.
  reliability: high | mixed | low | unknown
  use_status: verified | interpreted | adapted | inspiration-only
  license_or_permission: null

claim:
  id: clm-001
  statement: null
  status: approved | provisional | disputed | deprecated
  support: [src-001]
  confidence: confirmed | plausible | speculative | unknown
  affected_ids: []
```

A source record captures evidence; a claim captures the worldbuilding assertion. Do not turn a real-world source into fiction canon without an explicit author decision or adaptation status.

## 5. Perform Change Impact Analysis Before Canon Migration

Before changing or deprecating an established ID, request an impact report. Inspect direct references and semantic dependencies: entity links, system links, event effects, knowledge holders, consequence targets, state references, rules, routes, and prior decisions. The validator’s `--impact ID` report is an inventory, not a decision.

```yaml
change_set:
  id: chg-001
  from_version: 0.2.0
  to_version: 0.3.0
  status: proposed | approved | applied | reverted
  changes:
    - action: add | modify | deprecate | redirect | split | merge
      target_id: null
      replacement_ids: []
      rationale: null
      expected_impacts: []
      migration_notes: null
  verification: []
  author_decision: null
```

Use **redirect** when a stable ID is renamed but refers to the same thing. Use **split** when one record has been discovered to cover multiple canon entities. Use **merge** only when the distinction was never canonical or is deliberately retired. Never delete the provenance of a changed record.

## 6. Release a World State, Not Just a World Bible

A meaningful release has a manifest version, effective rule set, change set, current state, active consequences, known contradictions, open decisions, and compatibility notes. Freeze the source state before creating a counterfactual branch or making a high-impact canon migration. The goal is reversibility and traceability, not bureaucratic overhead.
