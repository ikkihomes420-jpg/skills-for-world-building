---
name: worldbuilding-research
description: Plan and execute evidence-first research for worldbuilding projects — surveys and comparisons of real-world source material (history, culture, linguistics, technology, ecology), structured canon research for fictional settings, and grounded decision-making for what becomes lore. Use for multi-item investigations, source collection, comparative research, reference gathering, evidence-led canon decisions, and research documentation that feeds worldbuilding skills. Produces source records and claims that align with storycraft-os, living-canon-os, and conlang-design record formats.
---

# Worldbuilding Research

Use this skill when a worldbuilding project needs structured research: collecting real-world
reference material, comparing options across multiple sources, or deciding what evidence
justifies a canon decision. It is a research discipline, not an encyclopedia generator — it
keeps the difference between what a source says, what you inferred, and what became canon.

It is designed to work **alongside** the sibling skills:

- `storycraft-os` — world systems, simulation, and publication (consumes the claims this skill produces)
- `living-canon-os` — durable canon storage, transactions, and retrieval (stores the records)
- `conlang-design` — constructed language design (uses the same typology/elicitation discipline)

## Routing: what kind of research is this?

| Request shape | Route | Record to produce |
| --- | --- | --- |
| A bounded factual question ("did medieval cities have night watchmen?") | Focused lookup; cite the strongest source. | A single source record + short note. |
| A comparison or survey ("medicine across 6 fictional cultures", "sailing ship tech trees") | Write a research spec before collecting at scale. | `templates/research-spec.yaml` + batched source records. |
| Research feeding a canon decision ("should this culture be matriarchal?") | Spec + evidence review, then route the decision to the owning worldbuilding skill. | Source records + a claim with linked support. |
| Reference material for a conlang (real-language typology, glossing conventions) | Collect per `conlang-design` conventions; keep sources distinct from invented material. | Source records typed `reference-work` or `secondary-source`. |
| Canon consolidation across sessions | Hand records to `living-canon-os` via its transaction workflow. | Claims with support lists, ready to import. |

Do not build research artifacts for a one-off question. Scale the record-keeping to the
consequence of the decision.

## Core workflow

### 1. Define the investigation before scaling it

For any multi-item or multi-source research, fill in `templates/research-spec.yaml`:
the objects under study, the fields to fill per object, the evidence standard, the
completion criteria, and a human checkpoint. Validate it:

```bash
python3 scripts/validate_research_spec.py path/to/research-spec.yaml
```

The validator checks structural completeness only, not factual quality. Treat the spec
as a contract: reopen it when the question changes, a key source fails, or the evidence
would change a material conclusion.

### 2. Collect in bounded batches

Work in batches sized to the user's review capacity. After each batch, report:
what completed, what is blocked, which required fields are still unknown, any
source-quality concerns, and any proposed spec change. Pause for a checkpoint before
a material scope or method change.

Prefer primary and authoritative sources (historical documents, academic references,
field data, original dictionaries). Record for each source: locator, access date, what
it directly establishes, and its limits. **Never convert missing evidence into a
confident value** — mark it unknown or uncertain and carry that forward.

### 3. Separate extraction, analysis, and synthesis

- **Extraction** records what a source states. It is attributed, dated, and unmodified.
- **Analysis** derives a comparison or interpretation and states its method.
- **Synthesis** makes a claim across sources, links to the source records, and states scope.

Keep them in separate artifacts. A generated summary is never a source.

### 4. Record results in the shared vocabulary

Use the same record shapes the sibling skills define, so research output imports cleanly:

**Source record** (matches `living-canon-os` `templates/source.yaml`):

```yaml
kind: source
id: source.night-watch-london
source_type: secondary-source   # author-decision | primary-source | secondary-source | reference-work | project-note | generated-inference
locator: https://...            # URL, file path, or conversation anchor
scope: what this source supports or limits
reliability: high               # high | mixed | low
use_status: interpreted         # verified | interpreted | adapted | inspiration-only
license_or_permission: null
```

**Claim** (matches `living-canon-os` `templates/claim.yaml`):

```yaml
kind: claim
id: claim.night-watch-prevalence
label: Night watch coverage in pre-industrial cities
statement: Pre-industrial major cities commonly maintained organized night watch, varying by era and region.
status: provisional            # provisional | approved | disputed | deprecated
authority: assistant-proposed
confidence: plausible          # confirmed | plausible | speculative
truth_status: unknown          # unknown | true-in-canon | false-in-canon
support: [source.night-watch-london, source.watch-ordinance-york]
affected_ids: []               # canon entities this claim touches
```

Use `source_type: generated-inference` for your own reasoning chains — and never let a
generated inference alone support an approved canon claim.

### 5. Hand off to the owning skill

When research concludes, deliver:
- the completed spec (or a statement that no spec was needed),
- the source records,
- the claims with linked support,
- the limitations and unknowns.

Route each claim to its owner: world rules and systems → `storycraft-os`; canon storage
→ `living-canon-os` (as a capture transaction); language data → `conlang-design`. The
owning skill decides whether a claim becomes canon — this skill only assembles the
evidence.

## Calibration

Match the strength of the verb to the evidence: "is associated with" is not "causes";
"documented in 14th-century England" is not "universal in medieval Europe"; "common in
the sources I found" is not "universal". Preserve the difference between:

- **Documented** — a source states it.
- **Inferred** — you derived it from sources (say which).
- **Inspired-by** — a source shaped a decision that has no factual claim.
- **Invented** — a deliberate fictional choice; no source should be cited as proof.

For fiction, most final decisions are invented — that is the point. The research exists
so the inventions are grounded, internally consistent, and defensible when a reader asks
"would this actually work?"

## Rigor audit (before delivery)

| Dimension | Check |
| --- | --- |
| Evidence relevance | Every material claim links to at least one source record. |
| Scope calibration | Claims state their era, region, and population limits. |
| Inference integrity | Inferences are labeled and their reasoning preserved. |
| Completeness | Required spec fields are filled or explicitly marked unknown. |
| Reproducibility | Locators and access dates allow re-finding every source. |

Disclose remaining gaps in the final report rather than smoothing them over.

## References

Read `references/research-workflow.md` for the detailed lifecycle: spec structure,
batching rules, evidence-card discipline, outer-loop synthesis, and worked examples.
