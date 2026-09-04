# Worldbuilding Skill Collection

A collection of agent skills in the standard [Anthropic Agent Skills](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview) format. Each skill lives in its own directory under [`skills/`](skills/) with a `SKILL.md` entry point plus supporting `references/`, `scripts/`, and `templates/`.

The four skills are designed to work together on worldbuilding projects:

| Skill | Purpose |
| --- | --- |
| [storycraft-os](skills/storycraft-os/) | Build, simulate, govern, audit, and publish coherent fictional worlds as durable causal systems: factions, cultures, economies, magic/tech systems, timelines, maps, campaigns, and persistent world state. |
| [living-canon-os](skills/living-canon-os/) | Build, maintain, recall, audit, simulate, branch, and hand off durable living knowledge bases with transaction-governed canon changes and grounded retrieval: world bibles, lore/canon systems, campaign state, continuity memory. |
| [conlang-design](skills/conlang-design/) | Design, expand, document, audit, test, translate, or evolve constructed languages as coherent, versioned communicative systems. Includes rule-based generators, glossing, diachrony, and language-bundle validation tooling. |
| [worldbuilding-research](skills/worldbuilding-research/) | Evidence-first research for worldbuilding: structured specs, batched source collection, source records and claims with calibrated confidence. Produces records that import cleanly into the other three skills. |

## How they connect

```
worldbuilding-research ──source records + claims──▶ living-canon-os (canon storage)
        │                                            │
        └──typology/language data──▶ conlang-design  │
                                                     ▼
                                       storycraft-os (world systems + publication)
```

All four share a common record vocabulary: `source` records (`source_type`, `locator`,
`reliability`, `use_status`) and `claim` records (`status`, `support`, `confidence`), so
research output flows into canon storage and world bundles without reformatting.

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
- **Typical flow** — research real-world material with `worldbuilding-research`, store approved canon in `living-canon-os`, evolve systems and simulate with `storycraft-os`, and design languages with `conlang-design`.

## License

`conlang-design`, `living-canon-os`, and `storycraft-os` do not declare a license.
`worldbuilding-research` adapts governance concepts from the MIT-licensed
[Orchestra Research AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs)
(see its provenance note) and is offered under MIT.
