# The Entity Stack

The layered system of signals that gets search engines and LLMs to (a) recognize that an entity exists, (b) resolve every mention of it to one identity, and (c) attach facts and trust to that identity. Knowledge panels, E-E-A-T attribution, and AI citations are all built on top of it.

---

## Disambiguation: Entity Stack vs. "Entity Stacking"

Two different things share this name. Get this right before recommending anything.

**"Google entity stacks" (the sold product):** mass-created, interlinked assets on Google properties (Sites, Docs, Sheets, Drive, Maps) plus Web 2.0 profiles, all naming the brand with keyword anchors, funneling to a money site. Sold on Fiverr/Legiit as "entity stacking."

**Verdict: do not buy or build these.** Not primarily because of penalty risk — creating the assets violates nothing, and Google mostly discounts rather than punishes them. They fail the *mechanism*: 50 same-owner, same-week properties are not independent corroboration, and the links pass essentially nothing. The real costs are (1) wasted budget and (2) contamination — a trust-dependent entity (especially YMYL) surrounded by templated spam-pattern assets never accrues the confidence the stack was supposed to build. The kernel of truth in the pitch: a few *real* Google properties (Business Profile, an active YouTube channel) are legitimate corroboration sources. Keep those; skip the stack.

**The entity stack (this document):** the white-hat layered method below.

---

## The Mechanism: Reconciliation Through Corroboration

Google's Knowledge Graph and LLM training pipelines do not trust any single source's claim about who you are. They extract entity mentions from many sources and check whether **independent** sources agree on the same facts — same name, same person↔org relationship, same expertise area, same profile URLs. Entity confidence rises with the number of consistent, independent corroborations.

Two consequences drive everything below:

1. **Schema is a claim, not proof.** JSON-LD is the machine-readable version of your claim; other sources must confirm it. Markup without corroboration triggers nothing.
2. **Consistency beats volume.** Three sources agreeing exactly outweigh thirty sources agreeing approximately. One profile with a different bio actively lowers confidence.

Why this is mandatory for YMYL niches (finance, crypto, health): Google's systems specifically try to establish *who is behind* YMYL content, and unattributable content in these niches is what core updates suppress. The same consistent entity facts are what LLMs need to cite a source by name.

---

## The Four Layers

### Layer 1 — Entity Homes (on-site foundation)

One canonical URL per entity that everything resolves to:

- **Organization** → about page
- **Person/author** → author page with real, verifiable credentials (career history, since-when, what they actually do)
- **Topic entities** → pillar pages (one per core topic)

Every article byline links to the author home. Internal links for topic terms point at their pillar. Naming is identical everywhere — one spelling, one form.

### Layer 2 — Schema Serialization

Serialize Layer 1 decisions as a connected `@graph`: `Person` ↔ `Organization` ↔ `WebSite`, author `@id` on every `Article`, `sameAs` arrays from Layer 3. Implementation belongs to **seo-schema**; the decisions (the registry below) belong here. Schema must never invent entity facts — it only serializes the registry.

### Layer 3 — Off-Site Corroboration

The independent sources that confirm the claim:

- **Profiles you actually maintain** (X, LinkedIn, Facebook, YouTube, GitHub) with *identical* name, one-line bio facts, and links back to the entity homes. `sameAs` lists only these. Dead profiles created "for SEO" are negative corroboration — don't create new ones.
- **Employer/affiliation pages** — if the author has a profile on an established company's site, get it linked to the personal entity. One genuinely independent, high-authority confirmation outweighs dozens of self-made profiles. This is usually the cheapest high-value corroboration available.
- **Real media/podcast mentions** — the 6–12 month layer. One appearance on a known niche outlet beats a campaign of minor ones.
- **Google Business Profile / YouTube** — legitimate if real and maintained.

**Skip until notability is defensible:** Wikipedia/Wikidata. Premature attempts get reverted and salt the ground.

### Layer 4 — Topical Reinforcement

