---
name: project
description: Create, select, or inspect a Timbre project and its voice/content configuration. Use /project, /project NAME, or /project create NAME. Also handles the legacy /active alias.
---

# Project

Resolve project identity and resources without hard-coded project names or user paths.
The selected project is pinned in the current conversation. The last explicit selection
is a default for future conversations, not a command to switch existing ones.

## Commands

- `/project`: show the conversation's current project and registered projects. With no projects, start setup.
- `/project NAME`: select a registered project. If unknown, ask whether to create it; do not create from a possible typo.
- `/project create NAME`: collect the missing folder and voice choice, create configuration, register it, and select it. This command authorizes creation; do not ask again.
- An explicit configuration path can register/select an existing project. If the name already maps elsewhere, resolve the conflict before replacing it.
- `/active` forwards its arguments to this skill. There is only one registry.

## Local state

Registry: `~/.config/timbre/projects.json` (expand the current user's home).
Shape: `{"version": 1, "last_project": null, "projects": {"name": "/absolute/path/.timbre/project.yaml"}}`.
This is machine-local state, never part of a shared plugin or a project repository.
A missing registry means no registered projects; invalid JSON is an error, not an empty registry to overwrite.
On registration or explicit selection, re-read the registry, preserve other entries,
merge the change and replace the file atomically. Check it did not change since reading;
on a conflict re-read and merge rather than overwrite another session's registration.

Pin the resolved name and absolute config path in this conversation. After compaction,
restore that binding from conversation context; do not reload `last_project` over it.
There is no promise that another app can access these files: a host without filesystem
access needs the user to supply the configuration and relevant content.

## Resolution for calling skills

1. Use an explicit project/config from the request. Check for conflicts with the article being resumed.
2. For a named existing article, use its established project/dossier association; frontmatter name must resolve to a registered config or a supplied config. Do not guess a version or change its project.
3. Otherwise use the project already pinned in this conversation.
4. On a fresh conversation, inspect `.timbre/project.yaml` in the workspace or nearest ancestor, and the registry's `last_project`. If both exist and refer to different projects, ask which to use before writing. If only one exists, use it.
5. If unresolved, show the registered choices or start setup when none exist.

Only an explicit selection/create updates `last_project`. A passive resume does not.
Announce `Project: NAME` once when binding the conversation; do not repeatedly ask for confirmation.
Selecting a new project here never switches another open conversation. If an article and
selection disagree, ask whether to switch the task or keep its existing association; do not move or relabel the article.

## Project configuration

Store `.timbre/project.yaml` inside the chosen project folder. All relative paths are
resolved against that project folder (the parent of `.timbre`), not the current shell
folder or plugin cache. Absolute external resources are allowed but not portable.
Resolve resources to absolute paths before handing them to scripts or other skills.

```yaml
name: my-publication
voice:
  dna: [voices/author/dna.md]
  calibration: null
  structural_rules: null
  jargon: null
  samples: null
content:
  drafts: drafts
  policy: null
visual:
  brand: null
tools:
  lint: null
```

`voice.dna` is an ordered list, base first and project overlay second when applicable.
No universal requirement for two layers. Optional resources may be absent or null;
if a path is declared but missing, report the configuration error when it is needed.
Do not silently fall back to another project's voice. Missing/empty DNA blocks drafting,
not project creation or selection.

Setup asks only for a project name, folder, and an existing voice or intent to create one.
Validate a nonempty name; reserve `create` for the command. Never derive an arbitrary
filesystem destination from unchecked name text. Do not overwrite existing configs or voice files.
If the author wants a new voice, leave `dna: []`, finish setup, and route to the voice
capture workflow before drafting. Do not fabricate DNA or copy a friend's private voice.
Brand, jargon, policy, and lint can be added later. Do not create article files during setup.

The optional lint field is a script path using the existing Python content-check interface
(`--all FILE`, `--diff BEFORE AFTER`, `--check-hash FILE HASH`, optional `--terms FILE`).
Other lint tools need an explicitly configured adapter; do not execute arbitrary YAML command text.

## Return to the caller

Provide resolved project config, voice resources, `DRAFTS_ROOT`, policy, brand and lint
paths. Calling skills read only what their current step needs. Project selection never
changes author approval, ARTICLE/version selection, or publication permissions.
Installed skill resources resolve from the actual Timbre installation; personal resources
resolve from the selected project config. Never store drafts inside a plugin cache.
Old Claude-specific active-project memory is superseded for Timbre routing, not a second default.
