---
name: conlang-design
description: >
  Design, expand, document, audit, test, translate, or evolve constructed
  languages as coherent, versioned communicative systems. Use for artlangs,
  auxiliary languages, naming systems, fictional language families, phonology,
  phonotactics, grammar, morphology, syntax, lexicon design, word generation,
  scripts, romanization, diachrony, corpus work, interlinear glossing,
  translation, language data, rule-based generators, and conlang workbench
  or release workflows.
---

# Conlang Design Toolkit

Build a language as a **documented, testable communicative system**, not a word list, a naming aesthetic, or a collection of unrelated typological features. Preserve canon, state assumptions, distinguish evidence from invention, and test every change across the systems it touches. Match the effort to the promised use: a naming system and a historically layered language family require different evidence.

## Core Operating Rules

1. **Route before generating.** Identify whether the work creates, expands, repairs, translates, historicizes, publishes, or merely names.
2. **Declare scope and constraints.** Set a project scale, a measurable completion test, and non-negotiable constraints before adding features.
3. **Maintain one source of truth.** Keep stable records for approved canon, decisions, lexicon, rules, examples, tests, and releases.
4. **Design interfaces, not isolated parts.** Check phonology against morphology, morphology against syntax, grammar against semantics, and all of them against corpus use.
5. **Separate state.** Label every item as **approved**, **proposed**, **deprecated**, **exception**, or **open**. Generated output is proposed by default.
6. **Record provenance.** Identify whether a form or rule is hand-created, generated, derived, inherited, borrowed, calqued, reconstructed, or otherwise sourced.
7. **Test productive claims.** Derive novel forms, analyze existing ones, and use connected text. A table without examples is not proof of a usable system.
8. **Do not silently retcon.** Preserve established forms and rules until a decision records the rationale, impact, migration, and regression tests.

## Route the Request and Load Only Relevant Resources

| Need | First action | Required result | Read / use |
|---|---|---|---|
| New language | Write a brief, constraints ledger, scale, and typological skeleton. | Coherent minimum viable language at the chosen scale. | `references/conlang-design-framework.md`, `references/project-scales.md` |
| Naming system / fragment | Limit expressive scope and define sound and formation rules. | Productive, pronounceable forms with declared limits. | `references/project-scales.md` |
| Existing-language expansion | Extract canon, dependencies, exceptions, and affected tests. | Compatible addition plus updated records and tests. | `references/data-management-and-auditing.md` |
| Audit / repair | Inventory forms, rules, examples, and contradictions. | Severity-ranked findings and non-destructive repair plan. | `references/workbench-artifacts.md` |
| Translation / text | Inventory available constructions and lexicon. | Idiomatic text, analysis where useful, and gap log. | `references/glossing-and-example-data.md`, `references/computational-workflows.md` |
| Historical / family design | Freeze source stage and relative chronology. | Ordered changes and traceable etymologies. | `templates/sound-change-ledger.md`, `templates/etymology-template.csv` |
| Generator, rewrite rules, or phonotactic checker | Declare formal inputs, semantics, and test cases before generating. | Reproducible candidates plus an acceptance/rejection log. | `references/computational-workflows.md`, `templates/generation-validation-log.yaml` |
| Structured workbench or release | Select a portable bundle and run the applicable audits. | Versioned package, audit result, and known-issues list. | `references/workbench-artifacts.md`, `templates/language-bundle-template.json`, `scripts/validate_language_bundle.py` |
| Typology or naturalism | Inspect cross-feature compatibility and evidence. | Bounded recommendation with dependencies. | `references/typology-and-naturalism.md` |
| Interlinear examples | Define abbreviations and analyze consequential examples. | Consistent glosses and example records. | `references/glossing-and-example-data.md` |

Use `templates/conlang-canon-template.md` for a substantial or continuing project. Use `templates/lexicon-template.csv` for a spreadsheet lexicon, `templates/corpus-and-test-suite.md` for regression material, and `templates/phonology-audit-config.json` for static spelling checks.

## Establish a Canon and Project Ledger

Use stable IDs: `L-0001` for lexemes, `S-0001` for senses, `EX-001` for examples, `D-001` for decisions, `C-001` for constraints, `R-001` for productive rules, `SC-001` for sound changes, `E-001` for etymology relations, `T-001` for tests, and `AUD-001` for findings. Retain unresolved fields explicitly; absence is not a decision.

