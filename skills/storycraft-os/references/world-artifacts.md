# Storycraft OS World Artifacts

Use these schemas for any world that will be revisited, simulated, audited, published, or shared. The goal is a **small, linked source of truth**, not a database for its own sake. Start with the smallest artifacts that support the user’s scope, then add only records that affect generation, simulation, or continuity.

## 1. World Manifest

```yaml
world:
  id: lower-kebab-case
  name: Display name
  version: 0.1.0
  status: draft | active | frozen | retired
  uses: [worldbuilding, game, campaign, interactive-fiction, setting-bible]
  design_promise: What the world should feel like and what it will not be.
  scale: local | regional | planetary | interstellar | multiversal
  canon_sources: []
  constraints: []
  unresolved: []
  decision_log: []

reality_model:
  genre_calibration: realistic | low-fantasy | high-fantasy | science-fiction | surreal | mixed
  physics_or_metaphysics: []
  causality_level: strict | calibrated | symbolic
  information_technology: null
  map_status: absent | conceptual | canonical
```

A design promise is a decision filter. It might say, “A river-confederacy world where seasonal logistics, ritual obligation, and kinship shape politics more than territorial conquest.” It should make feature creep visible.

## 2. Entity Registry

Use one entity record for a place, faction, institution, culture, person, artifact, species, technology, language, belief system, or recurring phenomenon. Stable IDs never change when a display name, interpretation, or status changes.

```yaml
entity:
  id: fac-001
  type: faction
  name: The Reed Compact
  aliases: []
  status: approved | provisional | disputed | deprecated
  summary: One precise sentence.
  scope: geographic/social/temporal domain
  dependencies: []
  relationships: []
  resources: []
  beliefs_and_values: []
  constraints: []
  public_knowledge: []
  private_knowledge: []
  sources: [decision-id, event-id]
```

Keep **display name**, **canonical ID**, and **aliases** separate. Do not use a name as an identifier. A relationship points to another entity and states direction, kind, status, and evidence.

## 3. Systems Map

Worldbuilding requires interfaces. Do not list climate, culture, trade, and power as disconnected lore. For every consequential system, declare conditions, outputs, dependencies, and tension points.

```yaml
system:
  id: sys-water-law
  domain: ecology | economy | politics | culture | technology | magic | information | infrastructure
  statement: The system's rule or recurring behavior.
  inputs: []
  outputs: []
  constraints: []
  beneficiaries: []
  burdened: []
  failure_modes: []
  linked_entities: []
  evidence: []
```

Use a systems map to derive second-order effects. If trade depends on a seasonal pass, ask what happens to food prices, routes, migration, state revenue, disease movement, military campaigns, and metaphor—not whether each item is “interesting.”

## 4. Faction and Institution State

```yaml
faction_state:
  entity_id: fac-001
  objective_now: null
  long_horizon: null
  capabilities: []
  vulnerabilities: []
  resources: []
  constraints: []
  internal_divisions: []
  external_relationships: []
  public_position: null
  private_agenda: null
  current_pressure: null
  knowledge_ids: []
  updated_by: [event-id]
```

Institutions have mandates, incentives, capacity limits, internal politics, and information blind spots. Do not make every institution corrupt or efficient; give it a calibrated character supported by incentives, history, and oversight.

## 5. Timeline and Historical Causality

```yaml
event:
  id: evt-001
  date_or_sequence: null
  name: null
  status: proposed | approved | disputed | superseded
  causes: []
  event: What occurred.
  immediate_effects: []
  delayed_effects: []
  affected_entities: []
  sources: []
  counterfactual_branch: null
```

Events without causes may be deliberate mysteries, but mark them as such. Historical memory can differ from event truth. Store competing accounts in the knowledge ledger, not by overwriting the event record.

## 6. Knowledge and Public Narrative

```yaml
knowledge_item:
  id: know-001
  proposition: null
  truth_status: verified | believed | contested | false | unknown
  holders: []
  channel: witness | rumor | archive | dispatch | press | divination | inference
  reliability: high | mixed | low | unknown
  date_or_sequence: null
  public_status: secret | private | restricted | public | mythic
  sources: []
```

Separate what happened, what each actor believes, what the public believes, and what a player/reader knows. Information travels through physical and institutional channels; encode delays and distortions where they constrain action.

## 7. Consequence and Active State

```yaml
consequence:
  id: cons-001
  origin: event-id or decision-id
  scale: personal | relational | institutional | structural | civilizational
  affected: []
  current_state: latent | developing | visible | transformed | resolved
  next_surface: condition, trigger, or likely window
  author_intent: required | optional | unknown
  evidence: []

session_state:
  date_or_sequence: null
  pause_point: null
  active_entities: []
  active_situations: []
  consequence_ids: []
  open_threads: []
  player_choice_boundary: null
  drift_watch: []
```

The world state records active material only. Archive dormant entities and historical detail in the world bible; reactivate them when they begin affecting the present.

## 8. Canon Decisions and Audits

```yaml
decision:
  id: dec-001
  question: null
  chosen_option: null
  rationale: null
  affected_ids: []
  status: approved | provisional | superseded
  tests_required: []

audit_finding:
  id: aud-001
  severity: blocker | major | moderate | minor
  type: contradiction | underspecification | unsupported-link | deliberate-exception | drift
  evidence: []
  impact: null
  repair_options: []
  decision_needed: false
```

Preserve old canon in an audit or decision record. A repair becomes canon only after it receives an approved decision status.

## 9. World Release

A release includes world version, manifest, changed entities, changed systems, affected timeline/events, audit status, unresolved decisions, and an active-state snapshot. Freeze before substantial restructures so retroactive changes remain intelligible.
