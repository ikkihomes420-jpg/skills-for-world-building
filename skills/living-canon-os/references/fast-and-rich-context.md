# Fast Updates and Rich Context

Use this reference whenever the user wants speed, exploratory discussion, more detail, or a more natural chat-native experience. The goal is **selective depth**: do less work for a small, safe update and preserve more detail when it materially affects later reasoning.

## Separate discussion from canon

Do not treat every idea, question, comparison, or hypothetical as a canon suggestion. Use these five levels deliberately.

| Level | Use when | Storage behavior | Canon effect |
|---|---|---|---|
| **Conversation only** | The user is casually exploring, debating, or thinking aloud. | Do not write a record unless asked. | None. |
| **Tracked discussion** | The user wants to retain a rich exploration, possibilities, alternatives, or reference notes. | Save a `discussion` record with its context and source locators. | None; explicitly `not-proposed`. |
| **Candidate** | The user says an idea may matter but has not chosen it. | Hold in the capture inbox or save as a provisional discussion. | None until promoted. |
| **Canon proposal** | The user asks to make, revise, or consider an enduring fact. | Create a proposed transaction and review diff. | None until approved. |
| **Approved canon** | The user explicitly accepts the transaction or supplies established canon. | Apply the transaction and rebuild derived views. | Targeted canonical update. |

Default to **conversation only** for ordinary discussion. Use **tracked discussion** only when the user says “keep this,” “track this,” “save these possibilities,” “hold onto this idea,” or otherwise indicates durable value. Use a canon proposal only when the user says or clearly means “make this true,” “add this to canon,” “update the bible,” “use this going forward,” or asks to review its canon impact.

A tracked discussion is valuable because it preserves a detailed exploration without creating pressure to decide. Use `capture_discussion.py` to store it under `discussions/`; set `detail_level` to `verbatim` for exact important wording, `detailed` for structured context, or `summary` only when the user explicitly wants a light note.

## Use the fast path by default

For a local addition or update, do not run a world-wide audit or read the entire archive. Follow this fast path:

1. Load `state/active-snapshot.md`.
2. Run an exact or narrow `query_canon.py` search for the named entity, rule, event, or thread; use `--hops 0` unless connected state clearly matters.
3. Read the matched target record and only its direct dependencies needed for the decision.
4. If the change is canon-level, draft a targeted transaction. If it is an exploratory matter, hold it in conversation or capture it as a discussion instead.
5. On approved changes, update only the affected records; rebuild the snapshot and derived index automatically.
6. Defer a full audit, broad impact report, reader export, or branch comparison until the user requests it or a defined deep-review trigger occurs.

This is faster because it operates on a small **working set**, not the entire world bible. The archive remains available when needed, but ordinary conversation does not pay the cost of rereading it.

## Escalate only when depth is justified

Use the deep path when a change can affect many records, breaks a cross-cutting rule, changes history, crosses branches, alters an active relationship, makes a new exception, introduces a likely duplicate identity, or materially affects player/author choice.

| Signal | Required depth |
|---|---|
| A new minor location, visual detail, or local preference | Fast path; often no durable record. |
| A new named entity with no major dependencies | Fast path plus an entity/provisional discussion record. |
| A major historical event, world rule, faction relationship, or cosmology rule | Targeted impact report and transaction review. |
| A retcon, branch change, identity merge/split, or revision to an invariant | Full impact analysis, integrity audit, and explicit change set/branch process. |
| A dense requested analysis of a known subject | Query with `--detail context` or `--detail full`, then load only linked records that answer the question. |

## Preserve richness without context flooding

A summary is an index, **not a substitute for detail**. For subjects that need nuance, retain three layers in the same record or in linked records:

| Layer | Intended size | What it preserves | When to load it |
|---|---|---|---|
| **Brief** | One or two sentences | Identity and immediate relevance. | Ordinary chat continuity. |
| **Context** | Several precise paragraphs, lists, exceptions, and motivations. | The detail needed to reason correctly. | Detailed questions, canon extension, simulation, or audit. |
| **Source detail** | Verbatim conversation material, citations, excerpts, competing accounts, and rationale. | Exact evidence and non-lossy history. | Disputes, retcons, close analysis, or “why do we know this?” |

Use `summary` for the brief layer. Use fields such as `detail`, `details`, `context`, `notes`, `attributes`, `exceptions`, `causes`, `effects`, and linked knowledge records for context. Preserve exact conversation wording or imported material in an evidence/source record when wording itself matters. Never overwrite rich context with a new summary merely to keep the snapshot shorter.

Use `query_canon.py --detail brief` for ordinary recall, `--detail context` for nuanced work, and `--detail full` when the user explicitly needs the complete selected record. These levels apply to **selected records only**; full detail must never mean “load the entire archive.”

## Organize by role and state, not only by folders

Use folders to keep files approachable, but use IDs, tags, links, statuses, branches, and active state for retrieval. A record can be simultaneously a location, a sacred site, a trade hub, a factional flashpoint, and a setting for an event. Do not force it into one conceptual drawer.

Maintain these organization layers:

| Layer | Function |
|---|---|
| **Registry folders** | Human-friendly storage by broad kind, such as entities, events, rules, claims, and discussions. |
| **Stable IDs and aliases** | Identity across renamed terms, titles, historical names, and shorthand. |
| **Tags and scopes** | Flexible grouping by era, region, theme, campaign, POV, faction, or research domain. |
| **Relationships and dependencies** | Causal and semantic connective tissue. |
| **Active snapshot** | What matters now. |
| **Discussion archive** | Valuable context that is not current canon. |
| **Transaction log** | Why authoritative state changed. |

## Chat behaviors to use

Keep visible interruptions rare. Use short, clear prompts only when they have value.

> “We are exploring possibilities here. I will not treat any of these as canon unless you ask me to.”

> “This seems worth keeping for later, but it does not need a canon ruling. Would you like it saved as a detailed discussion note?”

> “This changes an established rule. I can make a focused canon proposal using only the affected rule, event, and faction records; a full audit is not necessary unless you want one.”

> “I have the brief version of this subject. Because you are asking about its political logic, I will load its detailed context and directly linked records rather than summarize it further.”

## Quality gate

Before finalizing any update or response, verify that the chosen depth matches the user’s intent. Do not perform global analysis for a local change. Do not reduce a detailed record to a single summary if its exceptions, motivations, causal links, or exact wording matter. Do not promote exploratory material to a canon proposal without a clear signal. Do not allow the desire for speed to bypass an approval requirement for an established canon change.
