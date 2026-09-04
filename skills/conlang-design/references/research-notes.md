# Research Notes for Conlang-Design Upgrade

These notes support the 2026 major expansion of the `conlang-design` skill. Use them to guide reference selection and workflow design; they are not a substitute for reading the linked sources when their conventions are needed.

| Resource | Verified finding | Intended use in the skill |
|---|---|---|
| [WALS Online](https://wals.info/) | WALS is a structured database of phonological, grammatical, and lexical properties assembled from descriptive materials. It exposes features, chapters, language records, references, and downloadable data. It advises citing the individual chapter that supplies a feature. | Route typological exploration to specific feature chapters, and treat feature distributions as design inspiration rather than a prescriptive menu. |
| [Leipzig Glossing Rules](https://www.eva.mpg.de/lingua/resources/glossing-rules.php) | The rules establish widely used conventions for interlinear morpheme-by-morpheme glosses. They specify word-level alignment, matching morpheme boundaries with hyphens, clitics marked with equals signs, and uppercase abbreviated grammatical labels. The source explicitly allows justified local extensions and notes that glosses do not by themselves settle linguistic analysis. | Add a concise reference sheet and lintable conventions for interlinear examples; require a project-specific abbreviation key and preserve analytic uncertainty. |

The architecture should therefore add a dedicated typology-and-usage module, a detailed interlinear-glossing reference, explicit corpora and elicitation templates, machine-readable canon templates, and an opt-in static audit script. Keep these resources one level below `SKILL.md` to preserve progressive disclosure.

## Sources

1. Dryer, Matthew S. & Martin Haspelmath, eds. *WALS Online*, version 2020.4. https://wals.info/
2. Comrie, Bernard; Martin Haspelmath; and Balthasar Bickel. *Leipzig Glossing Rules*. https://www.eva.mpg.de/lingua/resources/glossing-rules.php

| [CLDF](https://cldf.clld.org/) | CLDF is a specification for interoperable cross-linguistic tabular data. Its design principles emphasize UTF-8 text, hand-editability, software-readability, explicit semantics, and CSV-based workflows for wordlists, structural datasets, and dictionaries. | Use CLDF-inspired, human-editable UTF-8 CSV/Markdown templates for optional lexicon, corpus, etymology, and feature data. Do not claim conlang projects are CLDF-compliant unless they implement the actual specification. |

3. Forkel, Robert et al. *Cross-Linguistic Data Formats*. https://cldf.clld.org/
