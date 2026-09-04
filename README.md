# Skill Collection

A collection of agent skills in the standard [Anthropic Agent Skills](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview) format. Each skill lives in its own directory under [`skills/`](skills/) with a `SKILL.md` entry point plus its supporting `references/`, `scripts/`, and `templates/`.

## Skills

| Skill | Purpose |
| --- | --- |
| [ai-research-suite](skills/ai-research-suite/) | Umbrella/router skill for AI research and engineering. Bundles 98 preserved specialist skills (model architecture, training, fine-tuning, quantization, evaluation, serving, observability, writing, and more) plus an evidence-first research-governance layer and structured investigation workflow. |
| [conlang-design](skills/conlang-design/) | Design, expand, document, audit, test, translate, or evolve constructed languages as coherent, versioned communicative systems. Includes rule-based generators, glossing, diachrony, and language-bundle validation tooling. |
| [living-canon-os](skills/living-canon-os/) | Build, maintain, recall, audit, simulate, branch, and hand off durable living knowledge bases with transaction-governed canon changes and grounded retrieval. Suitable for world bibles, lore/canon systems, campaign state, continuity memory, and research knowledge bases. |
| [storycraft-os](skills/storycraft-os/) | Build, simulate, govern, audit, and publish coherent fictional worlds as durable causal systems: factions, cultures, economies, magic/tech systems, timelines, maps, campaigns, and persistent world state. |

## Layout

```
skills/
  <skill-name>/
    SKILL.md        # Entry point: how and when to use the skill
    references/     # Deep-dive documentation referenced by SKILL.md
    scripts/        # Optional validation/automation tooling
    templates/      # Optional starting templates and schemas
```

The collection contains 102 skills total: the 4 top-level skills above, 98 of which are specialist skills bundled inside `ai-research-suite/references/skills/`.

## Usage

Skills are plain directories with a `SKILL.md` entry point, so they work with any agent or tool that supports the Agent Skills convention:

- **Claude Code / Claude apps** — copy a skill directory into `~/.claude/skills/<skill-name>/` (personal) or `.claude/skills/<skill-name>/` (per-project), or point your agent at the `SKILL.md` directly.
- **Any other consumer** — read `skills/<skill-name>/SKILL.md` and follow its instructions; it will reference the files under its `references/` as needed.
- **ai-research-suite** — treat it as a router: read its `SKILL.md`, pick the narrowest relevant specialist from the catalog, then read that specialist's complete `SKILL.md` under `references/skills/<skill-name>/`.

## License

`ai-research-suite` declares `license: MIT` in its frontmatter. The other skills do not declare a license.