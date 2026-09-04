# Advanced Conlang Design Framework

Use this reference when creating a language from scratch, rebuilding its architecture, or evaluating whether it behaves as a coherent language rather than an inventory of isolated features. Treat every choice as a decision about a communicative system used by speakers in a setting; do not add features solely because they are exotic.

## Contents

1. Project brief and design targets
2. Typological profile and system interfaces
3. Phonology, prosody, and phonotactics
4. Morphology, syntax, and semantics
5. Lexicon and word formation
6. Pragmatics, variation, and register
7. Writing systems and romanization
8. Diachrony and language families
9. Corpus-based testing

## 1. Project Brief and Design Targets

Establish the language's **design brief** before coining vocabulary or specifying paradigms. Record the intended use, desired degree of naturalism, speakers, historical period, genres of text, and practical constraints. A language can be an artlang, an auxiliary language, a fictional reconstruction, a naming language, a secret language, or a deliberately experimental system. These targets entail different trade-offs; avoid judging one by the standards of another.

| Design question | Record | Why it matters |
|---|---|---|
| Function | What will the language be used for? | Determines the needed corpus, lexicon, and documentation depth. |
| Naturalism target | Stylized, moderately naturalistic, or rigorously historical? | Determines whether to model irregularity, contact, and change. |
| Speakers and setting | Who uses it, with whom, and in what institutions? | Constrains registers, social variation, loan sources, and honorifics. |
| Time depth | A synchronic snapshot, a proto-language, or a family? | Determines whether sound changes and historical strata are necessary. |
| Aesthetic target | Which audible, visual, and rhythmic qualities are desired? | Guides frequency, syllable structure, prosody, and script without replacing analysis. |
| Non-negotiable constraints | What must be present, absent, or avoided? | Prevents later contradictions and accidental resemblance. |
| Proof of completion | What can the finished language express? | Supplies a realistic stopping rule. |

Write a one-paragraph **design promise**. For example: “Design a moderately naturalistic coastal trade language spoken by adult multilingual communities over three centuries. It should favor open syllables, productive compounding, and a three-way evidential contrast, while remaining usable for dialogue and short songs.” Revisit this statement when a proposed feature does not serve it.

## 2. Typological Profile and System Interfaces

Choose a small, mutually compatible typological profile before developing details. Do not treat typology as a shopping list. State the default pattern and then mark purposeful exceptions.

| Domain | Establish first | Check against |
|---|---|---|
| Morphological strategy | Analytic, agglutinative, fusional, templatic, polysynthetic, or a deliberate mixture | Word length, phonotactics, historical sources, and parsing burden |
| Alignment | Accusative, ergative, active–stative, tripartite, neutral, or split | Pronouns, case, agreement, relativization, and clause coordination |
| Clause organization | Default constituent order, head/dependent order, and verb phrase behavior | Adposition type, genitive order, adjective order, and subordinate clauses |
| Nominal system | Number, case, classifiers, possession, definiteness, and noun classes | Agreement targets, pronouns, demonstratives, and numeral phrases |
| Verbal system | TAM, polarity, mood, evidentiality, valency, agreement, and aspect | Negation, questions, imperatives, subordinate clauses, and discourse |
| Information structure | Topic, focus, contrast, and presentational strategies | Word-order flexibility, particles, prosody, and pronoun omission |

Make every interface explicit. If a language is head-final, test whether its adpositions, genitives, relative clauses, auxiliaries, and complementizers follow that tendency or are documented historical exceptions. If number is marked on nouns but not on pronouns, state the semantic condition. If an alignment split applies only in perfective clauses, show it in a paradigm and in examples.

Use a **feature budget**. Start with the small set of distinctions the language must make. Add a category only when its meaning, exponent, distribution, interaction with other categories, and at least two example contexts are defined. A category with no contrastive use is decoration, not grammar.

## 3. Phonology, Prosody, and Phonotactics

### 3.1 Define contrasts rather than lists

Record consonants and vowels in IPA, organized by phonological contrast. Specify marginal phonemes, allophones, length, nasalization, phonation, tone, stress, and syllabification separately. A spelling inventory is not a phoneme inventory.