| Record | Capture |
|---|---|
| Brief and constraints | Purpose, speaker/setting, naturalism target, aesthetic goals, exclusions, completion test, and non-negotiables. |
| Typological profile | Morphological strategy, alignment, clause organization, head/dependent tendencies, core categories, and marked patterns. |
| Phonology and writing | IPA contrasts, group/class membership, legal shapes, repairs, prosody, orthography, conversion, directionality, and normalization. |
| Grammar and rules | Meanings, exponents, distribution, ordering, conditions, productivity, exceptions, and derivation traces. |
| Lexicon | Form bundle, senses, POS, valency/class, derivation, register, provenance, status, history, and examples. |
| Evidence and release state | Minimal pairs, paradigms, corpus text, test outcomes, review records, open decisions, version, and known issues. |

Treat **constraints** as testable requirements, not aesthetic notes. For each `C-` record, state its source, scope, pass condition, and affected artifacts. Do not let a later form or generated candidate silently violate a hard constraint.

## Workflow A: Create or Rebuild a Language

Work through the following gates. Permit iteration, but record the changed decision and rerun downstream tests whenever a gate changes.

1. **Brief and profile gate.** Define the use case, scale, completion test, design promise, hard constraints, and a compatible typological skeleton. Exclude irrelevant feature creep.
2. **Phonology gate.** Declare contrasts, allophony, syllable structures, processes, prosody, spelling implications, and a 30–50-form curated sample. Verify legal forms, edge sequences, and a stated tokenization policy.
3. **Grammar gate.** Define meaning, form, distribution, co-occurrence restrictions, and exceptions before completing paradigms. Cover ordinary clauses before rare or decorative constructions.
4. **Lexicon and derivation gate.** Add function words, core roots, common constructions, productive formation, and semantic fields required by the completion test. Keep candidate output separate from approved entries.
5. **Text gate.** Test forms and paradigms in analyzed assertions, questions, negation, commands, possession, clause linking, dialogue, and use-case-specific text. Back-translate or paraphrase consequential examples.
6. **Release gate.** Freeze a version; audit applicable data; publish decision impacts, known contradictions, and open decisions. Do not release a clean machine report as proof of linguistic quality.

## Workflow B: Expand or Repair an Existing Language

1. Extract current canon, examples, lexicon records, rules, exceptions, constraints, and existing tests.
2. Build an impact map. A sound change affects spelling, morphology, corpus forms, and historical layers; a new case affects syntax, agreement, pronouns, and the lexicon.
3. Classify each finding as **error**, **underspecification**, **deliberate exception**, or **open decision**. Do not regularize data merely because it is inconvenient.
4. Propose the smallest compatible solution. Present alternatives when a choice changes typology, history, or user-facing aesthetics.
5. Update every affected record together, including decision, rule, lexicon, corpus, and release notes.
6. Reanalyze representative old examples and rerun affected tests. Retain superseded historical forms with provenance instead of overwriting them.

## Workflow C: Generate, Derive, and Curate Forms

Use a generator to explore a declared search space, not to assign meanings or create canon autonomously. Read `references/computational-workflows.md` before formalizing a generator, rewrite pipeline, phonotactic matcher, or constructive translation loop.

1. Declare the inventory, tokenization policy, natural classes/groups, legal templates, boundary behavior, normalization, and generation preferences. Keep **preference weights** separate from **legality conditions**.
2. Declare every rewrite with identifier, input, output, environment, order, scope, status, and application semantics. Specify whether a rule is simultaneous or iterative and whether an output can trigger the same rule.
3. Generate candidates with a reproducible configuration. Retain source batch, seed or method where available, and intermediate derivation steps.
4. Validate candidates against inventory, templates, rewrites, collision risk, spelling conversion, and the relevant constraints. Use token-aware analysis where multigraphs or ambiguous segmentation exist.
5. Curate for phonological fit, semantic fit, cultural motivation, redundancy, and corpus utility. Promote only after documenting a sense, provenance, status, and at least one usage test.

A form that fits templates is not thereby a justified word; a rule pipeline that runs is not thereby historically plausible.

## Workflow D: Translate and Produce Connected Text

