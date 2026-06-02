---
name: content-recap
description: >
  Recaps an existing article and generates platform-native social posts
  for X (thread), LinkedIn, Facebook, and Threads — all in your voice.
  Invoke as /content-recap [url-or-path].
---

# Content Recap — Social Repurposing Skill

Turns an existing article into ready-to-post content for X, LinkedIn, Facebook, and Threads. Voice-first: every output applies your writing DNA, not generic repurposing templates.

## Invoke

```
/content-recap [url]
/content-recap [file-path]
```

Examples:
```
/content-recap https://tokemist.com/vn/vi-crypto-la-gi/
/content-recap drafts/tokemist/vi-crypto-la-gi/draft.md
```

---

## Step 0 — Detect Project + Load Voice

**Detect project from input:**

| Input contains | Project |
|----------------|---------|
| `tokemist.com` or `drafts/tokemist/` or `tokemist` in path | tokemist |
| `simplize.vn` or `drafts/simplize/` or `simplize` in path | simplize |
| `motquacam` or `drafts/motquacam/` in path | motquacam |
| Cannot determine | Ask: "Which project is this content for? tokemist / simplize / motquacam" |

Once project is known, load silently:
- `voices/bui-thang/dna.md` — author layer (always)
- `voices/bui-thang/calibration.md` — sentence-level correction pairs
- `voices/bui-thang/bad-almost-good.md` — anti-slop patterns
- `voices/[project]/dna.md` — project layer

If `voices/[project]/dna.md` does not exist — hard stop:
```
DNA file not found: voices/[project]/dna.md
Run /voice-dna-writer [project] first, then retry.
```

Do not summarize or confirm loading. Proceed to Step 1.

---

## Step 1 — Read Article

**If URL:** Fetch with WebFetch. Extract: title, body text, H2 headings, any data/statistics mentioned.

**If file path:** Read the file. Extract the same fields.

If fetch fails (404, timeout, blocked): stop and say:
> "Could not read [url]. Check the URL or paste the article text directly."

Do not proceed with partial content.

---

## Step 2 — Extract Center + Key Insights

From the article content, derive:

**Center of gravity** — what the article is REALLY about, at the mechanism level. Not the topic — the thesis. One sentence.

Example:
- Topic: "ví crypto là gì"
- Bad center: "bài này giải thích ví crypto"
- Good center: "quyền kiểm soát tài sản phụ thuộc vào ai giữ private key, không phải tên tài khoản"

**Key insights** — 3–5 bullets. Each must be:
- Specific (contains a number, mechanism, or concrete example from the article)
- Non-obvious (not the definition of the topic)
- Self-contained (makes sense without the full article)

Bad: "Ví crypto có nhiều loại khác nhau"
Good: "Binance giữ private key của bạn — nếu Binance bị hack, bạn mất tiền dù tài khoản vẫn còn"

---

## Step 3 — Confirmation Gate

Present to the user:

```
Center: [one-sentence center of gravity]

Key insights:
1. [insight]
2. [insight]
3. [insight]
(4. [insight] — if applicable)
(5. [insight] — if applicable)

Does this capture what the article is really about?
Reply 'yes' to generate posts, or correct anything.
```

**STOP. Wait for confirmation.**

If the user corrects — update center and/or insights accordingly. Do not regenerate until user confirms.

---

## Step 4 — Generate Platform Posts

Generate all 4 platforms after confirmation. Apply voice DNA throughout.

---

### X Thread

**Rules:**
- 5–8 tweets. Each tweet max 260 characters (leave room for numbering if added).
- Tweet 1 (hook): bold claim, striking number, or the counterintuitive insight. No "THREAD:" opener. No "🧵" unless the article itself used emoji.
- Tweets 2–7: one insight per tweet. Each self-contained — a reader who only sees tweet 3 should understand it without context.
- Last tweet: one concrete implication or next action. No "follow me for more," no slogan closer.
- Apply DNA: short sentences, lead with data/mechanism, no announce-importance, no symmetrical insight.

**Format output as:**
```
[1/N] [tweet text]
[2/N] [tweet text]
...
[N/N] [tweet text]
```

---

### LinkedIn Post

**Rules:**
- 150–300 words.
- Line 1 (hook): must stand alone before "see more" — 1 sentence, creates curiosity or states the sharpest observation from the article. Blank line after.
- Body: 2–4 short paragraphs. Blank line between each. Mechanism → evidence → implication.
- Ending: a real question that invites reflection or comment. Not "check out my article" or "click the link."
- Article URL: include at the end as a plain URL on its own line, no "Link:" label.
- Hashtags: max 3, at the very end. Only include if the project DNA uses them.
- Apply DNA: no meta-narration, no motivational filler, no slogan closer.

---

### Facebook Post

**Rules:**
- 80–150 words.
- Opens with the observation or mechanism — not "Tôi vừa viết bài về..." or "Bài mới rồi nhé."
- Body: 2–3 short paragraphs.
- Ends with a question that invites comments (not a CTA to read the article).
- Article URL: on its own line after the text.
- Apply DNA: conversational but specific, not generic. Lead with what's interesting, not what the article is called.

---

### Threads Post

**Rules:**
- If article is short (< 800 words): single post, max 500 characters.
- If article is medium/long (≥ 800 words): 3–5 posts, each max 480 characters.
- More casual than X. Conversational opener.
- Same anti-patterns apply: no meta-narration, no slogan closer.
- Multi-post: each post self-contained, last post ends with the implication.

---

## Step 5 — Voice Quality Check

After generating all 4 posts, run a quick check. Flag any of the following — do NOT self-correct, list the flags for the user:

| Anti-pattern | Signal |
|---|---|
| Meta-narration | "Bài này sẽ...", "In this thread I explain...", "Check out my new article" |
| Announce importance | "Đây là điều quan trọng nhất...", "This is crucial..." |
| Slogan closer | Two-part symmetrical closing sentence |
| Motivational filler | "Bạn hoàn toàn có thể...", "Don't miss this", "Start today" |
| Generic opener | Opens with topic definition instead of mechanism or observation |

Append after the 4 posts:

```
--- VOICE CHECK ---
[list any flags, or "No flags — all 4 posts pass voice check."]
```

---

## Output Format

Present in this order, each with a clear platform header:

```
## X Thread
[tweets]

## LinkedIn
[post]

## Facebook
[post]

## Threads
[post]

--- VOICE CHECK ---
[flags or pass]
```

---

## What This Skill Does NOT Do

- Does not create content from scratch — use /content-seo for that
- Does not schedule or post to any platform
- Does not rewrite the article — it recaps and adapts
- Does not skip the confirmation gate — human confirms the center before any post is written