An entity with no authority attached is inert. Pillar coverage of the core topics, internal linking that resolves topic mentions to pillar pages, and growing brand-name search demand attach the expertise to the identity. This layer is the bridge to the topical map work elsewhere in this skill.

---

## The `@id` Registry

The #1 failure mode in entity SEO is drift: three slightly different Organization entities across templates, author names spelled two ways, `sameAs` lists that differ per page. The vaccine is a registry — entity URIs decided **once**, then serialized identically everywhere, forever.

**Location:** `voices/[project]/entity-registry.md` (alongside `brand-identity.md`; it is a durable brand artifact, not a draft).

**Template:**

```markdown
# Entity Registry: [project]
*Decided: [date]. Change only deliberately — every change must be rolled out site-wide.*

## Core Entities

| Entity | Type | @id (canonical URI) | Entity home URL |
|---|---|---|---|
| [Org name] | Organization | https://site.com/#organization | https://site.com/ve-chung-toi/ |
| [Author name] | Person | https://site.com/#person-[slug] | https://site.com/tac-gia/[slug]/ |
| [Site name] | WebSite | https://site.com/#website | https://site.com/ |

## Canonical Facts (must match everywhere, including off-site bios)
- Name (exact form): ...
- One-line bio: ...
- Role / affiliation: ...
- Since: ...

## sameAs (only profiles that are real, maintained, and consistent)
- https://x.com/...
- https://linkedin.com/in/...

## Topic Entities
| Topic | Pillar URL | Wikipedia/Wikidata ref (for `about`/`mentions`) |
|---|---|---|
| [topic] | /pillar-url/ | https://vi.wikipedia.org/wiki/... |
```

**Hand-off contract:** seo-schema *reads* this registry and serializes it. It never invents `@id`s, never adds `sameAs` entries, never restates facts differently. If the registry is missing, create it here first.

---

## Per-Project State Assessment

The stack is a method, not a fixed checklist. Assess before sequencing:

**New entity (site/author unknown to the graph):** build in layer order 1 → 2 → 3 → 4. Author-first if YMYL — a credible author entity consolidates in months; brand entities take years.

**Established brand (partial Knowledge Graph presence already):** the job is a *consistency audit*, not construction. Find every existing entity assertion (site templates, old schema, profiles, third-party listings), reconcile contradictions into the registry, then re-serialize. Construction work on top of contradictory signals wastes effort.

**Multi-brand author (person writes for several properties):** one Person `@id` per human, referenced by each brand's schema. Never mint a separate person entity per site — that splits the corroboration you're trying to accumulate.

---

## Default Sequencing

**Days 0–30 (foundation, non-negotiable order):**
1. Decide the registry (1 hour, highest leverage per minute of the whole stack)
2. Author page with real credentials + bylines linking to it
3. About page
4. Serialize via seo-schema
5. Align existing profiles to the canonical facts; wire `sameAs` both ways

**Days 30–90 (corroboration):**
6. Employer/affiliation profile linked to personal entity
7. Topic-entity pillar audit; internal links resolve to pillars
8. Real Google properties if genuinely maintained

**Months 3–12 (authority):**
9. Selective real mentions (podcast, niche media)
10. Reassess Wikidata only if notability has become defensible

---

## Measurement

Monthly scoreboard:

- **Brand SERP** — search the org and author names: does Google show a coherent result set? Knowledge panel triggered yet?
- **AI citations** — ask ChatGPT, Perplexity, and Google AI Overviews the questions your pillars answer (in the market's language). Log whether the site is cited by name. This is the entity stack's GEO scoreboard.
- **Consistency drift** — spot-check 3 pages' JSON-LD against the registry; check profile bios still match canonical facts.
- **`site:` + name search** — is the author entity attached to all articles (byline + schema)?

No knowledge panel after 12 months of consistent signals usually means insufficient *independent* corroboration (Layer 3), not insufficient markup — resist the urge to add more schema.