1. Identify text type, register, audience, setting, and grammatical distinctions required by the source.
2. Inventory licensed constructions and lexical items. Treat a missing construction as a design decision, not an invitation to calque the source language.
3. Prefer idiomatic canon-licensed solutions. Provide interlinear analysis for consequential new forms.
4. Send newly introduced forms, meanings, and rules to the **proposed queue** with their source sentence and rationale. Do not update approved canon mid-translation without a recorded decision.
5. Back-translate or paraphrase to expose unintended readings, unexpressed distinctions, and register errors.
6. Promote recurring candidates only after a compatibility review and form/paradigm/corpus tests. Rerun prior translations if an approved update changes their analysis.

## Workflow E: Historical, Contact, and Family Design

1. Freeze the source stage, inventory, grammar, lexicon, and relative chronology.
2. Create an ordered ledger from `templates/sound-change-ledger.md`; state environment, scope, order, exceptions, and test set.
3. Explain apparent irregularity through analogy, borrowing, lexical diffusion, morphology, register, or chronology rather than random selection.
4. Trace a simple root, affixed form, compound, loan, and near-exception through each stage.
5. Record relationships in `templates/etymology-template.csv` and distinguish inherited, borrowed, derived, calqued, blended, speculative, and inspirational sources.

## Phonology, Grammar, and Lexicon Controls

Record a contrastive IPA inventory, not a spelling list. Separate phonemes from allophones; state whether length, tone, stress, nasalization, phonation, or gemination contrasts. Define syllable structure, processes, prosody, and repairs with unambiguous notation such as `n → ŋ / _ k, g`. Label every process as productive, lexicalized, restricted, historical, optional, or socially variable.

When spelling units can have multiple segmentations, declare the operational tokenization policy and test ambiguous sequences. Normalize equivalent Unicode forms before checking or converting them. Do not mistake a preferred generator weight, commonness heuristic, or script rendering rule for a phonological contrast.

For every grammatical category, define **meaning**, **form**, **distribution**, **co-occurrence restrictions**, and **exceptions**. Build paradigms after meanings are clear; mark blocked cells, syncretisms, periphrasis, and overrides intentionally. For every consequential rule chain, record `input → rule ID → intermediate output → surface form`.

Give lexemes a form bundle when relevant: native script, transliteration, reader-facing romanization, and IPA are distinct fields. Store multiple senses separately when a headword is polysemous. Give content verbs valency and construction notes; distinguish homophony, spelling collision, predictable inflectional identity, and near-collision.

## Examples, Tests, and Audits

Use `references/glossing-and-example-data.md` for interlinear conventions. Segment morphemes with hyphens, mark clitics with `=`, maintain a consistent abbreviation key, and attach an idiomatic translation. Existing analyzed text is a regression suite, not disposable illustration.

| Test level | Minimum purpose | Pass condition |
|---|---|---|
| Form | Inventory edges, templates, boundaries, rewrites, and spelling. | Output is legal or documented as an exception. |
| Paradigm | Regular, boundary-sensitive, class-conditioned, irregular, compound, and loan roots. | Rule order yields the intended form and analysis. |
| Sentence | Assertion, question, negation, command, possession, and clause linking. | Each marked choice has an interpretable function. |
| Discourse | Dialogue, narrative, or use-case-specific connected text. | Text works without recurring workaround patterns. |
| Reverse | Back-translation or paraphrase. | Ambiguities and gaps become visible and actionable. |
| Interchange | Export/import a project bundle without losing identifiers or relations. | Round trip preserves approved records and reports any lossy fields. |

Run `python scripts/audit_conlang.py lexicon.csv --config phonology-audit-config.json` for a CSV lexicon’s declared structural constraints. Run `python scripts/validate_language_bundle.py language.json` for a structured bundle. Use `--json` or `--strict` where appropriate. Read `references/workbench-artifacts.md` before releasing a structured project.

These checks find declared structural problems only. They do not prove grammaticality, IPA accuracy, naturalism, semantic suitability, historical plausibility, originality, or cultural appropriateness. Always follow a clean machine report with linguistic and corpus review.

## Deliver High-Quality Work

State assumptions and confidence where data are incomplete. Present rules before examples; use examples to demonstrate rather than replace rules. For substantial work, deliver an updated canon excerpt, concise rule tables, derivation traces, analyzed examples, lexicon records with provenance, an interface/compatibility note, test/audit result, and next-step test. For narrow work, deliver only the necessary work plus dependencies and open questions.

Avoid importing English structure without examination, collecting incompatible typological features, adding unexplained irregularity to imitate naturalism, treating generated candidates as canon, and presenting untested tables as a usable language. Favor explicit constraints, motivated complexity, stable documentation, curated generation, and corpus evidence.
