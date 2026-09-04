# Worldbuilding Research Workflow

Detailed reference for planning, executing, and delivering research for worldbuilding
projects. Complements the core workflow in `SKILL.md`. The record formats here match the
`source` and `claim` templates in `living-canon-os` and `storycraft-os`, so research
output imports cleanly into canon storage.

## 1. Research spec: the contract

Before collecting at scale, fill in `../templates/research-spec.yaml`. A complete spec
answers:

| Section | What it fixes | Worldbuilding example |
| --- | --- | --- |
| `topic` / `question` | The decision the research informs | "Which real governance structures should the three river cultures adapt?" |
| `purpose` | What happens with the result | "Pick governance for culture C's capital." |
| `scope.included` / `excluded` | What is in and out | Include river-delta societies; exclude maritime empires. |
| `objects` | The items compared | Each real society or each fictional culture. |
| `fields` | What is recorded per object | Succession rule, food base, trade goods, legal tradition. |
| `evidence_standard` | How strong a source must be | Minimum sources per material claim; preferred source types. |
| `completion_criteria` | When you may stop | Every required field sourced or marked unknown. |
| `human_checkpoint` | What requires user review | Scope change, method change, material conclusion. |
| `status` | Draft → approved → in_progress → complete → paused | Track the spec's own lifecycle. |

Validate structure before collecting:

```bash
python3 ../scripts/validate_research_spec.py research-spec.yaml
```

Reopen the spec when the decision question changes, a key source fails, a required field
cannot be sourced, or the evidence would change a material conclusion. Record the change
and treat post-change results as exploratory.

## 2. Evidence discipline

### Source records

One record per salient source. For worldbuilding, the source types that matter:

- `primary-source` — documents, data, or artifacts from the studied period/culture.
- `reference-work` — dictionaries, encyclopedias, WALS, field guides, atlases.
- `secondary-source` — academic syntheses, histories, analyses.
- `project-note` — your own project notes, clearly marked as such.
- `author-decision` — the author's deliberate fictional choice; not evidence.
- `generated-inference` — the assistant's own reasoning; never cite as proof.

Capture: locator (URL, citation, or file path), access date, **what it directly
establishes**, and what it does not establish. Note what a source does not establish as
carefully as what it does.

### Never launder uncertainty

Missing evidence is recorded as **unknown**, **not publicly disclosed**, or **uncertain**,
with a reason. Do not fill a required field with a plausible-sounding value. Do not
produce a complete-looking comparison table from incomplete evidence; ship the gaps.

### Distinguish evidence from fiction

Keep a hard line between:

| Type | Meaning |
| --- | --- |
| Documented | A source states it. |
| Inferred | You derived it, and you say from what. |
| Inspired-by | A source shaped a decision; no factual claim is made. |
| Invented | A deliberate fictional choice; cite nothing as proof. |

A source may support the *inspired-by* case but never the *invented* case. When a claim
becomes canon, its support list must contain only sources that genuinely back it.

## 3. Batched collection and checkpoints

Work in batches sized to the user's review capacity. Before the next material batch,
report: completions, blockers, unresolved required fields, source-quality concerns, and
any proposed spec change. Resume after the checkpoint when a change is material.

Prefer the strongest source for each field. If two sources conflict, keep both records
and represent the conflict; do not average or silently pick one. For fictional targets,
conflicts are often design fodder: "sources disagree on X, so region A follows tradition
P and region B follows tradition Q" is a legitimate, labeled outcome.

## 4. Outer-loop synthesis

Run this after a meaningful batch of results, a surprise, a plateau, or a material
constraint change. Produce a short synthesis note:

```yaml
id: synthesis.001
evidence_reviewed: [source.x, source.y]
result_patterns: [what keeps showing up]
contradictions: [where sources conflict]
supported_constraints: [constraints the fiction must respect]
updated_direction: deepen | broaden | pivot | pause | conclude
rationale: why this direction
next_steps: []
human_checkpoint: required | optional | none
```

- **deepen** — an effect needs more sources or mechanism (e.g., the daily rhythm of a craft you keep citing).
- **broaden** — adjacent questions now matter (e.g., neighboring cultures, climate).
- **pivot** — the evidence contradicts a design assumption.
- **pause** — source quality blocks reliable progress.
- **conclude** — the findings and their limits can be stated coherently.

Before concluding, run the rigor audit in `SKILL.md` and confirm every material claim
links to evidence with stated scope and uncertainty.

## 5. Delivery and hand-off

Deliver:

1. The spec (status `complete`, or a note that no spec was needed).
2. Source records — one per salient source, with locators and access dates.
3. Claims with linked `support` lists and calibrated confidence.
4. The limitations and unknowns, prominently.
5. The synthesis notes.

Route the claims:

| Claim type | Destination |
| --- | --- |
| World rules, systems, faction behavior | `storycraft-os` (world bundle + audit) |
| Durable canon, continuity, retcons | `living-canon-os` (capture transaction) |
| Language/typology/glossing data | `conlang-design` (canon template + lexicon) |

The owning skill decides whether a claim becomes canon. This skill assembles and
attributes evidence; it does not approve canon.

## 6. Worked example

> **Request:** "Research how real pre-industrial cultures handled wood scarcity for a
> forest-based fictional culture."
>
> **Route:** Comparison across several real societies → write a spec first.
>
> **Spec:** objects = chosen real cultures; fields = fuel economy, building materials,
> forest-management practice, scarcity responses; evidence standard = at least 2 sources
> per material claim; checkpoint before the synthesis step.
>
> **Collection:** one source record per society/source; unknowns stay unknown; conflicts
> preserved.
>
> **Synthesis:** "Documented practices cluster around coppicing, rights-of-use systems,
> and material substitution. The fictional culture adopts coppicing (documented),
> adapts rights-of-use to a guild structure (inspired-by), and adds a sacred-grove taboo
> (invented)."
>
> **Hand-off:** the invented elements go to `storycraft-os` as a claim whose support is
> empty for the invented part and cites sources only for the documented part — often as
> two claims: one documented, one invented-but-grounded.

## 7. Provenance

The evidence-first governance model (plans / observations / evidence / claims separation,
calibrated language, pre-execution protocols, claim–evidence ledgers) is adapted from the
MIT-licensed [Orchestra Research AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs)
governance layer, refactored from AI-engineering research to worldbuilding research. The
record vocabulary is aligned with `living-canon-os` and `storycraft-os` so research
output imports cleanly.
