---
name: image-prompt
description: >
  Create brand-aligned image prompts from author-approved SEO articles, newsletters,
  or social content. Use after final content approval or when asked for image prompts
  for approved content. Produces a prompt document, not images or published assets.
---

# Image Prompt

Turn approved content into visual briefs and ready-to-use generation prompts. The calling workflow owns content review and author approval; this skill does not approve content, rewrite it, or dispatch another agent.

## Inputs and approval

Accept from the caller or the author:
- The approved content: an absolute file path and approved SHA-256 (12 or 64 characters), or the exact text explicitly approved in the conversation.
- Approval reference: the author's explicit final approval or the calling workflow's approval record. A draft delivery, reviewer pass, file date, or request for prompts alone is not proof of content approval.
- Channel: SEO article, newsletter, or social; for social, the platform and requested format if known.
- Brand reference path, if available, plus any author-provided visual constraints or assets.
- Absolute output path or dossier folder; requested dimensions/format, if any.

Reuse information already provided. Ask only for missing information that changes the work. If approval is missing, wait for it before creating prompts. For file input, read the content and compare its current hash with the approved hash before writing output; on mismatch, report the path and hashes and resolve the approved version. Do not silently accept the latest file. For approved pasted text, use only that exact text as the source; do not copy it into the prompt document.

Read only the approved content, supplied brand reference and relevant visual assets. If no brand reference exists, use a restrained visual direction suited to the content and label it as a proposal, not established brand identity. Do not borrow branding from another project.

## Choose visuals for the channel

- **SEO article:** one cover plus explanatory visuals where they clarify a mechanism, comparison or sequence. No fixed quota for supporting images. Identify the heading or passage each visual serves.
- **Newsletter:** default to one opening visual; add supporting visuals only when they clarify the approved issue. Keep the core idea legible at email-column width.
- **Social:** follow the approved post and requested format. For a single image, focus on one message. For a requested carousel, map each panel to approved material and maintain a consistent visual system; do not turn every post into a carousel. An article's approval does not automatically approve newly written social copy or a newsletter adaptation.

Use supplied dimensions first. Otherwise propose dimensions for the intended placement; label these as production choices, not verified platform limits. Avoid requiring live platform research for a draft prompt. For SEO, retain these defaults where suitable: wide infographic 1200×628, multi-row comparison 800×600, photo illustration 1200×800. For other channels, choose an appropriate aspect ratio and state the intended placement.

## Write the visual briefs

Stay within the approved claims, figures, scope and conditions. Keep illustrative metaphors distinct from literal mechanisms. Do not turn uncertainty into a guarantee or invent data to fill a chart. If the content cannot support a visual accurately, flag that specific gap without rewriting the source.

How-to steps needing proof of an interface or operation require real screenshots. Mark these entries **real screenshot required**, describe the capture and annotations, and omit a synthetic screenshot prompt. Brand logos and actual product interfaces require supplied or verified assets; do not invent them.

For each generated visual, specify the subject, composition, visual relationships, brand treatment, aspect ratio, exact labels and meaningful exclusions. For diagrams, spell out the nodes, arrows, order and conditions rather than merely asking for an attractive infographic. Use charts only with approved values, units and scales.

Prompts are in English. Alt text and any in-image text use the content's language with full diacritics unless the author requests otherwise. Keep in-image copy brief; for dense labels, request a clean illustration and provide exact text separately for layout. Alt text describes the intended visual without keyword stuffing and should be checked against the eventual image.

## Save and return

For content-seo, save to the supplied `$D/image-prompts.md`. For other callers, use their output path or save `image-prompts.md` beside the source when unambiguous. If several channel outputs share a folder, use a channel-specific filename to avoid replacing another deliverable. Read an existing output before updating; preserve unrelated entries and author edits.

Document header: keep it short. Include only:
- Brand reference path, or state that the visual direction is proposed when none exists.
- Visual direction.

Do not write approval references, source paths or hashes, channel metadata, pasted source text, or global export targets into `image-prompts.md`. Use those inputs to validate and shape the work, but keep them out of the deliverable.

Each entry:

`## Image N — [Name]`

Location or carousel panel / purpose / size and aspect ratio / asset format / filename / alt text / exact in-image text (or none).

**Prompt:** followed by a fenced code block containing the English prompt. Screenshot entries use capture instructions instead.

Use descriptive, hyphenated filenames without diacritics, section-first then topic where appropriate. Before saving, compare the briefs against the approved source and brand: no added claim, lost condition, misleading visual relationship or inconsistent label. For file input, recheck the source hash before completion; if it changed during work, report the mismatch and do not present the prompts as matched to that revision.

Return the output link and any unresolved capture/asset needs. Create prompts only; do not generate images, edit the source, mark content approved, commit or publish. When later approved edits affect a visual, update only the affected entries and their source-version reference; content edits still awaiting approval do not trigger prompt regeneration.
