# Domain Packs

The Living Canon core is universal: entities, claims, events, relationships, rules, decisions, sources, changes, snapshots, and audits. Use a domain pack only to add domain-specific fields and checks. Do not replace the core governance model or duplicate records merely because a domain has familiar labels.

## World bible pack

Use for fictional settings, lore bibles, roleplaying campaigns, games, alternate history, and shared universes.

| Add when it constrains work | Preferred record(s) | Key questions |
|---|---|---|
| Geography, ecology, travel, or jurisdiction matters | entity/location, rule, relationship/connection | What sustains settlement, access, food, defense, and communication? |
| Economy or material life matters | claim, rule/system, event, consequence | What is scarce, produced, moved, stored, taxed, or owed? |
| Factions or institutions act independently | entity/faction, actor-state, relationship | Who can authorize, coerce, administer, or legitimize action? |
| Culture, religion, or beliefs matter | entity, knowledge, claim, rule | What values, rituals, taboos, and metaphors arise from conditions? |
| Magic or technology matters | rule, entity, claim, event | What are prerequisites, access rules, bottlenecks, costs, failure modes, and second-order effects? |
| History matters | event, knowledge, consequence, branch | What caused this, what changed immediately, and what still surfaces? |

Model systems as interfaces instead of isolated lists. Geography, resources, institutions, culture, information, technology/magic, and infrastructure should create incentives and constraints for one another. Do not impose misery or failure as a quota: functioning institutions, cooperation, hope, and prosperity are valid when supported by the model.

Use the **world truth / actor knowledge / presented output** distinction whenever secrecy, unreliable narration, discovery, or player agency matters.

## Series and narrative continuity pack

Use for novels, screen stories, serial fiction, scripts, and character-centered projects. It works alongside a world bible but does not turn prose drafts into canon automatically.

| Need | Use | Keep distinct |
|---|---|---|
| Character identity and development | entity + attributes + event history | Author fact, character self-belief, and reader revelation |
| Plot thread | open-question or thread entity + events + consequences | Plan, draft event, and final published canon |
| Point-of-view knowledge | knowledge item | What the POV knows versus what the reader knows |
| Scene continuity | event or structured scene record | Scene intention versus irreversible world-state change |
| Theme/motif | entity/concept or claim | Interpretive reading versus authorial commitment |

Do not use an outline as a record of what has actually happened in a completed story. Mark future beats as provisional and published/locked material as approved only at the author’s direction.

## Research and evidence pack

Use for a persistent inquiry, literature review, investigation, technical analysis, or evidence ledger. Read any more specialized research skill when the task requires experiments, formal claims, or scholarly standards.

| Core record | Research extension |
|---|---|
| Source | Creator, date, method, locator, reliability, scope, license/permission, access date |
| Claim | Claim type, confidence, support, counterevidence, limitations, status |
| Event | Study, data collection, analysis run, finding, decision, publication update |
| Decision | Research question, inclusion/exclusion rule, methodology choice, rationale |
| Open question | Hypothesis, evidence gap, planned test, review date |

Never let an interpretation become a verified fact merely because it was summarized in a prior conversation. Maintain source support and counterevidence separately. Separate an external factual claim from a project decision about how to use it.

## Product and project pack

Use for planning, requirements, implementation decisions, operations, stakeholders, and evolving product knowledge.

| Need | Preferred record(s) | Example |
|---|---|---|
| Requirement or constraint | claim/rule + decision | Accessibility requirement or latency limit |
| Stakeholder and responsibility | entity + relationship + actor-state | Team, customer, owner, dependency |
| Risk or unresolved issue | consequence/open-question | Security risk, vendor uncertainty, blocked decision |
| Milestone or release | event + state-transition | Beta launch, incident, release decision |
| Architecture change | change-set + impact report | Database migration or API version change |

Treat product facts, decisions, assumptions, and future intentions as distinct records. A roadmap item is not a completed feature; a meeting statement is not necessarily an approved decision.

## Learning and personal knowledge pack

Use for concepts, reading notes, long-term inquiry, and a user-owned study system. Create records only with the user’s permission when material may be personal or sensitive.

| Need | Preferred record(s) |
|---|---|
| Concept | entity/concept + claim relations |
| Question | open-question with importance and revisit cue |
| Source note | source + claims supported |
| Understanding update | state-transition or decision noting confidence change |
| Study priority | actor-state-like planning record or tagged open question |

Avoid pretending to assess mastery from a single conversation. Store the user’s stated understanding, practice evidence, and questions separately.

## Creating a custom domain pack

Create a custom pack only after identifying a field or validation rule that repeatedly matters in the user’s domain. Keep it additive.

1. State the recurring decision or continuity failure the pack addresses.
2. Reuse core record types wherever possible.
3. Add only domain-specific fields, relationships, and validation checks needed to prevent that failure.
4. Define how the new records appear in the active snapshot and audit workflow.
5. Include one template and one compact example—never a giant taxonomy without a real use case.

A custom pack is successful when it makes subsequent recall, reconciliation, or decision-making more accurate than the core alone, not merely when it stores more fields.
