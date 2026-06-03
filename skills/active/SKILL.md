---
name: active
description: Switch the active project context. Use when changing focus between projects. Triggers: "active [project]", "/active tokemist", "/active simplize", "chuyển sang [project]", "switch to [project]".
metadata:
  version: 1.0
---

# /active — Switch Active Project

Switches the active project context by updating the memory file. All future requests default to the new project.

## Known projects

| Project | Status |
|---|---|
| tokemist | Active |
| simplize | Active — DNA created 2026-05-29 |
| motquacam | DNA not created yet |

## Steps

**1. Read argument.** If the user typed `/active [project]`, use that project name. If no argument, ask: "Which project? tokemist / simplize / motquacam"

**2. Validate.** Check the project is in the known projects table. If unknown, list the valid options and stop.

**3. Update memory.** Overwrite `~/.claude/projects/-Users-buithang-timbre/memory/project_active_focus.md` with:

```
---
name: active project focus
description: Which project is currently being worked on — check this before assuming project context
type: project
---

Current active project: **[project]**

**Why:** User switched to [project] on [today's date].

**How to apply:** When in doubt about which project a request refers to, default to [project]. Do not mention other projects unless the user explicitly brings them up. When doing file scans or QA, scope to [project] paths only.

Last updated: [today's date]
```

**4. Update MEMORY.md index.** Edit the first line of `~/.claude/projects/-Users-buithang-timbre/memory/MEMORY.md` to reflect the new active project:

```
- [Active project focus](project_active_focus.md) — current focus: **[project]**; default mọi request về [project], không đề cập project khác trừ khi user hỏi
```

**5. Confirm.** Output:

```
Active project: [project]

Từ giờ mọi request mặc định về [project]. Để chuyển lại, gõ /active [other-project].
```
