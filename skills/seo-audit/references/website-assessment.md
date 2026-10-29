# SEO Audit — Website Assessment

Use for a site or published-page audit. This is separate from the article-writing checklist at `../../content-seo/references/instructions-detail.md`; it does not approve a draft or rewrite the author's voice.

## Select the audit scope

Use only dimensions relevant to the request. The main `seo-audit/SKILL.md` owns the technical and on-page checklists; do not duplicate them in a second report.

| Dimension | Evidence to inspect | Guidance owner |
|---|---|---|
| Crawlability and indexing | Response status, robots directives, canonical, sitemap, rendered page, available Search Console data | Main skill: Crawlability and Indexation |
| Technical usability | Field/lab performance evidence, mobile rendering, HTTPS, assets | Main skill: Technical SEO Audit |
| Published-page presentation | Rendered title, description, headings, navigation, links, media and visible structured data | Main skill: On-Page SEO Audit and schema detection limits |
| Site content and trust | Representative pages, author/about pages, sourcing, relevant business disclosures and external reputation evidence | Criteria below |
| International setup | Locale URLs, canonical/hreflang and actual translated content | `international-seo.md`, only for multilingual scope |

## Content and trust criteria

- **Experience:** look for relevant first-hand work, original data, examples or case studies where the topic calls for them. Do not demand anecdotes or screenshots in every article or infer authorship from style alone.
- **Expertise:** assess accuracy, explanations suited to the audience, sourcing, and relevant author background. Missing formal credentials alone is not proof that a general explainer is poor.
- **Authority:** inspect relevant independent recognition, citations and topic coverage. Distinguish site-level reputation from the quality of one article; do not ask the writer to manufacture authority signals.
- **Trust:** assess attribution, source transparency, correction practices and applicable business/contact/policy information. Commerce-specific disclosures apply to commerce, not every publication. Technical HTTPS checks remain in the main skill.
- **Content depth:** assess intent satisfaction, useful follow-up answers, freshness and originality across the sampled pages. Report duplication or coverage gaps with URLs, not an arbitrary word-count target.
- **Engagement:** interpret available time-on-page, bounce, return-visit and session data in context of page purpose and measurement setup. Missing analytics means unavailable; these metrics alone do not establish quality or ranking causation.

## References and evidence limits

Resolve shared references from `${CLAUDE_PLUGIN_ROOT}/`:
- `references/google-seo-reference.md`: consult relevant sections for Search concepts, technical measurements, structured data or diagnostics; do not load the whole file for every audit.
- `references/eeat-framework.md`: legacy background only when deeper context is needed. Its unsupported update claims, weights and score bands are not an authoritative scoring system and must not determine findings.

These shared documents are dated background, not proof of current Google policy. Verify time-sensitive requirements, update claims and eligibility rules against relevant official documentation before relying on them. A claim repeated in both files is not corroboration; preserve uncertainty even when one copy omits the warning.

## Findings

Use the main skill's existing report format. Each actionable finding identifies the affected URL/site scope, observed evidence, reader or technical impact, and a specific recommendation. Separate observed issues from hypotheses and inaccessible checks. Do not assign a Google E-E-A-T score or unsupported percentage weights.

Article claim verification goes to the assigned content reviewer when requested; a site audit does not imply that all claims were checked. Propose content or voice changes without silently editing the author's text. Do not infer author approval, permission to publish, or ranking guarantees from an audit result.
