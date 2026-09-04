# Conlang Project Scales and Delivery Standards

Use this reference when deciding how much language architecture the request actually needs. Do not impose a full reference grammar on a user who needs ten coherent place names; do not treat a list of names as adequate when the user needs dialogue, translation, or a historical family.

## Scope Levels

| Level | Appropriate for | Required foundation | Minimum deliverables | Do not promise |
|---|---|---|---|---|
| **0. Naming system** | Personal names, place names, objects, factions, limited flavor text | Sound inventory, phonotactics, word shapes, name-formation rules, orthographic convention | Design brief, 20–50 generated/curated forms, formation table, pronunciation key | Fluent prose, full grammar, historical realism |
| **1. Fragment language** | Mottoes, ritual formulas, songs, short inscriptions, signature phrases | Level 0 plus pronouns/particles or a deliberately restricted construction set | Canon, phrase grammar, 30–100 entries, analyzed exemplar texts | Open-ended translation |
| **2. Dialogue language** | Fictional dialogue, tabletop roleplay, daily-use scenes, short letters | Level 1 plus core clause syntax, polarity, questions, TAM strategy, deixis, core lexicon, register policy | 150–500 entries, key paradigms, 10+ sentence tests, dialogue corpus | Full expressive coverage or a language family |
| **3. Documented synchronic language** | Reference grammar, sustained fiction, substantial translation, learning materials | Level 2 plus broad syntax, productive morphology, lexicon policy, writing policy, corpus/regression suite | Canon, grammar outline, structured lexicon, 500+ entries or defined derivational coverage, analyzed texts, audit | Historical depth unless separately designed |
| **4. Naturalistic synchronic language** | Linguistically plausible culture/language portrayal, advanced artlang | Level 3 plus motivated variation, contact effects, lexical strata, nontrivial distributional evidence, partial history | Everything in Level 3 plus change ledger, register/dialect notes, historical explanations for opaque patterns | Complete family reconstruction |
| **5. Historical family or reconstruction** | Proto-languages, daughters, diachronic narrative, comparative work | Level 4 plus a source stage, chronology, correspondence sets, daughter profiles, etymology graph | Proto-canon, ordered change ledgers, cognate sets, daughter derivations, comparative tests | Exhaustive natural-language documentation without a defined scope |

## Completion Gates

Before calling a level complete, meet its gate. A larger word list cannot compensate for a missing grammatical or testing foundation.

| Gate | Ask | Evidence |
|---|---|---|
| **Coherence** | Do all forms obey the declared sound, writing, and morphological rules? | Audit output and derivation traces. |
| **Coverage** | Can the language perform the communicative tasks promised in the brief? | Corpus texts, translation tests, gap log. |
| **Documentation** | Can another reader infer why forms behave as they do? | Canon, tables, examples, abbreviation key. |
| **Productivity** | Can the system generate a new, well-formed item without an ad hoc decision? | Novel forms traced through stated rules. |
| **Revision safety** | Can a later change be tested against existing material? | Stable IDs, corpus suite, change log. |
| **Historical plausibility** | If claimed, do opaque patterns have a timeline or socially motivated source? | Change ledger, etymology evidence, contact notes. |

## Choosing the Next Upgrade

Raise the level only when the intended use demands it. If users request “more depth,” identify their immediate bottleneck.

| Symptom | Upgrade first | Avoid |
|---|---|---|
| Names sound inconsistent | Phonotactics, word-shape distribution, and orthography | Inventing grammar the project will never use. |
| Translation feels like English with substitutions | Syntax, semantic ranges, discourse conventions, collocation | More inflection without a use case. |
| Paradigms look impressive but cannot make text | Clause syntax, function words, corpus testing | Adding another morphology dimension. |
| The language feels randomly complex | History, analogy, contact, register, and lexical strata | Random “irregularity.” |
| Revisions keep breaking earlier work | Canon versioning, IDs, change log, audit script, regression corpus | Retconning silently. |
| Daughters do not look related | Ordered sound changes, cognate sets, morphology inheritance | Ad hoc word replacement. |

## Upgrade Procedure

1. State the current project level and the target level.
2. List what already satisfies the target gate and what is missing.
3. Upgrade the missing subsystem with examples and tests.
4. Record every compatible change in the canon and regression log.
5. Stop when the target use case works; reserve further development for a new scope decision.
