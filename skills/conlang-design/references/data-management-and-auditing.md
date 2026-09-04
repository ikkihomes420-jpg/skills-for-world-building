# Structured Data, Versioning, and Deterministic Audits

Use this reference for any continuing project that has more than a handful of lexical entries or more than one substantial grammar revision. Store data in formats a human can read and edit, while preserving stable identifiers and enough structure for automated checks. This follows the practical principles of structured linguistic data: UTF-8 text, hand-editability, software-readability, and clear data semantics.[1]

## Recommended Project Layout

```text
language-project/
├── canon.md                         # Design decisions and grammar source of truth
├── lexicon.csv                      # One row per lexical entry
├── phonology-audit-config.json      # Declared graphemes and simple constraints
├── corpus-and-test-suite.md         # Stable example IDs and regression records
├── etymology.csv                    # Optional: one row per source/relationship
├── sound-change-ledger.md           # Optional: ordered historical rules
└── releases/                        # Snapshots before structural revisions
```

Use this as a conceptual layout even when working in a single document or conversation. Do not claim that the files are CLDF-compliant unless they implement the relevant CLDF specification; these templates are merely **CLDF-inspired** for accessibility and auditability.[1]

## Stable Identifiers

Assign IDs that do not change when a spelling, gloss, or analysis changes. Avoid using the lexical form as an ID.

| Asset | Suggested pattern | Example |
|---|---|---|
| Lexical entry | `L-0001` | `L-0237` |
| Example | `EX-001` | `EX-042` |
| Phonological test | `P-001` | `P-014` |
| Morphology test | `M-001` | `M-008` |
| Decision | `D-001` | `D-017` |
| Sound change | `SC-001` | `SC-012` |
| Etymology relation | `E-001` | `E-104` |

Reference IDs in grammar prose, examples, corpus entries, and change logs. This permits revision without losing the ability to locate evidence.

## Lexicon Data Model

Start from `templates/lexicon-template.csv`. Retain the core columns even if others are blank until a project needs them.

| Column | Purpose | Requirement |
|---|---|---|
| `ID` | Stable lexical identifier | Required and unique. |
| `Form` | Canonical spelling/headword | Required; validate against spelling units. |
| `IPA` | Pronunciation or phonemic representation | Required when pronunciation matters. |
| `POS` | Part of speech or construction type | Required for grammar-aware lexica. |
| `Gloss` | Compact metalanguage label | Required; do not use as the full definition. |
| `Definition` | Sense, semantic range, and usage notes | Strongly recommended. |
| `Valency` | Argument structure or construction frame | Required for content verbs. |
| `Class` | Noun class, conjugation class, or other lexical class | Use only if governed by a defined system. |
| `Derivation` | Morphological analysis | Use whenever non-simple. |
| `Etymology` | Parent/source and history reference | Use for historical or contact claims. |
| `Register` | Neutral, formal, intimate, archaic, etc. | Use if socially marked. |
| `ExampleID` | Corpus/example evidence | Add as soon as a usable example exists. |
| `Status` | Controlled revision state | Required: `approved`, `provisional`, `deprecated`, or `exception`. |

## Etymology Data Model

Use one row per relationship, not one vague prose paragraph per word. Allow a word to have multiple sources only when the analysis explains the blend or multiple derivation.

| Column | Purpose |
|---|---|
| `RelationID` | Stable relation identifier, e.g. `E-001`. |
| `ChildID` | Derived/borrowed lexical entry ID. |
| `ParentForm` | Source form or parent entry ID. |
| `ParentStage` | Internal stage or external source language. |
| `Relationship` | Inherited, borrowed, calqued, derived, blended, analogical, etc. |
| `Chronology` | Approximate period and ordering. |
| `SemanticPath` | Meaning change or rationale. |
| `Confidence` | Certain, probable, speculative, or creative inspiration. |
| `Notes` | Evidence and unresolved questions. |

## Deterministic Audit Script

Use `scripts/audit_conlang.py` only after editing `templates/phonology-audit-config.json` for the actual language. The script is intentionally conservative: it checks declared columns, empty required values, duplicate IDs, duplicate forms, whitespace policy, undeclared spelling units, forbidden sequences, and controlled status values. It does **not** validate IPA, infer syllables, judge aesthetic quality, prove naturalism, or understand allomorphy.

```bash
python /path/to/audit_conlang.py lexicon.csv \
  --config phonology-audit-config.json
```

Use `--json` for a machine-readable report. The script returns exit code 1 for errors, and can treat warnings as failures with `--fail-on-warning`. Treat a clean report as a baseline check, not a linguistic endorsement.

## Change-Control Procedure

1. Create a snapshot before changing a structural rule, orthography, or large lexical stratum.
2. Create a decision record with a stable ID, rationale, affected systems, and required tests.
3. Apply the change to canon, data, and generation rules in the stated order.
4. Run the deterministic audit and all affected corpus/paradigm tests.
5. Record whether old examples were updated, marked historical, or deprecated.
6. Publish a new revision only after unresolved incompatibilities are visible in the issue log.

## Keep Data Semantics Explicit

Do not use a column named `Class`, `Tense`, or `Origin` without defining its values and scope in the canon. Do not place multiple unrelated meanings in a single free-text field if they must later be searched or audited. Prefer a small controlled vocabulary and a notes field for nuance.

## References

[1] [Cross-Linguistic Data Formats (CLDF)](https://cldf.clld.org/)
