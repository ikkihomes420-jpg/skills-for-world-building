# Anti-Rush and Repair

This reference covers the recurring ways a world is advanced too fast, too cheaply, or too flatteringly — and how to repair each one with the smallest credible change. Use it when a proposal feels convenient, when a stage feels reached too easily, or when a project has drifted toward an endpoint.

The stance is **critical partnership**: test ideas honestly, accept what works, revise what is promising but overstated, quarantine what violates the established world. Disagreement is a service, not an obstacle. Never agree by default to be agreeable.

## Failure modes

### 1. Grand-title leap
**Looks like:** "the empire", "the capital", "the standing army", "the university" appear without the machinery that makes them possible.
**Detection:** the label implies functions (taxation, jurisdiction, succession, records, pay) that no record supports; stage-gate dimension 6 (terminology) scores `0`–`1`.
**Why it happens:** an endpoint is more vivid than its prerequisites.
**Repair:** separate the title from the function. Ask what the institution can actually *do* on an ordinary day, then award at most the capacity shown. The title may remain as the world's own aspirational word, but canon records the function. Typically creates or updates `entity` + `rule`/`world-rule` + `system` records.

### 2. Founder fallacy
**Looks like:** an institution, city, religion, technology, or dynasty exists because one great person made it, and vanishes nowhere when they leave.
**Detection:** removing one named individual collapses the capability; stage-gate dimension 4 (continuity) is `≤ 2`.
**Why it happens:** protagonists are easier to write than institutions.
**Repair:** show the second and third person. Who was taught? Who financed it? Who carries it when the founder dies, fails, or is discredited? Add an apprenticeship, an office, or a custom, and record it. Maps onto `actor-state`, `relationship`, and a continuity `rule`.

### 3. Frictionless borrowing
**Looks like:** a foreign technology, religion, or language is copied whole, with no adaptation, opposition, cost, or skill gap.
**Detection:** the imported thing works identically in the new setting; no local materials, labour, or hydrology are mentioned.
**Why it happens:** the design is known to work, so the transplant feels safe.
**Repair:** require adaptation to at least three local conditions (materials, labour/skill, environment), then name one thing that *resists* — a guild, a rite, a shortage. Borrowing can succeed, but it must be paid for. Usually a `rule` with prerequisites + an `event` + a `consequence`.

### 4. Singular feat
**Looks like:** a one-time triumph (a great bridge, a decisive victory, a miraculous cure) presented as if it were infrastructure.
**Detection:** no one can repeat it; stage-gate dimensions 1 and 2 are `≤ 2`.
**Why it happens:** singular events are dramatic and memorable.
**Repair:** keep it as a `event` with `immediate_effects` and `delayed_effects`, and explicitly mark the capability as *not* repeatable. If repetition is desired, build the missing repeatability and maintenance first. A feat is allowed to stay a feat.

### 5. Protagonist gravity
**Looks like:** one household, hero, faction, or culture bends the whole world around it; everyone else is scenery.
**Detection:** after developing a central actor, the surrounding population is unnamed, unaffected, or uniformly approving.
**Why it happens:** narrative focus naturally narrows.
**Repair:** deliberately return to the whole settlement. Name households, labourers, dissenters, dependents, traders, and people harmed or excluded. Give at least one actor who benefits, one who bears a cost, and one who reads the change differently. Uses `actor-state`, `knowledge`, and `relationship` records.

### 6. Cost-free institution
**Looks like:** a standing army, welfare system, bureaucracy, or religion with no one paying for it and nobody maintaining it.
**Detection:** the cost bearer cannot be named; no labour, tax, tithe, levy, or displacement is recorded.
**Why it happens:** costs are less interesting than capabilities.
**Repair:** name who pays — in labour, goods, land, time, or legitimacy — and who is displaced or indebted. If no one can pay, the capability is subsidized by narration and must shrink. Almost always a `rule` (obligation) plus `consequence`s landing on named entities.

### 7. Map-first or lexicon-first
**Looks like:** a beautiful map or an elaborate language exists before the world knows what question it must answer.
**Detection:** the map/lexicon cannot yet constrain any decision (routes, jurisdiction, who speaks what, who reads what).
**Why it happens:** concrete artifacts feel like progress.
**Repair:** state the spatial or linguistic question first, then let the artifact answer it. Delegate map detail to the `storycraft-os` spatial records and language detail to `conlang-design`; keep only the world-facing constraints. A pretty artifact is canon only after it satisfies material, cultural, and historical constraints.

