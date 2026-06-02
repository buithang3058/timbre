# Timbre

**Grow without losing your voice.**

Timbre is an AI-assisted system for building a website or personal brand from scratch — strategy, content, distribution, and iteration — where your authentic writing voice is the engine, not an afterthought.

Most AI writing tools treat voice as a style preference. Timbre treats it as a competitive asset: something to encode, preserve, and compound over time.

---

## The Problem

AI content is converging. Every tool produces the same smooth, hollow output — correct on the surface, identical underneath. The writers and brands that will win are the ones who sound unmistakably like themselves.

The challenge: using AI at scale without losing what makes your voice distinct.

---

## How Timbre Works

**Voice-first architecture.** Before AI writes a single word, you capture your raw insight — what you actually know, what surprises you, what you still find unresolved. This is the Perception Dump. AI works from your thinking, not in place of it.

**Two-layer voice system.** An author layer (how you write) and a project layer (what you write about, who reads it). Both are always active. The author layer applies across every project you run.

**Anti-slop detection.** Timbre ships with a named taxonomy of AI failure modes — the patterns that sound almost-good but are actually generic. Symmetrical wisdom, fake depth through contrast, theatrical bucket brigade, over-clean conclusions. Each draft is checked against these before it ships.

**Compounding calibration.** Every time AI output sounds wrong, you log the correction: AI-ish sentence → preferred rewrite → why → reusable pattern. Over time, this builds a pattern library specific to your voice. The system gets more accurate with every article you write.

---

## Current Skills

Timbre runs as a set of Claude Code slash commands:

| Skill | What it does |
|-------|-------------|
| `/content-seo` | 4-stage writing workflow: Perception Dump → Research → Center of Gravity → Draft |
| `/seo-research` | SEMrush keyword volume + intent, semantic entity map, claim verification |
| `/voice-dna-writer` | Extracts your writing voice into a compact DNA file (≤500 words) |
| `/voice-interviewer` | Structured interview to surface raw voice source material |
| `/voice-calibration` | Log AI-ish → preferred correction pairs; build your pattern library |
| `/content-strategy` | Prioritized writing queue based on hub gaps and keyword opportunity |
| `/content-hemingway` | Cut and tighten pass after draft is complete |

---

## The 4-Stage Writing Workflow

**Stage 1 — Perception Dump** *(human only, no AI)*
You fill out 5 fields offline: what people get wrong, what predicts failure, what secretly matters, what changed your mind, what still bothers you. AI touches nothing until this is done.

**Stage 2 — Research**
SEMrush keyword data + semantic entity mapping + primary source verification for claims in your dump. Grounded in real data, not AI inference.

**Stage 3 — Center of Gravity**
Four article angle options generated from your dump. You pick the center: "This article is really about ___." The center is a lens, not a topic. It constrains everything in Stage 4.

**Stage 4 — Draft → Cut → Discovery Loop**
AI drafts against your center. Quality check flags voice anti-patterns, E-E-A-T signals, and semantic entity coverage. Cuts are proposed individually — you approve each one. Loop continues until you say done.

---

## Roadmap

- **Social format skills** — tweet/thread, LinkedIn post with format-specific structure rules
- **Reader engagement feedback loop** — GA4 + scroll depth data feeds back into calibration entries, giving voice rules evidence beyond gut feeling
- **Failure taxonomy engine** — aggregates correction pairs across articles into a ranked, categorized pattern library (the compounding asset)
- **Dynamic calibration loading** — at 50+ entries, load only the patterns relevant to the current topic
- **Multi-site support** — run multiple websites or brand voices from one system, each with its own project layer

---

## Requirements

- [Claude Code](https://claude.ai/code) CLI
- Node.js (for SEO research scripts)
- SEMrush API key (optional — required for `/seo-research`)

---

## Philosophy

> The best AI-assisted content is content where you can't tell what the AI contributed — not because the AI was hidden, but because it only amplified what was already yours.

Timbre is built on three convictions:

1. **Human perception before AI writing.** The writer's raw knowledge is the input. AI is the output layer, not the thinking layer.
2. **Voice is a system, not a setting.** It can be encoded, tested, and improved like any other component.
3. **Quality compounds.** Every correction you make today makes tomorrow's draft better.
