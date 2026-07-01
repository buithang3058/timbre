---
name: brand-seo
description: >
  Audits brand authority signals for Timbre projects — entity establishment,
  E-E-A-T, branded search volume, and unlinked mentions. Outputs a scored
  audit report with specific action commands. Invoke as /brand-seo [project]
  where project is tokemist | simplize | motquacam.
metadata:
  version: 1.0.0
---

# Brand SEO Audit

Measures whether Google recognizes the project as a trusted entity. Covers
entity establishment, E-E-A-T signals, branded search tracking, and unlinked
mentions. Every finding maps to a specific action command.

**Related skills:**
- `/schema [project]` — add structured data after entity audit
- `/seo-audit [project]` — technical + on-page audit
- `/seo-strategy [project]` — quarterly traffic strategy
- `/content-seo [project]` — write/update author page or articles

---

## Project Registry

| Project | Domain | Author | Niche | YMYL? |
|---------|--------|--------|-------|-------|
| tokemist | tokemist.com | Bui Thang | Crypto analytics & investment | Yes |
| simplize | simplize.vn | Bui Thang | Personal finance & Vietnamese stocks | Yes |
| motquacam | TBD | Bui Thang | TBD | TBD |

---

## Step 0 — Project Detection

If the user invoked `/brand-seo [project]`, use that project.
If no project argument, ask:
> "Which project? tokemist / simplize / motquacam"

Load domain, author name, and niche from the registry above.

---

## Step 1 — Entity Audit

Check whether the project exists as a recognized entity across the web.

### 1A — Author Page

Fetch the domain's `/about` or `/tac-gia` or `/author` page:

```
WebFetch: https://[domain]/about/
WebFetch: https://[domain]/tac-gia/
```

Check for:
- [ ] Author page exists and is indexable
- [ ] Full name visible (Bui Thang)
- [ ] Bio mentions first-hand experience (not just credentials)
- [ ] Photo present
- [ ] Links to social profiles (Facebook, LinkedIn, Threads)
- [ ] `Person` schema present — check page source for `"@type":"Person"`

Flag each missing item as `✗ MISSING` or `⚠ WEAK`.

### 1B — Homepage Entity Signals

Fetch homepage:

```
WebFetch: https://[domain]/
```

Check for:
- [ ] `Organization` or `WebSite` schema present
- [ ] About link in navigation or footer
- [ ] Author/team mention on homepage
- [ ] Social profile links in footer

### 1C — Social Profile Consistency

Check that author name and bio are consistent across platforms.
Search each:

```
WebSearch: "Bui Thang" site:linkedin.com
WebSearch: "Bui Thang" [project] site:facebook.com
WebSearch: buithang3058 site:threads.net
```

Check for:
- [ ] LinkedIn profile exists and mentions [project]
- [ ] Facebook profile/page links to [domain]
- [ ] Threads profile links to [domain]
- [ ] Bio description consistent across all platforms

---

## Step 2 — E-E-A-T Signals

E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) is Google's
quality framework for YMYL content. Every item here directly affects rankings.

### 2A — Article-Level Signals

Fetch 3 recent articles from the domain. Check each for:

- [ ] Visible author byline with link to author page
- [ ] Published date visible
- [ ] Last updated date visible (critical for crypto/finance — outdated = untrustworthy)
- [ ] Author bio block at bottom of article
- [ ] `Article` schema with `author` field pointing to author page URL

### 2B — External Citations

Search for external sites citing Bui Thang or the project:

```
WebSearch: "tokemist" -site:tokemist.com
WebSearch: "Bui Thang" crypto Vietnam
WebSearch: site:tokemist.com (via Semrush backlink_research)
```

Use Semrush `backlink_research` for domain:

```
Tool: backlink_research
Input: domain = [domain], limit = 20
```

Check for:
- Number of referring domains
- Quality of citing sites (are they relevant? authoritative?)
- Any press mentions, forum citations, or aggregator listings

### 2C — Content Freshness

Fetch sitemap or blog index to check article update patterns:

```
WebFetch: https://[domain]/sitemap.xml
WebFetch: https://[domain]/vn/ (or /blog/)
```

Flag articles that:
- Are >6 months old with no update date shown
- Cover topics with frequent changes (Bitcoin price, regulations, DeFi)
- Have `dateModified` missing from Article schema

---