### 8. Instant literacy or codification
**Looks like:** a full written register or formal grammar in a settlement with no scribes, writing surface, record-keeping reason, or readers.
**Detection:** the communication/literacy ladder skips rungs; stage-gate dimensions 2 and 3 are low.
**Why it happens:** writing feels like a marker of advancement.
**Repair:** climb the ladder — purpose, material, scribes, readers — before codification. Restrict literacy to the small class that actually exists and record what they read and write, and why. World-facing constraints mirrored as `rule`s; language internals handed to `conlang-design`.

### 9. Escalation treadmill
**Looks like:** each turn introduces a bigger crisis because the previous one no longer excites; history becomes a sequence of escalating spectacles.
**Detection:** the selected pressure is chosen for drama rather than being forced by current state; mundane bottlenecks are skipped.
**Why it happens:** spectacle is confused with progress.
**Repair:** select the *most deferred* bottleneck instead of the most dramatic event. Storage, water, fodder, disease, seasonality, inheritance, and debt usually matter more than battles. Let new pressures grow out of unresolved consequences rather than arriving from outside.

### 10. Contradiction erasure
**Looks like:** a conflicting earlier record is quietly rewritten to match the new one.
**Detection:** canon changed without a transaction, change set, redirect, or deprecation; old material disappeared.
**Why it happens:** contradictions are embarrassing.
**Repair:** preserve the old record. Mark it `deprecated` or `superseded`, add a `change-set` with rationale and migration notes, and record the author's decision. Never repair canon by deleting awkward history.

## Detection sweep

Run this quick sweep before accepting a large proposal:

| Question | Fail signal | Owner skill |
|---|---|---|
| Is this capacity or only a label? | No function behind the title | this skill + `storycraft-os` |
| Who does the labour, and who pays? | Cost bearer unnamed | `living-canon-os` consequence |
| What must already exist? | Prerequisites unstated | `storycraft-os` rule |
| What if the founder dies/leaves/fails? | Capability collapses | `living-canon-os` actor-state |
| Who benefits, loses, resists? | Everyone approves | `living-canon-os` actor-state/knowledge |
| Repeatable or singular? | Batch of one | `storycraft-os` system |
| Reach, influence, protection, jurisdiction, or control? | Terms used interchangeably | `storycraft-os` rule/location |
| Real constraint or invented veto? | Local limits used to block all knowledge | `worldbuilding-research` claim |
| Is one actor doing too much causal work? | Scenery population | `living-canon-os` actor-state |
| Smallest adjustment that makes it credible? | None offered | this skill |

Cite the sibling skill that should hold the repair, and produce the repair as a proposal, not a silent edit.

## Disagreement language

Keep the criticism proportionate to the evidence and useful to the author:

- **Accept:** "This works; the prerequisites are already in the record."
- **Revise:** "The direction is right, but the scale is ahead of the capacity. Smallest fix: …"
- **Quarantine:** "This currently contradicts an approved rule. Keep it as a branch or provisional claim until the contradiction is resolved."
- **Decline:** "Not credible under current capacity without an exception. Here is what would have to change first."

Never be dismissive, and never flatten a promising idea to avoid conflict. A recommendation should name the strongest objection, the hidden assumption, and the smallest change that resolves it.

## Repair ordering

When several things are wrong, repair in dependency order:

1. **Rules and prerequisites** (`storycraft-os`) — wrong foundations invalidate everything downstream.
2. **Actor capacity and knowledge** (`living-canon-os`) — who can actually do the thing, and who knows it.
3. **Labour, cost, and maintenance** — who pays and who repairs.
4. **Consequences** (`living-canon-os`) — latent effects that must resurface.
5. **Terminology and titles** — last, once function is real.
6. **Derived views and summaries** — rebuild after the records settle; never let a summary overwrite the detail it represents.

Repairs to approved canon go through a transaction and an author decision. Provisional material can be revised directly, but the revision should still be visible.

## What not to do

- Do not reject a whole idea when a smaller adjustment makes it credible.
- Do not add pessimism as a reflex; cost and opposition are calibrated counterweights, not quotas. Effective institutions, clean victories, and joy are valid when the canon supports them.
- Do not invent false precision to sound rigorous.
- Do not let a stage-gate become a bureaucratic ritual that blocks ordinary local additions; gates govern **stage advancement**, not every small lore detail.
- Do not advance a stage to satisfy suspense. Suspense comes from consequences within a layer, not from skipping layers.
