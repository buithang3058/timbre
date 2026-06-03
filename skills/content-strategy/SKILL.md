---
name: content-strategy
description: When the user wants to plan content for SEO, create a writing queue, build topic clusters, or decide what to write next. Triggers: "content strategy," "content plan," "what should I write next," "topic clusters," "pillar content," "cluster articles," "content hub," "content planning," "writing queue," "lên kế hoạch nội dung," "viết gì tiếp theo," "bài nào nên viết tiếp."
metadata:
  version: 2.0
---

# Content Strategy — Writing Queue Planner

Generates a prioritized writing queue for Timbre projects: scans published content, in-progress drafts, and ideas backlog; maps gaps per hub; outputs 3–5 next articles pre-formatted for `/content-seo` Stage 1.

**Related skills:**
- `/content-seo [project]` — write a specific article (4-stage perception-first workflow)
- `/seo-research` — keyword + competitor research (use before content-seo Stage 2)
- `/voice-dna-writer [project]` — create voice DNA if it doesn't exist yet

---

## Project → Path Mapping

| Project | DNA | Content Root | Drafts |
|---|---|---|---|
| tokemist | `voices/tokemist/dna.md` | `/Users/buithang/tokemist/web/content/` | `drafts/tokemist/` |
| simplize | `voices/simplize/dna.md` | TBD | `drafts/simplize/` |
| motquacam | `voices/motquacam/dna.md` | TBD | `drafts/motquacam/` |

---

## Step 0 — Project Selection

If the user invoked `/content-strategy [project]`, use that project. If no project argument, ask:

> "Which project? tokemist / simplize / motquacam"

Look up paths from the mapping table. Check if DNA file exists.

**If DNA file is missing — hard stop:**

```
DNA file not found: voices/[project]/dna.md
Run /voice-dna-writer [project] first, then retry /content-strategy [project].
```

Read DNA silently. Extract the Content Hubs section — hold the hub list with audience profiles in context. Proceed to Step 1.

---

## Step 1 — Content Audit

Scan all 3 sources silently. Combine results before outputting.

**Source 1 — Published:** `ls [Content Root]/[hub-folder]/` for each hub from the DNA. Each subdirectory = one published article. For tokemist, hub folders are the slug keys: `kien-thuc-co-ban`, `tu-dien-crypto`, `huong-dan-onchain`, `giao-dich-phan-tich`, `glossary`, etc.

**Source 2 — In-progress drafts:** `ls drafts/[project]/` — each subdirectory containing `draft.md` or `index.mdx` is a draft in progress. Cross-reference with Source 1: if a draft slug already appears in Published, mark it as stale and exclude from in-progress count.

**Source 3 — Ideas backlog:** Read `drafts/[project]/ideas.md` if it exists. Extract each article title and its target hub.

**Output — Content Inventory table:**

```
## Content Inventory — [project] ([date])

| Hub | Published ✓ | In-Progress ⏳ | Ideas 💡 | Total |
|---|---|---|---|---|
| [Hub 1] | N | N | N | N |
| [Hub 2] | 0 | 0 | 0 | 0 |

### Detail

**[Hub 1]** published ✓:
- [slug] → [URL]

**[Hub 1]** in-progress ⏳:
- [slug] → drafts/[project]/[slug]/

**[Hub 1]** ideas 💡:
- [Title] → from ideas.md
```

---

## Step 2 — Hub Gap Analysis

For each hub, apply priority scoring:

| Priority | Condition | Action |
|---|---|---|
| **P1 — Publish-ready** | Draft exists with content | Publish first — no Perception Dump needed |
| **P2 — Cluster gap** | Hub has pillar, fewer than 3 clusters live | High priority — build cluster coverage |
| **P3 — Hub launch** | Hub has 0 content | Needs a pillar page first |
| **P4 — Cluster expansion** | Hub has pillar + 3+ clusters, below 6 | Medium priority |

For P1: note any pre-publish tasks flagged in `drafts/[project]/[slug]/sources.md` (e.g., word substitutions, fact checks).

For P2/P3: identify missing cluster topics using hub audience profile from DNA + existing pillar content.

---

## Step 3 — Writing Queue Output

Output the writing queue, sorted P1 → P2 → P3 → P4.

```
## Writing Queue — [project]

[N] articles ready or next to write:

1. [Article Title]
   Hub: [hub name] | Tier: [Pillar | Cluster] | Priority: P[1–4]
   Pillar URL: [/vn/[pillar-slug]/ or "TBD — pillar not published yet"]
   Status: [Publish-ready (draft at drafts/[project]/[slug]/) | New | From ideas.md]
   Why now: [1 sentence — the specific gap this fills]

   → /content-seo handoff:
   TOPIC: [suggested topic angle]
   HUB: [hub name from DNA]
   CONTENT TIER: [Pillar | Cluster]
   PILLAR URL: [URL]

2. [Article Title]
   ...
```

After presenting the queue, ask once:

> "Bắt đầu `/content-seo [project]` cho bài số 1 ngay bây giờ không?"

If yes: output the Stage 1 Perception Dump template pre-filled with TOPIC, HUB, CONTENT TIER, PILLAR URL and stop for the user to fill in their answers.

---

## Reference: Topic Cluster Framework

### Structure

```
Pillar page (broad topic, 3,000–5,000+ words)
    ↕ internal links
Cluster 1 (subtopic, 1,200–2,500 words)
Cluster 2 (subtopic)
...
Cluster 6–12 (subtopics)
    ↔ cluster to cluster links
```

### Pillar Page

| Attribute | Guideline |
|---|---|
| **Length** | 3,000–5,000+ words; comprehensive guide |
| **Keyword** | Broad head term with search volume |
| **Role** | Hub; links to all cluster articles |

### Cluster Articles

| Attribute | Guideline |
|---|---|
| **Count** | 6–12 per pillar (minimum 6 for authority) |
| **Length** | 1,200–2,500 words; focused on one subtopic |
| **Links** | Cluster → pillar; pillar → cluster; cluster ↔ cluster |

### Why Topic Clusters Work

- **Topical authority**: Rank for multiple query variations; comprehensive coverage signals expertise to search engines and AI systems
- **Avoid cannibalization**: One page per topic/intent — no competing pages
- **AI citations**: Clustered content gets ~42% more AI citations than standalone pages
- **Traffic durability**: ~30% more organic traffic; rankings hold ~2.5× longer

### Evergreen vs Timely Mix

- **Evergreen (70–75%)**: Pillar guides, how-tos, comparisons, glossaries. Refresh every 6–12 months.
- **Timely (25–30%)**: Trending, news. Generates quick traffic, short shelf life. Link timely pieces into evergreen pillars after traffic spike.