| Layer | Specify | Test |
|---|---|---|
| Phonemic inventory | Contrastive consonants, vowels, suprasegmentals, and marginal units | Supply minimal or near-minimal pairs where feasible. |
| Allophony | Environment, surface realization, and ordering relative to other rules | Derive at least three representative surface forms. |
| Syllable structure | Onset, nucleus, coda, clusters, hiatus, and repair strategies | Test native roots, affix boundaries, and loanwords. |
| Prosody | Stress, tone, rhythm, intonation, and clitic behavior | Test statements, questions, focus, and morphologically long words. |
| Frequency and aesthetics | Common vs. rare phonemes and permitted word shapes | Compare a 30–50 word sample with the intended sound profile. |

Write phonological processes in an unambiguous form such as `n → ŋ / _ k, g` or prose with the same information. Identify whether a process is productive, lexicalized, morphologically restricted, historical, optional, or socially variable. Do not call a predictable alternation an exception.

### 3.2 Design phonotactics across boundaries

Specify legal native roots, affixed forms, compounds, proper names, and loans independently when they differ. State repair mechanisms: epenthesis, deletion, assimilation, metathesis, resyllabification, or preservation. Test every morphology rule against the phonotactic rules, not only isolated roots.

If using the PolyGlot-style generator, define categories only when they control frequency or a phonotactic class. Apply rewrite rules in a stated order, then test illegal clusters after rewriting. Treat generator output as candidates; curate each word for semantic fit, lexical collisions, and corpus balance.

### 3.3 Avoid false naturalism

Do not create “naturalism” by adding random difficult clusters, irregular spellings, or unpredictable exceptions. Naturalistic complexity has a source: regular sound change, analogy, borrowing, morphological leveling, register, or an explicitly limited lexical class. Document that source.

## 4. Morphology, Syntax, and Semantics

### 4.1 Build paradigms from meaning

For each grammatical category, define its **meaning**, **form**, **distribution**, **co-occurrence restrictions**, and **exceptions**. Distinguish obligatory marking from optional discourse-sensitive marking. Do not assign an English gloss to a form until its own semantic range is described.

| Category | Define before adding forms |
|---|---|
| Case or adposition | Core semantic role, syntactic role, animacy restrictions, spatial extension, and competing strategies |
| Number or classifier | Counting unit, collective/distributive reading, obligatoriness, and interaction with numerals |
| Tense/aspect/mood | Temporal reference, viewpoint, modality, evidentiality, and behavior in subordinate clauses |
| Agreement | Controller, target, features, hierarchy, domains, and default behavior |
| Valency operation | Input argument structure, output argument structure, affected case/agreement, and semantic effect |
| Derivation | Input category, output category, semantic contribution, productivity, and phonological alternation |

Construct a **paradigm grid** only after defining those categories. Mark impossible combinations, syncretisms, and periphrastic replacements intentionally. Trace forms through ordered morphological and phonological rules. When the language contains irregular classes, define the membership criterion and document the historical or analogical reason where appropriate.

### 4.2 Specify clauses before complex translation

Document the following in enough detail to write ordinary prose: intransitive and transitive clauses; pronouns and deixis; noun phrases; negation; yes/no and content questions; imperatives; possession; coordination; relativization; complementation; comparison; quotation; and at least one strategy for focus or topicalization. Add voice, switch reference, clause chaining, honorifics, or other advanced domains only when the design brief calls for them.

Use interlinear glossed examples whenever explaining grammatical behavior. Segment morphemes with hyphens, mark clitics with `=`, gloss grammatical morphemes in consistent capitals, and include a free translation. Use a glossing abbreviation only after defining it once in the grammar. Prefer two sharply contrasted examples over a paragraph of vague description.

```text
na   mi=ke  tora-m  see-ta
1SG  2SG=TOP bird-ACC see-PST
“I saw the bird, as for you.”
```

The sample is an illustration of format only; replace every form and gloss with the language's actual analysis.

### 4.3 Check semantic pressure points

Test differences that English or the user's language may conceal. Include demonstrations of deixis, inclusive/exclusive reference if relevant, evidentiality, possession, alienable versus inalienable reference if relevant, generic statements, habitual versus ongoing events, commands, politeness, information source, uncertainty, and counterfactuality. If the language lacks a distinction, demonstrate how speakers disambiguate pragmatically or by paraphrase.

## 5. Lexicon and Word Formation

Build the lexicon as a semantic network, not an alphabetical list. Establish core roots, function words, pronouns, productive derivation, compounds, and common idioms before adding large themed lists. Keep culture-specific concepts when the setting demands them, but do not assume every culture-specific word has a one-word English equivalent.

