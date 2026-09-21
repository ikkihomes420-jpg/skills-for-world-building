# Stage-Gates

A stage-gate answers one question: **has the current layer earned enough capacity to support the next one?** This reference makes that question measurable instead of intuitive.

The units are deliberately ordinal and observable. Do not manufacture false precision: a threshold you cannot observe is not a threshold. Every score must cite a countable or falsifiable observation — a named practice, a person, a store, a repair, a record, a route, or a visible consequence.

> **Gate rule.** A layer advances when capacity is demonstrated, not when time has passed, population has grown, or the author wants the next era.

## The seven gate dimensions

Score each dimension `0`–`5`. Anchors are examples, not universal laws; adapt the units to the setting, but keep them observable.

| # | Dimension | 0 | 2 | 3 | 4–5 |
|---|---|---|---|---|---|
| 1 | **Repeatability** | A single feat or one lucky success | Attempted more than once, inconsistent | Done regularly by a recognized group | Predictable, scheduled, survives a bad attempt |
| 2 | **Labour & maintenance** | Nobody maintains it | Ad hoc repair by whoever is present | Named workers and a repair method | Dedicated maintenance, resupply, and a replacement pipeline |
| 3 | **Knowledge & skill** | Only the founder knows it | A few know it, no teaching | An apprenticeship, guild, or teaching practice | Skill is reproduced without the original teacher |
| 4 | **Continuity** | Ends with one person | An informal successor expectation | A rule, office, or custom names who carries it on | Succession works through a documented, tested handoff |
| 5 | **Failure & disagreement** | Failure is unhandled | Failure is handled arbitrarily | A stated fallback or dispute process exists | Failure/dispute is handled repeatedly and revised |
| 6 | **Beyond one household** | Effect stays inside one home | A neighbouring household is affected | Multiple households or a settlement depends on it | A region or a whole system depends on it |
| 7 | **Terminology honesty** | Label exceeds capacity (title without function) | Label is aspirational | Label matches demonstrated function | Label is precise and the world's own |

## The advance rule

Use explicit, freezeable criteria so "feels ready" cannot replace "is ready":

- **Hard dimensions:** 1 (repeatability), 2 (labour), 3 (knowledge), 5 (failure handling). If any of these is `≤ 1`, the gate **does not open** regardless of the others. A capability with no repeatability or no fallback is a story event, not infrastructure.
- **Minimum overall:** at least **five of seven** dimensions `≥ 3`, with **none at 0**.
- **Continuity (4):** required `≥ 3` if the new stage depends on the capability surviving its founder. If the founder is expected to die, leave, or lose legitimacy, dimension 4 must be `≥ 4`.
- **Reach vs control:** if the increment claims control (not just reach), dimensions 2 and 6 must both be `≥ 3`, and a jurisdiction record must exist.
- **Terminology (7):** must be `≥ 3` before any grand title enters canon. A title at `0`–`1` is a claim the world has not paid for.

Record the assessment with `templates/stage-gate.yaml`. A gate result is **evidence**, not canon: it informs the increment handoff but does not itself change the world.

## Worked gate assessment

A river settlement is moving from "shared services" toward "dependable exchange". The proposal: hold a **weekly market**.

| Dimension | Score | Observation |
|---|---|---|
| Repeatability | 3 | Neighbouring households already barter on a predictable day at the ford. |
| Labour & maintenance | 2 | No one is responsible for stalls, order, or waste; a bad week would scatter it. |
| Knowledge & skill | 2 | Two families know the customary measures; neither teaches them. |
| Continuity | 2 | The meeting survives only because one elder convenes it. |
| Failure & disagreement | 1 | Disputes over weight and debt are settled by whoever shouts hardest. |
| Beyond one household | 3 | Three villages and a set of river traders already depend on the ford. |
| Terminology honesty | 4 | Everyone calls it "the ford day", not a market. |

**Result: gate does not open.** Dimensions 2, 3, 5 are `≤ 2`, and hard dimension 5 is `1`. Capacity is close but unearned.

**Smallest credible increment:** establish a **common measure and a weigh-man** plus a **dispute custom** — a person, an artifact, and a stated rule. Score again next turn. The market then opens with a paid-for mechanism behind it rather than a label. This is exactly the `rule` records (`strength: default`, with scope and exceptions) that `storycraft-os` expects, and the `state-transition` that `living-canon-os` stores.

## Ladder rung indicators

Each rung is a capacity. The right column lists the **observable marker** that the rung is genuinely reached, and the failure sign that it is not.

### Settlement and political growth

| Rung | Observable marker | Failure sign |
|---|---|---|
| Landing or refuge | Repeated occupation of a specific site | Seasonal visits only |
| Repeated residence | Structures repaired across more than one season | Tents that are moved each visit |
| Household network | Reciprocal obligations between named households | One household supplies everything |
| Shared services | A well, mill, kiln, or store maintained by a group | Each household independently |
| Dependable exchange | A recognized measure and a regular meeting | Barter that depends on one broker |
| Regular adjudication | A named person or custom that settles disputes | Force decides every case |
| Market-town threshold | Traders arrive on schedule without being summoned; storage exists | Trade stops when the road floods or a broker dies |
| Durable polity | Taxation, jurisdiction, and succession function without the founder | Collapses on the founder's death |

