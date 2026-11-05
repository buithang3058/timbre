# Content SEO — Heading Hierarchy Examples

Two worked examples for the O01 decision in `instructions-detail.md`: when to nest sections under a parent H2 with H3 children, and when to keep peer sections flat. These illustrate content *relationships*, not a template to copy. There is no required number of H2/H3 and no fixed depth — decide from whether a part carries its own content a reader needs to find on its own.

## Example 1 — Nesting is warranted (before → after)

Content context: an article on how ETH supply changes has three parts — issuance (phát hành ETH), burning (đốt ETH), and net supply (cung ròng) — plus a separate part on Layer 2.

Before (every idea as an equal H2):

- H2: Phát hành ETH
- H2: Đốt ETH
- H2: Cung ròng
- H2: Layer 2

After (related parts grouped):

- H2: Cơ chế nguồn cung ETH
  - H3: Phát hành ETH
  - H3: Đốt ETH
  - H3: Cung ròng
- H2: Layer 2

Why: issuance, burning and net supply are three parts of one subject — how supply changes — and each is a distinct point a reader may look up on its own, so they sit under one H2 as H3 children. Layer 2 stays an H2 because it opens a different analytical branch, not a sub-part of the supply mechanism. Caveat: If net supply is only a short synthesis, it may remain an unheaded closing paragraph. Issuance and burning may retain H3s when readers benefit from finding them separately. If the three ideas form one continuous explanation that needs no separate navigation, keep the H2 without H3s.

## Example 2 — Keep it flat (tree preserved)

Content context: an explainer on dollar-cost averaging (DCA) with three sections.

- H2: How DCA works
- H2: When DCA fits (and when it doesn't)
- H2: Common mistakes

Why: these three are genuine peers, each read as one continuous passage. Nesting them under a parent like "About DCA" would not create a useful grouping, because that label just restates the whole article's topic instead of marking a distinct subset of it. Splitting "When DCA fits (and when it doesn't)" into two H3s would cut a single continuous comparison into fragments the reader did not ask to navigate separately. Keep the sections flat.
