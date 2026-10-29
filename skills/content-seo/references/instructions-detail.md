# Content SEO — Article Quality and Self-Check

Used by `content-seo` 4.1 to prepare reader-facing elements and 4.4 to check the finished article. Keep the CORE-EEAT IDs for existing review records; these are local editorial criteria, not a Google score. Read alongside the approved center, target reader, research coverage, project policy and routed voice files.

Assess the text and its reader-facing structure. Crawlability, HTTPS, performance, schema implementation, business reputation and site-wide authority belong to `seo-audit`, not this check. Do not require credentials, testimonials or personal anecdotes merely to make an article pass. Never invent experience. Author-approved voice and the existing voice precedence remain in force.

## CORE-EEAT Constraints

Check these criteria against the actual draft. Do not interrupt writing to grade each sentence:

| ID | Standard | How to Apply |
|----|----------|--------------|
| C01 | Intent Alignment | Title promise matches delivery |
| C02 | Direct Answer | Core answer appears in the first 150 words (a Mode A utility block may supply it); the prose develops the explanation in the order the reader needs, without withholding an answer to create suspense |
| C06 | Audience Targeting | The opening addresses the TARGET READER’s question and knowledge level; it need not stage a reader scenario (see hook guidance in 4.1) |
| C10 | Semantic Closure | Conclusion resolves the opening question with a decision, implication, or next step — no recap |
| O01 | Heading Hierarchy | Clear H1 → H2 → H3 structure that remains usable for scanning after narrative restructuring |
| O02 | Summary Box | Key Takeaways block near the top |
| O06 | Section Chunking | Each section adds a useful answer or explanation; required concepts and reasoning are established before use (the reader has enough information to follow the next idea). Paragraph length follows voice, not a sentence quota |
| O09 | Information Density | Remove repetition and filler while preserving essential answers and conditions; brevity alone is not quality |
| R01 | Data Precision | Numbers are specific and carry units — and only appear when they can be sourced or labeled (see R02). No quota of numbers |
| R02 | Citation Coverage | Every number with a unit carries an inline source link OR a provenance annotation as an MDX comment right after the sentence: `{/* hằng số giao thức */}` or `{/* tự tính: <công thức> */}`. Annotations are for lint and the reviewer; they never appear as reader-visible text (no `[hằng số giao thức]` in prose — the author rejected it as unnatural). In prose, a derived figure reads "theo ước tính"; the spec is linked once per article. Minimum 1 external citation per article. Count comes from claims, not word count |
| R04 | Evidence-Claim Mapping | Material factual premises have supporting evidence; examples clarify but do not by themselves verify a general claim. Preserve the author’s interpretation while checking its premises under project policy |
| R07 | Entity Precision | Use full names for people and organizations |
| C03 | Query Coverage | Check essential questions against actual answer locations using the prepared coverage map; for rewrites account for useful answers lost from the original. Headings or keyword mentions alone do not satisfy coverage |
| O08 | Anchor Navigation | Add a TOC when the draft has 3+ H2 sections; entries must target headings, not merely list their names |
| O10 | Multimedia Structure | Captions and meaningful media when media is used. No image quota; mark not applicable if absent. New image prompts wait for final approval under content-seo 4.8 |

## Reader-facing elements

- **Length:** use Pillar 3,000–5,000 words, Cluster 1,000–2,000 and glossary under 300 only as initial planning references, not minimums, maximums or pass/fail criteria. Essential answers, necessary conditions and the target reader determine the finished length; never pad or cut them to hit a range. Report the word count and explain substantial deviations through coverage in the existing self-check. Follow an explicit author length constraint; if it conflicts with essential coverage, present the scope tradeoff instead of silently omitting answers.
- **Informational “X là gì”:** check whether the target reader needs definition, mechanism, characteristics, benefits, tradeoffs, comparison and applications. Include what is needed, not a quota of sections.
- **Takeaways:** immediately after the hook, 3–5 concrete insights serving the center, not teasers or a contents list.
- **FAQ:** 5–7 questions, 60–100 words each; remove or reframe questions already answered verbatim or unrelated to the center rather than filling a quota. Serve the reader who finished the article with decisions, edge cases or scenarios. First sentence answers; include consequential conditions without generic disclaimers.
- **Links:** Cluster links to its pillar and 1–2 related clusters; Pillar links to 3–5 existing or planned clusters (placeholders allowed). Citation count follows claims, with at least one external citation.
- **Metadata and keywords:** inspect the actual title/description in frontmatter. Description planning range: 120–160 characters. Check topic wording in H1, first 150 words, an H2 and conclusion; flag gaps, without mechanically inserting repeated terms. Title promise must match the article; consult title formulas when choosing it. Alternatives are not reviewed until promoted into frontmatter.

## Voice and reasoning

Compare passages with the selected author samples and applicable calibration. Check whether supplied personal observations became generic claims, explanations repeat what a detail already shows, or transition phrases conceal a missing reasoning step. Preserve the author's perspective and natural phrasing; fix the specific mismatch instead of adding "I" or shortening every sentence. Utility blocks remain direct and scannable. Apply existing voice precedence; this check creates no competing style rules.

## Self-Check

After drafting, check the actual article against the 15 items with Pass / Warn / Fail (or not applicable for conditional media). Record findings with locations in the existing `review.md` writer section using the content-seo template. Record the reader-facing and voice checks there too; do not create a second checklist file or aggregate score. Do not claim "all pass" without checking the text.

This is writer self-check, not independent claim verification. Report evidence gaps for `content-review`; a writer Pass neither closes reviewer findings nor approves publication. The author decides voice, thesis and final approval.

## Handling issues

Follow content-seo 4.6–4.7 for edits and approval; this reference adds no separate permission gate.
- Correct mechanical structure or formatting within the authorized scope: duplicate headings, missing TOC links, accidental repetition, or missing alt for existing media. Preserve meaning and author edits.
- Treat title/description changes that alter a claim as claim changes, not automatic length fixes. The actual title/description must remain in the reviewed article.
- Apply local claim fixes from reviewer findings under 4.6; changes to thesis, framing or center wait for the author. Do not add hedges or remove a position merely to satisfy this checklist.
- Use existing DNA/calibration for scoped voice work. During re-checks, do not reopen unrelated style or completed findings.