### Security growth

| Rung | Observable marker | Failure sign |
|---|---|---|
| Self-protection | Household weapons and watch custom | No shared warning |
| Ad hoc escort | Neighbours travel together when needed | Travel only in safe seasons |
| Shared warrant | A stated right to act, with limits | Vigilantism |
| Named captain | A person responsible for organizing defence | Whoever is loudest |
| Common equipment custody | Shared gear with a maintenance owner | Gear rots after one use |
| Relay or resupply | Signals, mounts, or stores on a route | Patrols exhausted after one pass |
| Recurring circuit | A predictable schedule of protection | Permanent mobilization (unsustainable) |
| Permanent security institution | Officers, pay, records, and relief | A private household force wearing a public title |

### Religious growth

| Rung | Observable marker | Failure sign |
|---|---|---|
| Private devotion | Personal practice | — |
| Household practice | A shrine or rite maintained in the home | Imported wholesale, no local meaning |
| Shared gathering | A regular common rite | Depends on a single travelling teacher |
| Accommodation among rites | Coexistence rules between practices | Forced uniformity |
| Lay roles | Non-specialists perform parts of the practice | Total dependence on clergy |
| Recognized clergy/teachers | Training and recognition exist | Self-appointed only |
| Conversion networks | Routes and relationships spread the practice | Broadcast with no carriers |
| Institutional settlement presence | Buildings, welfare, records, property | A doctrine with no material base |

### Character growth

| Rung | Observable marker | Failure sign |
|---|---|---|
| Origin and memory | Concrete formative history | Backstory that only predicts greatness |
| Daily role | A job in the material economy | Importance asserted, not shown |
| Relationships | Named ties with obligations | Isolated protagonist |
| Competence and limitation | A skill **and** a limit | Flawless competence |
| Decision under pressure | A recorded choice with cost | Choices that always work out |
| Consequence | Effects on other named people | Effects on no one |
| Changed identity/reputation | A state transition others acknowledge | Reputation declared by the narrator |

### Technology and infrastructure

| Rung | Observable marker | Failure sign |
|---|---|---|
| Observed model | The community has seen the thing work | Never witnessed |
| Local adaptation | Materials and skills adapted to local reality | Frictionless copy |
| Prototype | One working instance | A sketch or plan |
| Failure and repair | A documented failure and a fix | First failure ends it |
| Shared technique | Multiple people can build it | One irreplaceable craftsperson |
| Repeatable production | Predictable output at a known cost | Batch of one |
| Maintenance institution | Named responsibility for upkeep and resupply | Runs until it breaks, forever |
| Wider adoption | Spreads with adaptation and second-order effects | Static once introduced |

### Communication, literacy, and language

| Rung | Observable marker | Failure sign |
|---|---|---|
| Spoken-only contact | Contact with other communities | — |
| Borrowed names/terms | Loanwords used consistently | Random foreign flavour |
| Shared trade jargon | A working pidgin/register at the meeting point | Full translation everywhere |
| Oral record specialists | Named people who hold and recite records | No memory carriers |
| Restricted literacy | A small literate class and a writing surface | Literacy without purpose |
| Scribal/chancery practice | Records kept for a reason (debt, law, faith) | Writing with nothing to record |
| Standardized written register | One spelling/grammar in use | Each scribe invents their own |
| Formal codification | A grammar/ruleset others follow | A conlang with no speakers behind the desk |

### Knowledge and information

| Rung | Observable marker | Failure sign |
|---|---|---|
| Direct observation | Personal witness | — |
| Word of mouth | Gossip and rumour networks | Perfect instantaneous knowledge |
| Standing witness/memory-keeper | A named holder of knowledge | No one remembers |
| Durable record | A written or physical archive | Knowledge dies with holders |
| Archive/register | Records retrievable later | Records that no one can find |
| Controlled circulation | Access rules and secrecy | Free-for-all knowledge |
| Public account | Circulated narrative | State monopoly with no leak |
| Systematic inquiry | Methodical investigation | Conclusion precedes method |

## Companion sanity checks

Cheap numeric cross-checks that catch the most common scale slips. Use them as questions, not formulas:

- **Subsistence margin:** can the settlement survive one failed harvest or one blocked route? If not, dimension 2 is low and the population is living on credit.
- **Administrative load:** one administrator can only track a limited number of households, obligations, and records. A "state" over a village has surplus administration and should say who pays for it.
- **Travel time:** multiply distance by the setting's plausible daily speed and season. If a decision requires information to arrive faster than travel allows, the timeline is broken.
- **Repair chain:** for any capability, ask how many people must be alive and present for it to continue. If the answer is "one", dimension 3 is `≤ 2`.
- **Founder dependency:** if removing one named person collapses the capability, dimension 4 is `≤ 2` and the title is premature.
- **Cost bearer:** name the household or group paying the cost. If no one is paying, the capability is being subsidized by narration.

## Anti-false-precision note

Ordinal scales and countable markers are useful; invented statistics are not. Prefer "three named households depend on the ford and a weigh-man holds the customary measure" over "71% market integration". When a real number is genuinely unknown, keep it as a range or an open question, and route it to `worldbuilding-research` if evidence could settle it.
