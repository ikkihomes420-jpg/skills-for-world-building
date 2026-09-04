# Interlinear Glossing and Example Data

Use this reference whenever producing a grammar, analyzed examples, corpus excerpts, or translation notes. Follow a consistent project convention. The Leipzig Glossing Rules provide widely used conventions for interlinear morpheme-by-morpheme glosses, but they do not determine the correct linguistic analysis; define project-specific labels and analytic choices explicitly.[1]

## Recommended Example Structure

Use four lines for consequential examples: object-language text, segmented/glossed text, idiomatic translation, and a short analytic note when ambiguity or a non-obvious choice matters.

```text
EX-001  na   mi=ke  tora-m  see-ta
        1SG  2SG=TOP bird-ACC see-PST
        “I saw the bird, as for you.”
        Note: The topical clitic marks a discourse frame, not the subject.
```

Replace the sample data with actual conlang forms. Give every example a stable ID so rules, lexicon entries, corpus texts, and regression tests can cite it.

## Segmentation and Glossing Conventions

| Notation | Use | Example | Constraint |
|---|---|---|---|
| Hyphen `-` | Segment a bound morpheme. | `see-PST` | Use a matching hyphen in form and gloss. |
| Equals sign `=` | Mark a clitic boundary. | `mi=TOP` | Use a matching equals sign in form and gloss. |
| Period `.` | Join distinct gloss labels for one form. | `GEN.PL` | Use for multiple label components, not a new morphological boundary. |
| Underscore `_` | Keep a multiword metalanguage gloss together. | `come_out` | Use only when the object-language form is not segmented. |
| Tilde `~` | Mark reduplication when relevant. | `RED~walk` | Define local use in the abbreviation key. |
| Angle brackets `⟨ ⟩` | Mark infix material when relevant. | `t⟨um⟩ak` | Use consistently or describe another notation. |
| Capitals | Abbreviate grammatical categories. | `PST`, `ERG`, `1SG` | Define uncommon labels once. |

Align the words and glosses vertically. Use an idiomatic free translation in quotation marks. State whether an example is attested in the conlang corpus, elicited for testing, a constructed paradigm example, or a hypothetical reconstruction.

## Maintain an Abbreviation Key

Adopt familiar abbreviations where they communicate clearly; define every uncommon, language-specific, or project-specific abbreviation.

| Label | Meaning | Status | Example ID |
|---|---|---|---|
| `ACC` | Accusative | Standard | EX-001 |
| `TOP` | Topic | Standard | EX-001 |
| `[CUSTOM]` | [Project-specific category] | Local | [ ] |

Avoid an abbreviation when a plain-language gloss is more informative, especially for a rare lexicalized element or a category whose analysis is uncertain. Glosses are aids to interpretation, not substitutes for grammatical explanation.[1]

## Example Quality Checks

| Check | Question | Repair if failed |
|---|---|---|
| Segmentation | Does each claimed morpheme correspond to the grammar and lexicon? | Correct the analysis or mark an opaque/lexicalized form. |
| Alignment | Do object-language units and gloss units align word by word? | Reformat the example; do not hide a mismatch. |
| Category labels | Are labels in the project key and used consistently? | Add/rename labels and update existing examples. |
| Translation | Is the free translation idiomatic without erasing relevant ambiguity? | Add a note or alternate translation. |
| Context | Does the example show the claimed meaning and conditions? | Add a contrast pair or a brief context. |
| Provenance | Is the data source/status clear? | Mark constructed, corpus, elicited, or reconstructed. |
| Regression | Does later grammar still generate and analyze the example? | Update canon or flag a deliberate historical/example-stage mismatch. |

## Use Contrast Sets

For each consequential category, include at least two examples that differ in the targeted variable. Do not claim that a marker means “past,” for instance, using only one sentence when it might encode perfective aspect, evidentiality, or narrative style.

| Claim | Contrast to add |
|---|---|
| Case marks an object | Intransitive clause, transitive clause, and a non-prototypical object. |
| Marker is obligatory | Context with the marker and comparable context without it. |
| Order signals focus | Neutral order, focused constituent, and a prosodic/particle alternative. |
| Category is an alignment split | One sentence on each side of the claimed conditioning environment. |
| Form is an allomorph | Roots that trigger and do not trigger the alternation. |

## Separate Four Layers of Analysis

Keep these separate in examples and grammar prose: the underlying representation, surface pronunciation, orthographic form, and glossed morphological analysis. If only one is relevant, omit the others rather than conflating them. This separation prevents spelling conventions from being mistaken for phonological rules and gloss labels from being mistaken for semantic definitions.

## References

[1] [Bickel, Comrie, and Haspelmath, *Leipzig Glossing Rules*](https://www.eva.mpg.de/lingua/resources/glossing-rules.php)
