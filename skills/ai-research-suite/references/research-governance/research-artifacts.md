# Research Artifact Templates and Rigor Rubric

Use these structures for multi-session empirical or technical research. Adapt vocabulary to the field, but preserve the separation between **plans, observations, evidence, and claims**. Never silently promote an exploratory pattern to a confirmatory conclusion.

## 1. Research State

```yaml
project:
  id: lower-kebab-case
  title: Working title
  owner: user | team
  status: bootstrap | active | paused | synthesis | concluded
  question: A question answerable with defined evidence
  scope: What the project includes and excludes
  decision_checkpoint: What requires human review

method:
  target_population_or_system: null
  primary_metric: null
  success_criterion: null
  baseline: null
  constraints: [time, compute, data, ethics]

hypotheses:
  - id: H1
    statement: X because Y, predicting Z
    status: proposed | registered | tested | supported | refuted | inconclusive
    priority: 1
    prediction: null
    protocol_ids: []

next_actions: []
open_questions: []
known_constraints: []
```

A research question must identify its unit of analysis, evidence boundary, and decision consequence. If it cannot, narrow the question before experimentation.

## 2. Evidence Cards and Literature Ledger

```yaml
evidence_card:
  id: EV-001
  type: literature | dataset | benchmark | observation | experiment | analysis
  source: DOI | URL | file path | experiment ID
  retrieved_or_created: 2026-08-25
  supports: [H1, CLM-002]
  claim: What this evidence directly establishes
  methods_or_context: Conditions needed for interpretation
  limitations: []
  quote_or_measurement: Exact quotation, table, figure, or value
  confidence: low | medium | high
```

Do not write “the literature shows” without a traceable source. Store one evidence card per salient paper, result, or observation. Note what a source does **not** establish as carefully as what it does.

## 3. Protocol Before Execution

```yaml
protocol:
  id: P-001
  hypothesis: H1
  type: confirmatory | exploratory | diagnostic | replication
  rationale: Why this test can discriminate among possibilities
  intervention_or_comparison: null
  controls_and_baselines: []
  inputs_and_data_version: null
  primary_metric: null
  secondary_metrics: []
  prediction: null
  stopping_rule: null
  analysis_plan: null
  preregistered_at: timestamp or repository revision
  risks: []
```

Register a confirmatory protocol before viewing its outcome. If the plan changes after observations, create a new protocol and label the result exploratory or follow-up confirmatory. A protocol is not a guarantee of correctness; it is a guard against hindsight.

## 4. Experiment Record

```yaml
experiment:
  id: E-001
  protocol: P-001
  status: planned | running | completed | failed | invalidated
  environment: software versions, hardware, random seeds
  data_version: null
  outcome:
    primary_metric: {value: null, unit: null, baseline: null, delta: null}
    secondary_metrics: []
  sanity_checks: []
  artifacts: [config, log, raw-data, plot]
  interpretation: What the result permits; not a final claim by itself
  anomalies: []
  next_action: null
```

Record failures and invalid results. A failed execution is not evidence against a hypothesis unless the failure itself was measured and diagnosed.

## 5. Outer-Loop Synthesis

Perform this after a meaningful batch of results, a surprise, a stall, or a material constraint change.

```yaml
synthesis:
  id: S-001
  evidence_reviewed: [EV-001, E-001]
  result_patterns: []
  contradictions: []
  supported_constraints: []
  updated_hypotheses: []
  decision: deepen | broaden | pivot | pause | conclude
  rationale: null
  next_experiments: []
  human_checkpoint: required | optional | none
```

Use **deepen** when an effect needs mechanism, robustness, or ablation; **broaden** when adjacent questions now matter; **pivot** when assumptions fail or a stronger question appears; **pause** when resources, ethics, or evidence quality block reliable progress; and **conclude** only when the contribution and limits can be stated coherently.

## 6. Claim–Evidence Ledger

```yaml
claim:
  id: CLM-001
  text: Calibrated statement of result
  kind: descriptive | comparative | causal | mechanistic | recommendation
  evidence: [EV-001, E-003]
  scope: population, conditions, and uncertainty
  status: candidate | supported | contested | withdrawn
  confidence: low | medium | high
  limitations: []
```

Every consequential conclusion must point to evidence cards and specify scope. The strength of the verb must match the design: “is associated with” is not “causes”; “under these tested conditions” is not “generally.”

## 7. Rigor Audit

Score each dimension from 0 to 3 and give evidence-based findings.

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Evidence relevance | No linked evidence. | Loose or indirect evidence. | Relevant evidence with gaps. | Direct, triangulated evidence. |
| Falsifiability | Unclear claim. | Vague prediction. | Testable claim with partial disconfirmation path. | Clear prediction, controls, and failure conditions. |
| Scope calibration | Overclaims. | Limits implied but absent. | Main limits stated. | Scope, uncertainty, and transfer conditions explicit. |
| Argument coherence | Narrative assertions only. | Partial linkage. | Reasonable evidence chain. | Explicit claim-to-evidence-to-limit reasoning. |
| Exploration integrity | Hindsight hidden. | Protocol/result order unclear. | Exploratory work labelled. | Confirmatory and exploratory evidence clearly separated. |
| Reproducibility | No artifacts. | Partial notes. | Config/data/environment mostly captured. | Complete retrievable artifacts and regeneration path. |

The audit outcome is **pass**, **conditional pass**, or **fail**. A high average score cannot compensate for an unsupported causal or safety-critical claim.

## Provenance

This original schema is informed by public MIT-licensed material in [Orchestra Research’s AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs), especially its lifecycle-oriented autoresearch, ideation, and rigor concepts. It is substantially refactored for Manus as a bounded, checkpointed, evidence-first system that routes AI-specific implementation to the local `ai-research-suite` rather than reproducing its specialist content.
