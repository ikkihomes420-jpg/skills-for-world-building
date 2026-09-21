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

## Install

This repository is **public**. No token, GitHub App, or authentication is required to read it — see [If an agent says the repo is private](#if-an-agent-says-the-repo-is-private) if something claims otherwise.

Skills are plain directories with a `SKILL.md` entry point, so they work with any agent or tool that supports the Agent Skills convention.

> ### Which URL does your tool want?
>
> **If it asks for a repository**, give it the repository URL:
>
> ```
> https://github.com/ikkihomes420-jpg/skills-for-world-building
> ```
>
> **If it asks for a file** — a `SKILL.md` to fetch over HTTP — give it one of the
> `raw.githubusercontent.com` links in section 4 below.
>
> These are **not interchangeable**. Pasting a *raw file URL* into a *repository*
> field makes the tool try to `git clone` a text file; GitHub answers
> `404: Not Found`, and the client reports it as
> *"Could not access repository … This may be a private repository."*

### 1. Skillset apps (SuperAgent, and tools that read a skillset index)

These clone the repository and read **`index.json` at the repo root**, which lists
every skill and the path to its `SKILL.md`. Add the repository URL:

```
https://github.com/ikkihomes420-jpg/skills-for-world-building
```

Leave the token field empty — the repository is public.

> **Keep `index.json` current.** It is the source of truth these tools read. When
> you add, rename, move, or re-version a skill, update its entry in `index.json`.
> A `path` must point at that skill's `SKILL.md` file. Entries that fail to parse
> are dropped silently, so a stale entry makes a skill vanish from the app with no
> error shown.

### 2. Claude Code — plugin marketplace (one command)

```
/plugin marketplace add ikkihomes420-jpg/skills-for-world-building
/plugin install worldbuilding-suite@worldbuilding-skills
```

Installs all five skills at once. This works because the repository ships `.claude-plugin/marketplace.json`.

### 3. Claude Code / Claude apps — copy the directories

```bash
git clone https://github.com/ikkihomes420-jpg/skills-for-world-building.git

# personal (all projects)
mkdir -p ~/.claude/skills && cp -r skills-for-world-building/skills/* ~/.claude/skills/

# or per project
mkdir -p .claude/skills && cp -r skills-for-world-building/skills/* .claude/skills/
```

### 4. Agents that fetch a single file (raw URL) — *not* a repository URL

Point it directly at the `SKILL.md` it needs. All five verified live and public.
Use these only in tools that fetch a **file**; for tools that take a **repository**,
use the repo URL above.

| Skill | Raw `SKILL.md` |
| --- | --- |
| gradual-worldbuilding | `https://raw.githubusercontent.com/ikkihomes420-jpg/skills-for-world-building/main/skills/gradual-worldbuilding/SKILL.md` |
| storycraft-os | `https://raw.githubusercontent.com/ikkihomes420-jpg/skills-for-world-building/main/skills/storycraft-os/SKILL.md` |
| living-canon-os | `https://raw.githubusercontent.com/ikkihomes420-jpg/skills-for-world-building/main/skills/living-canon-os/SKILL.md` |
| conlang-design | `https://raw.githubusercontent.com/ikkihomes420-jpg/skills-for-world-building/main/skills/conlang-design/SKILL.md` |
| worldbuilding-research | `https://raw.githubusercontent.com/ikkihomes420-jpg/skills-for-world-building/main/skills/worldbuilding-research/SKILL.md` |

### 5. Clone or download

- Clone — `https://github.com/ikkihomes420-jpg/skills-for-world-building.git`
- Zip — `https://github.com/ikkihomes420-jpg/skills-for-world-building/archive/refs/heads/main.zip`
- Tarball — `https://api.github.com/repos/ikkihomes420-jpg/skills-for-world-building/tarball/main`

Skills live under `skills/<skill-name>/`. If your tool only scans the **repository root** for `*/SKILL.md`, point it at the `skills/` subdirectory (or use the plugin in section 1, which handles this).

### Typical flow

Pace the project with `gradual-worldbuilding`, research real-world material with `worldbuilding-research`, store approved canon in `living-canon-os`, evolve systems and simulate with `storycraft-os`, and design languages with `conlang-design`.

## If an agent says the repo is private

It isn't — the repository is public and every file is readable anonymously (verified via the GitHub API, `raw.githubusercontent.com`, `git ls-remote`, and the zip/tarball endpoints).

GitHub returns **404 Not Found** rather than 403 when a credential is not permitted to see a repository, and clients commonly report that 404 as "maybe private". So that message usually means one of these:

| Cause | Fix |
| --- | --- |
| A **fine-grained PAT** scoped to *Only select repositories* that doesn't include this repo | Add `skills-for-world-building` to the token's repository access — or remove the token, since the repo is public |
| A **GitHub App** that is not installed on this repo | Install the app on `skills-for-world-building`, or have its owner add the repo to the installation |
| **Wrong URL** — a typo, a different account, or a path that doesn't exist | Use the exact URLs in [Install](#install); a bad path also returns 404 |
| A **`raw.githubusercontent.com` file URL** pasted into a field that expects a **repository** | Give it `https://github.com/ikkihomes420-jpg/skills-for-world-building` — cloning a raw file URL fails with `404: Not Found` even with no credentials at all |
| **Expired, revoked, or mistyped token** | Regenerate it, or drop the token entirely for a public repo |
| The agent scrapes `github.com` HTML and gets blocked or rate-limited | Use a `raw.githubusercontent.com` URL (section 4) or the zip/tarball (section 5) |

Check anonymously — if this prints `"private": false`, the repo is readable without any credential:

```bash
curl -s https://api.github.com/repos/ikkihomes420-jpg/skills-for-world-building | grep '"private"'
```

### The exact error: `Could not access repository`

This is what a **repository-scoped** tool reports — one that clones or lists refs,
and offers "repository token" or "SSH authentication" settings — when the thing it
was handed is not a repository, or when the credential it sent is not valid.
Two causes account for nearly every case:

1. **A `raw.githubusercontent.com` file URL was given where a repository URL
   belongs.** Git operations against a raw file URL return `404: Not Found`,
   which the tool then reports as a possibly-private repository.
2. **A stale or invalid token is saved in the tool's settings.**
   `raw.githubusercontent.com` honours the `Authorization` header, so an invalid
   token turns a public, working URL into a 404.

Both are reproducible from a shell with no special access. The same public URL
returns `200` anonymously and `404` when a bad token is attached:

```bash
# 200 — public, needs no credentials at all
curl -s -o /dev/null -w '%{http_code}\n' \
  https://raw.githubusercontent.com/ikkihomes420-jpg/skills-for-world-building/main/skills/living-canon-os/SKILL.md

# 404 — same URL, with an invalid token in the header
curl -s -o /dev/null -w '%{http_code}\n' \
  -H 'Authorization: Bearer <any-invalid-token>' \
  https://raw.githubusercontent.com/ikkihomes420-jpg/skills-for-world-building/main/skills/living-canon-os/SKILL.md
```

**Fix:** give repository-scoped tools the repo URL
(`https://github.com/ikkihomes420-jpg/skills-for-world-building`) and leave the
token field **empty** — the repository is public. If a token is already saved,
clear it rather than replacing it, so a stale value can't break an otherwise
working URL.

## License

`conlang-design`, `living-canon-os`, and `storycraft-os` do not declare a license.
`gradual-worldbuilding` and `worldbuilding-research` adapt governance concepts from the
MIT-licensed [Orchestra Research AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs)
and are offered under MIT.