## Step 3 — Branded Search Tracking

Pull branded keyword volume from Semrush to measure real-world recognition.

```
Tool: keyword_research
Input: keyword = "[project name]", database = "vn"

Tool: keyword_research  
Input: keyword = "[domain without TLD]", database = "vn"

Tool: overview_research
Input: domain = [domain], database = "vn"
```

Extract:
- Monthly search volume for brand name
- Search volume trend (growing / flat / declining)
- Domain authority score
- Estimated monthly organic traffic
- Number of ranking keywords

Interpret:
- Brand volume < 100/month → entity not yet established
- Brand volume 100-500/month → early recognition
- Brand volume > 500/month → established entity

---

## Step 4 — Unlinked Mention Finder

Search for sites mentioning the project without linking back.
Each unlinked mention is a link-building opportunity.

```
WebSearch: "tokemist" -site:tokemist.com -site:facebook.com -site:threads.net
WebSearch: "tokemist.com" -site:tokemist.com
WebSearch: "[author name]" "[niche keyword]" Vietnam
```

For each mention found:
- Record: source URL, mention context, link present (yes/no)
- If no link → flag as `OUTREACH OPPORTUNITY`

---

## Step 5 — Competitor Comparison

Pick 1-2 competitor domains in the same niche. Pull their brand signals
to benchmark where the project stands.

```
Tool: overview_research
Input: domain = [competitor domain], database = "vn"

Tool: backlink_research
Input: domain = [competitor domain], limit = 10
```

Vietnamese crypto competitors to check for tokemist:
- tienao.com
- coinviet.net
- blogtienao.com

Vietnamese finance competitors for simplize:
- cafef.vn
- vneconomy.vn (large, use for reference only)

Compare: domain authority, referring domains, branded search volume.
Output delta: "tokemist has X% of competitor's referring domains."

---

## Step 6 — Audit Report

Output the full report in this format:

```
BRAND-SEO AUDIT — [PROJECT]
Generated: [date] | Domain: [domain] | Niche: [niche]
══════════════════════════════════════════════════════

ENTITY STATUS
  Author page:             ✓/✗/⚠
  Person schema:           ✓/✗/⚠
  Organization schema:     ✓/✗/⚠
  Social profiles linked:  ✓/✗/⚠ ([which ones])
  Bio consistency:         ✓/✗/⚠

E-E-A-T SIGNALS
  Article bylines:         ✓/✗/⚠ ([X/Y articles checked])
  Author bio on articles:  ✓/✗/⚠
  Published dates:         ✓/✗/⚠
  Update dates:            ✓/✗/⚠ ([X articles missing])
  External citations:      [N referring domains]
  Press/notable mentions:  [list or "none found"]

BRANDED SIGNALS
  "[project]" search vol:  [N]/month ([trend])
  Domain authority:        [score]
  Organic traffic est.:    [N]/month
  Ranking keywords:        [N]
  vs [competitor]:         DA [X] vs [Y] | [X]% of their referring domains

UNLINKED MENTIONS
  Found: [N] mentions without backlinks
  [list each: source + context]

──────────────────────────────────────────────────────
PRIORITY SCORE: [X]/10
[1-4: weak entity — fix before anything else]
[5-7: developing — strengthen E-E-A-T signals]
[8-10: established — focus on amplification]
──────────────────────────────────────────────────────

ACTION COMMANDS (priority order)
  1. [CRITICAL] Build author page
     → /content-seo [project] (use author page template)

  2. [CRITICAL] Add Person + Article schema  
     → /schema [project]

  3. [HIGH] Add update dates to [N] articles
     → manual — edit each article frontmatter

  4. [HIGH] Outreach to [N] unlinked mentions
     → manual — contact site owners

  5. [MEDIUM] Standardize bio across social profiles
     → manual — update LinkedIn, Facebook, Threads

  6. [MEDIUM] Add author bio block to articles missing it
     → /content-seo [project] (add author bio template)
```

---

## Step 7 — Re-run Recommendation

After actions are completed, suggest when to re-run:

- Author page + schema fixes → re-run in 2 weeks (Google re-crawl time)
- Outreach sent → re-run in 4 weeks
- Quarterly brand health check → re-run every 90 days

Output:
> "Run `/brand-seo [project]` again in [timeframe] to measure improvement.
>  Track branded search volume growth as the primary KPI."
