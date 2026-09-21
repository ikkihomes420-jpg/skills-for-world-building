# Worldbuilding Skill Collection

A collection of agent skills in the standard [Anthropic Agent Skills](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview) format. Each skill lives in its own directory under [`skills/`](skills/) with a `SKILL.md` entry point plus supporting `references/`, `scripts/`, and `templates/`.

The five skills are designed to work together on worldbuilding projects:

| Skill | Purpose |
| --- | --- |
| [gradual-worldbuilding](skills/gradual-worldbuilding/) | The pace-and-method layer: develop worlds in earned layers instead of rushing to an empire, endpoint, or encyclopedia. Governs sequencing, stage-gates, development ladders, and depth, with measurable capacity thresholds, and hands each increment to the other skills in their own record formats. |
| [storycraft-os](skills/storycraft-os/) | Build, simulate, govern, audit, and publish coherent fictional worlds as durable causal systems: factions, cultures, economies, magic/tech systems, timelines, maps, campaigns, and persistent world state. |
| [living-canon-os](skills/living-canon-os/) | Build, maintain, recall, audit, simulate, branch, and hand off durable living knowledge bases with transaction-governed canon changes and grounded retrieval: world bibles, lore/canon systems, campaign state, continuity memory. |
| [conlang-design](skills/conlang-design/) | Design, expand, document, audit, test, translate, or evolve constructed languages as coherent, versioned communicative systems. Includes rule-based generators, glossing, diachrony, and language-bundle validation tooling. |
| [worldbuilding-research](skills/worldbuilding-research/) | Evidence-first research for worldbuilding: structured specs, batched source collection, source records and claims with calibrated confidence. Produces records that import cleanly into the other skills. |

## How they connect

`gradual-worldbuilding` is the **layer above** the other four. It does not store, simulate, research, or design anything itself; it decides *when a world may advance* and *what evidence it must show*, then writes the result in the record vocabulary the owning skill already uses.

```
                        gradual-worldbuilding
                    (pace · stage-gates · ladders)
                                │
        ┌───────────────┬───────┴────────┬──────────────────┐
        ▼               ▼                ▼                  ▼
worldbuilding-research  conlang-design  living-canon-os  storycraft-os
   source + claims       languages       canon storage    systems + sim
        │                   │            + transactions   + rules + release
        └───────source/claims──┴───────────────┬──────────┘
                                                ▼
                                     world rule / change set / consequence
```

Reading the flow:

- `worldbuilding-research` supplies `source` records and calibrated `claim`s for any plausibility question.
- `conlang-design` supplies the language as a testable system; the world-facing constraints it must satisfy are mirrored as `world-rule`s.
- `living-canon-os` stores approved canon, governs changes as transactions, and keeps a rebuildable active snapshot.
- `storycraft-os` holds the systems, rules, factions, simulation, and publication layer.
- `gradual-worldbuilding` sequences all of it and records each increment as a `state-transition`, `change-set`, `consequence`, `claim`, and `decision`/`open-question` bundle.

All five share a common record vocabulary: `source` records (`source_type`, `locator`, `reliability`, `use_status`), `claim` records (`status`, `support`, `confidence`, `truth_status`), and the status/authority/branch fields used across the suite — so output flows between them without reformatting.

## Layout

```
skills/
  <skill-name>/
    SKILL.md        # Entry point: how and when to use the skill
    references/     # Deep-dive documentation referenced by SKILL.md
    scripts/        # Optional validation/automation tooling
    templates/      # Optional starting templates and schemas
```

## Usage

Skills are plain directories with a `SKILL.md` entry point, so they work with any agent or tool that supports the Agent Skills convention:

- **Claude Code / Claude apps** — copy a skill directory into `~/.claude/skills/<skill-name>/` (personal) or `.claude/skills/<skill-name>/` (per-project).
- **Any other consumer** — read `skills/<skill-name>/SKILL.md` and follow its instructions; it will reference the files under its `references/` as needed.
- **Typical flow** — pace the project with `gradual-worldbuilding`, research real-world material with `worldbuilding-research`, store approved canon in `living-canon-os`, evolve systems and simulate with `storycraft-os`, and design languages with `conlang-design`.

## License

`conlang-design`, `living-canon-os`, and `storycraft-os` do not declare a license.
`gradual-worldbuilding` and `worldbuilding-research` adapt governance concepts from the
MIT-licensed [Orchestra Research AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs)
and are offered under MIT.