| Lexical layer | Document | Quality test |
|---|---|---|
| Core vocabulary | Stable concepts, function words, body, motion, perception, evaluation, relation | Support a basic conversation without recurrent placeholders. |
| Semantic fields | Kinship, landscape, material culture, trade, time, emotion, color, food, and ritual as needed | Map internal distinctions rather than copying English categories. |
| Word formation | Affixes, compounding order, reduplication, conversion, clipping, and borrowings | Derive several new forms without introducing ad hoc rules. |
| Collocation and idiom | Which verbs, classifiers, metaphors, and particles co-occur | Translate short natural passages without word-for-word calques. |
| Lexical history | Roots, loans, semantic shifts, and register | Explain nontransparent forms and competing synonyms. |

Give every entry a stable identifier or canonical headword and record: form, phonemic form, part of speech, concise definition, semantic field, morphology, valency if verbal, register, examples, derivation, etymology, and status (native, loan, archaic, coined, uncertain). Permit homophony only under an explicit policy, and distinguish exact homophones from orthographic or morphological collisions.

## 6. Pragmatics, Variation, and Register

A language becomes usable when it handles social meaning, not only propositional meaning. Define at least the default neutral register. Then decide whether the design brief requires formal, intimate, ritual, slang, child-directed, regional, heritage, or contact varieties. Do not invent variation as arbitrary substitution; anchor it in sound change, contact, prestige, taboo, identity, or genre.

Specify pragmatic particles, politeness strategies, address terms, deixis, evidential stance, turn-taking conventions, quotation, and common discourse connectors when relevant. Track whether a form is formal, familiar, ironic, archaic, pejorative, honorific, or neutral. Test the same request in two social contexts when the language distinguishes them.

## 7. Writing Systems and Romanization

Separate the phonological representation, native orthography, transliteration, and reader-facing romanization. A writing system may be phonemic, morphophonemic, etymological, defective, mixed, or artistic; state which it is. Define grapheme inventory, directionality, word boundaries, punctuation, capitalization, digits, transcription conventions, and the treatment of loans and names.

Order conversion rules from most specific to most general. Apply and test them on ambiguous sequences, morpheme boundaries, uppercase forms, punctuation, and Unicode normalization. Use one canonical Unicode encoding and state it. Never let visual resemblance substitute for code-point identity.

## 8. Diachrony and Language Families

Use diachrony to explain patterns, not to decorate the language with random changes. For a proto-language or family, establish relative chronology, sound changes, morphological reanalysis, analogical changes, borrowings, and contact strata. Apply a sound change regularly within its stated environment by default. Model exceptions through a documented mechanism such as lexical diffusion, analogy, morphological blocking, borrowing after the change, careful-speech restoration, or an earlier/later chronology; do not choose exceptions at random.

Use the notation `A > B / X_Y` for a sound change from A to B between X and Y. For each change, keep a ledger containing the input stage, environment, chronology, affected lexical class, output stage, exceptions, and rationale. Apply a proposed chronology to a test set containing roots, affixed forms, compounds, and loans. Recheck that later changes do not erase evidence needed for a claimed earlier stage.

Treat etymology as a directed graph. For every derived or borrowed form, store parent form, source language or internal stage, approximate date, intermediary if known, semantic path, and confidence. Reject cycles. Distinguish an attested source from an inspiration or a merely similar-looking form.

## 9. Corpus-Based Testing

Do not declare a language complete on the basis of tables. Maintain a small but growing corpus of analyzed texts: a self-introduction, dialogue, directions, procedural text, narrative, description, argument, and culturally central genre where relevant. Revisit old texts after each major grammar change.

Use a staged test suite:

1. **Form tests:** minimal pairs, phonotactic edge cases, affix boundaries, and orthographic conversions.
2. **Paradigm tests:** one regular root, one phonologically difficult root, one irregular class, and one loan or compound per major paradigm.
3. **Sentence tests:** assertions, questions, negation, commands, possession, transitivity, relative clauses, and information-structure contrasts.
4. **Discourse tests:** a dialogue and a connected narrative with anaphora, tense/aspect shifts, quotation, and topic management.
5. **Reverse tests:** translate or paraphrase the conlang text back into a metalanguage, then identify ambiguities, missing forms, and unintended meanings.

Record every repair as a decision in the canon, not merely as an edit to the immediate example. A reliable language is one whose rules continue to generate and analyze new text after the original designer has forgotten the details.
