# Structured Research Intake and Empirical Workflow

Use this reference when the request is a multi-item investigation, a literature/technology/market review, an empirical project, a replication, or a research report. It complements—rather than replaces—the Research Governance Layer in `SKILL.md` and the artifact schemas in `research-governance/research-artifacts.md`.

## 1. Choose the Route

| Request shape | Route | Required record |
| --- | --- | --- |
| A bounded factual question | Perform focused research and cite primary sources where feasible. | Source notes only. |
| A comparison, survey, landscape, or due-diligence request | Create a research specification before collecting at scale. | `research-spec.yaml` or an equivalent approved plan. |
| A hypothesis, experiment, replication, or empirical analysis | Use the Research Governance Layer and the relevant technical specialist. | Research state, evidence cards, and a protocol before execution. |
| A paper, report, or research release | Run a claim–evidence audit; route to the paper-writing or ARA rigor specialist when appropriate. | Claim–evidence ledger and limitations. |

## 2. Structure the Investigation Before Scaling It

For a comparison or landscape, define the **objects/items**, **fields**, **source and time boundaries**, **evidence standard**, **completion criteria**, and a **human checkpoint**. Start from `templates/research-spec.yaml` when the work is likely to involve multiple items or repeated research.

Treat the specification as a contract, not a prediction. Confirm or revise it before broad collection. Reopen it when the user changes the decision question, a critical data source fails, a required field cannot be sourced, or the evidence would change a material conclusion.

> Preserve the distinction between an object of investigation, a source, an observation, an analysis, and a claim. No field is complete merely because an answer was generated; it is complete only when its evidence and uncertainty are recorded.

## 3. Collect Evidence in Bounded Batches

Work in batches whose size is appropriate to the user’s time, resource, and review constraints. Before beginning the next material batch, report completion, blocked items, unresolved required fields, source-quality concerns, and any needed specification change. Resume only after the checkpoint when a change is material.

Use the strongest available source for each field. Prefer primary documents, official datasets, original papers, repositories, and direct measurements; use credible secondary synthesis for context; identify uncorroborated or inaccessible evidence as uncertain. Capture a source URL or artifact path, retrieval date, what it directly establishes, and its limitations in an evidence card.

Never convert missing evidence into a confident value. Mark it **unknown**, **not publicly disclosed**, or **uncertain**, explain why, and preserve it for the final limitations section. Do not omit uncertainty merely to make a comparison table look complete.

## 4. Separate Extraction, Analysis, and Synthesis

Extraction records what a source states or measures. Analysis derives a comparison, calculation, or interpretation and must state the method. Synthesis makes a claim across evidence and must link to evidence cards, state scope, identify contradiction or uncertainty, and use calibrated language.

For a multi-item study, ensure every item is checked against all required fields before synthesis. Identify both missing required fields and extra observations that fall outside the agreed field framework. Do not force cross-item comparability when definitions, time periods, populations, or measurement methods differ.

## 5. Apply the Empirical Lifecycle When Applicable

Route a full empirical project through these stages, skipping only stages that are demonstrably out of scope:

1. **Question and design:** define the unit of analysis, decision consequence, theory/mechanism, data feasibility, identification or comparison strategy, and primary estimand or metric.
2. **Evidence and literature:** search systematically enough for the decision; preserve search boundaries, inclusion/exclusion logic, and gaps.
3. **Data and provenance:** record sources, permissions, retrieval dates, transformations, sample construction, joins, exclusions, and version identifiers.
4. **Analysis and identification:** state assumptions, controls/baselines, diagnostics, robustness checks, and threats to validity before interpreting estimates.
5. **Writing and citation:** distinguish source-backed facts from original analysis; verify citations and keep findings aligned with evidence.
6. **Reproducibility and release:** preserve code, configurations, environment, seeds, data-access instructions, generated outputs, and a regeneration path.
7. **Review and response:** audit claims, scope, limitations, and reproducibility; address critiques by revising evidence or analysis rather than narrative alone.

For experiments, follow the protocol, experiment-record, outer-loop, and claim-ledger schemas in `research-governance/research-artifacts.md`. For AI implementation, route each technical stage to the narrowest preserved specialist skill. For a paper or reusable research package, route to `ara-compiler`, `ara-research-manager` (at session end), or `ara-rigor-reviewer` as appropriate.

## 6. Verify Completion Before Reporting

Run `scripts/validate_research_spec.py <research-spec.yaml>` for a structured investigation. It requires the Python package `PyYAML`; install it in the execution environment if unavailable. The validator checks specification completeness, not factual truth or research quality. For experiment-heavy work, run `scripts/validate_research_bundle.py` on the local JSON bundle as described by the governance layer. Resolve errors; disclose warnings and remaining evidence gaps in the final report.

Before delivery, verify that required fields are covered or explicitly unresolved, material claims link to evidence, calculations are reproducible, conflicting sources are represented, and the stated conclusion does not exceed the evidence boundary.

## Workflow Provenance

This workflow adopts compatible design ideas from the MIT-licensed [Auto-Empirical-Research-Skills](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills)—notably lifecycle routing, provenance, reproducibility, and review gates—and [Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills)—notably plan-first item/field definition, iterative human control, structured results, and completeness validation. It is independently written and adapted to the local evidence-first governance model; it does not import or execute external repository code.
