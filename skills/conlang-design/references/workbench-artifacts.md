# Language Workbench Artifacts

Use these compact artifacts when a language will be extended, audited, translated, generated, exchanged, or published. Store the canonical version in JSON or YAML and keep identifiers stable after first approval. Use CSV as a lexicon-oriented view, not as the sole source of truth for a rich project.

## Contents

1. [Language manifest and constraints](#1-language-manifest-and-constraints)
2. [Phonology and writing contract](#2-phonology-and-writing-contract)
3. [Lexicon and sense records](#3-lexicon-and-sense-records)
4. [Grammar, morphology, and rewrite rules](#4-grammar-morphology-and-rewrite-rules)
5. [Generator configuration and curation](#5-generator-configuration-and-curation)
6. [Corpus, tests, and translation deltas](#6-corpus-tests-and-translation-deltas)
7. [Audits and releases](#7-audits-and-releases)
8. [Compatibility notes](#compatibility-notes)
9. [Provenance](#provenance)

## 1. Language Manifest and Constraints

```yaml
schema_version: 1.1
language:
  id: lower-kebab-case
  name: Display Name
  status: draft | active | frozen | released
  version: 0.1.0
  purpose: dialogue | fiction | naming | translation | auxiliary | historical
  design_promise: One paragraph stating the design and hard limits.
  canonical_sources: [canon.md, language.json, corpus.md]
  unresolved: []
  decisions: [D-001]

constraints:
  - id: C-001
    statement: The language contrasts exactly three oral vowel qualities.
    source: project brief
    status: approved
    scope: [phonology, lexicon, generator]
    pass_condition: Every approved phonemic form uses only /i a u/ as an oral vowel.
    exceptions: []

profile:
  morphology: analytic | agglutinative | fusional | templatic | mixed
  alignment: nominative-accusative | ergative-absolutive | active-stative | other
  clause_order: SVO | SOV | VSO | flexible
  head_direction: initial | final | mixed
  evidence: [D-002, EX-001]
```

Treat `schema_version` as the artifact structure version and `language.version` as the published language snapshot. Increase the latter for content decisions; make and document a migration when a semantic schema change prevents an older reader from interpreting the bundle safely.

## 2. Phonology and Writing Contract

```yaml
phonology:
  normalization: NFC
  tokenization: longest_match
  phonemes:
    - id: ph-t
      symbol: t
      ipa: t
      status: approved
      generator_weight: 1.0
      groups: [stops, coronals]
  groups:
    - id: stops
      members: [ph-p, ph-t, ph-k]
  syllable_templates:
    - id: SYL-001
      slots:
        - {group: stops, optional: true}
        - {group: vowels, optional: false}
        - {group: nasals, optional: true}
      generation_weight: 1.0
  illegal_clusters: [tl#, sr#]
  processes: [R-014]
  stress_or_tone: null

writing:
  native_script: null
  native_form_field: native_form
  phonemic_layer: IPA
  orthography_layer: romanization
  conversion_order: []
  unicode_normalization: NFC
  direction: LTR
  boundary_conventions: []
```

Use opaque IDs for segments and group members when multigraph symbols or script changes could make a rendered string ambiguous. A generator weight biases selection; it never establishes legality. Store `native_script`, transliteration, reader-facing romanization, and IPA as separate layers when they differ.

## 3. Lexicon and Sense Records

```yaml
lexicon:
  - id: L-0001
    headword: form
    forms:
      native: null
      transliteration: form
      romanization: form
      ipa: /form/
    tokenization: [ph-f, ph-o, ph-r, ph-m]
    status: proposed | approved | deprecated | exception | open
    provenance:
      type: hand_created | generated | derived | inherited | borrowed | calqued | reconstructed | other
      source: GEN-2026-01 | D-004 | null
      note: null
    senses:
      - id: S-0001
        pos: noun
        gloss: brief English gloss
        definition: Precise meaning, scope, and usage.
        semantic_field: [kinship]
        register: neutral
        valency: null
        examples: [EX-001]
    morphology:
      root: form
      derivation: []
      irregular_forms: []
    relations:
      synonyms: []
      antonyms: []
      etymology_parent: null
    tags: []
    notes: null
```

Keep the **proposed queue** separate from approved lexemes. A generated form becomes vocabulary only after semantic assignment, collision review, a provenance record, and at least one usage test. Retain multiple senses separately; do not force a polysemous form into a single part-of-speech/gloss pair.

## 4. Grammar, Morphology, and Rewrite Rules

Write category meaning before a paradigm. Use a separate identifier for every ordered operation.

```yaml
paradigms:
  - id: P-VERB-FINITE
    applies_to: [verb]
    dimensions:
      - name: tense
        values: [nonpast, past]
        required: true
    blocked_cells: []
    overrides: []

morphology_rules:
  - id: M-PAST-01
    applies_to: [verb]
    when: {classes: [], match: ".*"}
    transform: "$ -> -ta"
    order: 10
    status: productive
    rationale: Regular past exponent.
    tests: [T-021]

rewrite_rules:
  - id: R-014
    layer: phonology
    input: {kind: group, value: nasals}
    output: {kind: segment, value: ph-ng}
    left_context: []
    right_context: [{kind: segment, value: ph-k}]
    application: simultaneous
    self_feeding: false
    order: 140
    scope: word_internal
    status: productive
    rationale: Place assimilation before dorsal stops.
    tests: [T-031, T-032]
```

Distinguish substitution, deletion, and insertion. Represent deletion with `output: null`; represent insertion with `input: {kind: gap}` and a non-null output. State word boundaries, optional contexts, class/group resolution, and interaction with morphology. Record whether each rule is **simultaneous**, **iterative**, or directionally sequential, and whether its outputs may feed the same rule.

Capture consequential derivations as `input → rule ID → intermediate output → next rule ID → surface form`. Mark a form as an exception only after testing whether a class-conditioned, historical, or stratal account explains it.

## 5. Generator Configuration and Curation

```yaml
generators:
  - id: GEN-2026-01
    source_version: 0.2.0
    method: rule_based | assisted | manual_batch
    seed: null
    tokenization: longest_match
    templates: [SYL-001, SYL-002]
    filters:
      illegal_clusters: [tl#, sr#]
      reserved_forms: []
    rewrite_order: [R-014, R-015]
    preference_note: Earlier segments are favored; weights do not define legality.

candidates:
  - id: GC-0001
    form: lani
    tokens: [ph-l, ph-a, ph-n, ph-i]
    source: GEN-2026-01
    trace: []
    constraint_results: [{constraint: C-001, result: pass}]
    verdict: hold | reject | reserve | propose | promote
    reason: Near-collision with lan; reserve for kinship field.
```

Treat generation as search-space exploration. Generate from declared configuration, validate against phonotactics and constraints, then curate for collision, semantic fit, cultural motivation, and corpus value. Preserve rejected/reserved candidates if they guide future curation.

## 6. Corpus, Tests, and Translation Deltas

```yaml
corpus:
  - id: EX-001
    status: approved
    text: Example target-language sentence.
    gloss: morph-by-morph analysis
    translation: Idiomatic translation.
    tests: [T-051]

tests:
  - id: T-031
    level: phonology
    input: [ph-n, ph-k]
    expected: [ph-ng, ph-k]
    result: pass | fail | pending
    evidence: R-014

translation_deltas:
  - id: TD-001
    source_example: EX-042
    approved_snapshot: 0.3.0
    type: lexeme | sense | construction | rule
    proposal: Proposed item and analysis.
    status: proposed | rejected | promoted
    decision: null
```

Maintain a compact analyzed corpus that grows after structural changes. Old examples are regression tests: do not silently update their form or meaning. Track translation-introduced material as a proposed delta until an explicit decision promotes it.

| Test family | Minimum cases | Capture |
|---|---:|---|
| Phonology | 10 | Edge clusters, tokenization, rewrites, loans, boundaries, normalization. |
| Morphology | 8 per paradigm | Regular, boundary-sensitive, class-conditioned, irregular, compound, loan. |
| Syntax | 12 | Assertion, question, negation, command, possession, and clause linking. |
| Orthography | 10 | Ambiguous sequences, capitalization, punctuation, Unicode, directionality. |
| Discourse | 3 texts | Dialogue, narrative, and a use-case-specific text. |
| Interchange | 1 per release | Export/import counts, IDs, statuses, and lossy fields. |

## 7. Audits and Releases

```yaml
audit:
  id: AUD-001
  scope: full_language | lexicon | paradigm | orthography | corpus | release
  language_version: 0.4.0
  findings:
    - id: AUD-002
      severity: blocker | major | moderate | minor
      type: contradiction | underspecification | deliberate_exception | open_decision
      evidence: [L-0034, EX-002]
      impact: What breaks or becomes ambiguous.
      repair_options: []
      recommended_action: null
  result: pass | conditional_pass | fail

release:
  language_version: 0.4.0
  bundle_schema_version: 1.1
  source_snapshot: main
  audits: [AUD-001]
  known_issues: []
  round_trip: pass | fail | not_run
  public_scope: private | shared | public_read_only | public_editable
```

Prioritize contradictions that block generation, parsing, or translation. Preserve attested or author-approved forms until a deliberate decision records the repair. A clean structural audit does not establish linguistic validity.

## Compatibility Notes

Legacy bundles using `phonology.phonemes` as plain strings, `profile`, `writing`, `lexicon`, `rules`, and `corpus` remain valid inputs for the local validator. The richer 1.1 structures are recommended rather than mandatory, except in a project that declares a 1.1-specific completion or release requirement. Convert legacy structures deliberately; do not rewrite an active canon solely to adopt a new schema.

Use `templates/language-bundle-template.json` for a new 1.1-style project, `templates/lexicon-template.csv` for spreadsheet workflow, and `templates/generation-validation-log.yaml` for derivation and promotion reviews.

## Provenance

This original schema is informed by the public [PolyGlot toolkit](https://github.com/DraqueT/PolyGlot) and by workflow patterns observed in [ConlangCrafter](https://github.com/morrisalp/ConlangCrafter), [Glotbase](https://github.com/thvtzy/Glotbase), and [conlang-studio](https://github.com/YangRCabrera/conlang-studio). It is an independently authored interoperability and audit schema, not a reimplementation of any referenced application.
