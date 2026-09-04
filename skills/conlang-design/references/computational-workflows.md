# Computational Conlang Workflows

Use these workflows when a conlang project needs rule-based candidate generation, phonotactic validation, multi-script conversion, constructive translation, portable data, or publication readiness. Treat computation as a **reproducibility aid**; it does not decide whether a language is grammatical, naturalistic, ethical, or artistically successful.

## Contents

1. [Choose the correct workflow](#choose-the-correct-workflow)
2. [Define a formal generation contract](#define-a-formal-generation-contract)
3. [Apply rewrite rules reproducibly](#apply-rewrite-rules-reproducibly)
4. [Validate phonotactics without overclaiming](#validate-phonotactics-without-overclaiming)
5. [Curate generated candidates](#curate-generated-candidates)
6. [Use constructive translation safely](#use-constructive-translation-safely)
7. [Package, exchange, and release project data](#package-exchange-and-release-project-data)
8. [Audit checklist](#audit-checklist)
9. [Provenance](#provenance)

## Choose the Correct Workflow

| Need | Use | Do not infer |
|---|---|---|
| Produce plausible form candidates | Generator contract, declared templates, ordered rewrite pipeline, curation log. | Semantic fit, etymology, or canon status from form shape alone. |
| Check an entered form | Inventory/template matcher plus boundary and normalization tests. | That a legal form is typologically or historically motivated. |
| Derive inflected or affixed forms | Typed morphological rule record and full derivation trace. | That a productive form has an attested sense or idiomatic construction. |
| Translate a sequence of sentences | Proposed queue with per-sentence introduction log. | That a recurring translation workaround is an approved grammar rule. |
| Share or migrate a project | Versioned canonical bundle and round-trip test. | That CSV retains all structured relations or rich textual analysis. |
| Publish a public demo or reference | Release readiness audit and privacy/provenance check. | That a read-only display is a complete language description. |

## Define a Formal Generation Contract

Define the following before generating. Preserve the exact configuration with the candidate batch.

| Element | Record | Test |
|---|---|---|
| Inventory | Stable segment IDs, display symbols, IPA where distinct, status, and group memberships. | Every generator unit resolves to a declared segment. |
| Tokenization | Longest-match, explicit segmentation, or other policy for multigraphs and complex graphemes. | Test every ambiguous string, such as a potential digraph versus two segments. |
| Normalization | NFC/NFD policy for stored forms, matching, and conversion. | Test precomposed/combining variants and mixed-script input. |
| Classes/groups | Named, extensional sets such as `vowels`, `stops`, or a language-specific class. | Test empty, overlapping, and changed groups deliberately. |
| Templates | Ordered slots, optionality, weights, and boundary policy. | Test positive edge cases and prohibited near-misses. |
| Preferences | Generation weight, frequency tendency, field balance, or style bias. | Keep preference separate from well-formedness. |
| Rewrites | Rule IDs, input/output, context, order, scope, and application semantics. | Keep representative traces for no-change, regular, and exceptional cases. |
| Filters | Illegal clusters, collisions, restricted forms, or reserved terms. | Record the reason for each rejection. |

Use a token sequence, not a raw character string, whenever inventory symbols may contain multiple characters. A raw string cannot always be segmented unambiguously after the fact. Preserve both tokens and the rendered form in derivation traces when practical.

Do not use a generic `C`/`V` generator class without a project definition. A class can represent a feature, a distributional category, or an author convenience; state which role it plays.

## Apply Rewrite Rules Reproducibly

Write each rule in a structured record and human-readable notation. Use ordered rule IDs instead of relying on prose order.

```yaml
id: R-014
status: productive
layer: phonology
input: {kind: group, value: nasals}
output: {kind: segment, value: ng}
left_context: []
right_context: [{kind: segment, value: k}]
application: simultaneous
self_feeding: false
order: 140
scope: word_internal
rationale: Place assimilation before dorsal stops.
tests: [T-031, T-032]
```

The rule record must distinguish **substitution**, **deletion**, and **insertion**. Represent deletion with a null/zero output and insertion as a rule whose input is a gap, not an ordinary segment. State word-boundary conditions explicitly instead of treating beginning/end of word as ordinary phonemes.

Choose and record an application model.

| Model | Meaning | Use carefully when |
|---|---|---|
| Simultaneous | Identify all sites against the pre-rule input, then replace them together. Outputs do not retrigger the same rule. | Preventing within-rule cascade and ensuring reproducibility. |
| Iterative | Apply a rule repeatedly until no eligible site remains or a declared limit is reached. | Modeling explicitly iterative processes; provide termination evidence. |
| Left-to-right / right-to-left | Rewrite one eligible site at a time in declared direction. | Rule order within a word is linguistically consequential. |
| Morphologically restricted | Apply only to a stated boundary, class, stratum, or paradigm cell. | Explaining alternations without falsely generalizing them. |

Record a trace for every consequential derivation: `underlying tokens → R-001 → intermediate tokens → R-014 → surface tokens → orthography`. Include non-application examples. A rule that has no documented environment is not an explanatory rule.

## Validate Phonotactics Without Overclaiming

Treat phonotactic validation as a **declared-language membership test**. It decides only whether a form can be segmented into legal declared structures under the stated policy.

1. Normalize the candidate and declared inventory according to the project policy.
2. Explore all legal tokenizations if symbols overlap or syllable boundaries are ambiguous.
3. Accept a word only if it can be segmented into one or more declared templates and it passes declared boundary/cluster filters.
4. Report the segmentation(s) or a useful failure reason when possible.
5. Keep template optionality separate from template weights: optionality affects legality; weight affects only how often generation chooses a path.

Test every new inventory or template with at least one positive and one negative case. Add tests for multigraphs, optional slots, word boundaries, cross-morpheme behavior, script conversion, Unicode normalization, and loans where in scope.

> A phonotactic pass does not show that a word is semantically suitable, historically plausible, free of collision, or appropriate for an approved lexicon.

## Curate Generated Candidates

Keep generated candidates in a queue. Do not mix them into the approved lexicon merely because they are legal.

| Stage | Required record | Promotion rule |
|---|---|---|
| Generated | Batch/configuration, raw output, tokenization, preliminary derivation. | Never auto-promote. |
| Filtered | Constraint results, template/rewrite result, collision check, rejection/hold reason. | Remove illegal or unsuitable candidates. |
| Reserved | Intended semantic field, register, and any collision caution. | Wait for a concrete need or decision. |
| Proposed | Form bundle, sense, POS, provenance, derivation, and usage example. | Require review and at least one test. |
| Approved | Canon decision or documented authority, stable ID, examples, and status. | Rerun affected audits after promotion. |

Curate candidates for sound, collision risk, semantic motivation, derivational transparency, cultural fit, register, and value to the completion test. Preserve rejections and reservations when they prevent repeated generation or explain later choices.

Use `templates/generation-validation-log.yaml` to record a batch, derivation, checks, review, and promotion decision.

## Use Constructive Translation Safely

Translation reveals gaps, but it must not silently mutate the language. When a translation introduces a word, sense, construction, or rule, record it as a **proposed delta** tied to the sentence and context.

1. Translate from the current approved snapshot and state its version.
2. Record each introduced item with source sentence, intended meaning, analysis, and why existing canon was insufficient.
3. Use proposed items consistently only within the declared working draft; distinguish them from approved forms in the output.
4. At a review checkpoint, cluster repeated deltas into candidate lexicon or grammar decisions.
5. Promote a delta only after checking phonology, morphology, syntax, semantics, and prior corpus examples.
6. Reanalyze earlier translations when a promotion changes the grammar or a previously proposed form.

Do not treat consistency across a short generated sequence as evidence that a rule is productive or well-integrated. Require a derivation or distributional account and regression examples.

## Package, Exchange, and Release Project Data

Use a JSON/YAML bundle as the structured canonical interchange, because it can preserve nested senses, derivations, relations, rules, tests, and decision IDs. Use CSV for tabular lexicon exchange only; document any fields it flattens or omits.

1. Include `schema_version`, language version, stable IDs, and status values in every canonical bundle.
2. Preserve native script, transliteration/romanization, IPA, and normalization policy separately when they differ.
3. Store status and provenance on lexemes, senses, rules, and examples as needed.
4. Export and import a copy before release; compare counts, stable IDs, relations, and approved states after round trip.
5. Retain an audit result and known-issues list alongside the versioned bundle.
6. Remove private notes, credentials, contributor data, and unpublished material before public sharing.

Use `templates/language-bundle-template.json` as a starter and `scripts/validate_language_bundle.py` for static structural checks. The validator is not a migration engine; write an explicit migration decision when changing a schema or rule interpretation.

## Audit Checklist

Before a major revision or release, answer each question with evidence IDs.

| Check | Evidence required |
|---|---|
| Constraint coverage | Every hard constraint has a pass/fail or exception note. |
| Dependency review | Changed artifacts and downstream tests are listed. |
| Tokenization and normalization | Ambiguous spellings and Unicode behavior have test results. |
| Rule semantics | Order, scope, contexts, and application model are explicit. |
| Candidate status | Generated/proposed material is distinct from approved canon. |
| Corpus coverage | Existing affected examples have been reanalyzed or marked pending. |
| Interchange integrity | Round-trip comparison documents preserved and lossy fields. |
| Publication safety | Shared material has appropriate scope, provenance, and privacy review. |

## Provenance

This original guidance adapts high-level workflow patterns from three public projects, without copying their code or product interfaces: ConlangCrafter’s staged construction and review pipeline; Glotbase’s lexicon, derivation, sentence, and interchange affordances; and conlang-studio’s token-aware phonological generation, rewrite, provenance, and phonotactics patterns. Consult the repositories directly for their own implementation details and licenses: [ConlangCrafter](https://github.com/morrisalp/ConlangCrafter), [Glotbase](https://github.com/thvtzy/Glotbase), and [conlang-studio](https://github.com/YangRCabrera/conlang-studio).
