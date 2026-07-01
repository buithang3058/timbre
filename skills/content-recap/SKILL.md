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

Proceed to Step 1.

---

## Step 1 — Read Article

**If URL:** Fetch with WebFetch. Extract:
- **Hook** — the opening sentence or paragraph of the article, verbatim
- **Key takeaways** — bullet points, conclusion section, or the 3–5 most important statements actually written in the article. Pull verbatim or near-verbatim. Do not derive or invent.
- **Article URL** — the canonical URL for linking

**If file path:** Read the file. Extract the same fields.

If fetch fails (404, timeout, blocked): stop and say:
> "Could not read [url]. Check the URL or paste the article text directly."

Do not proceed with partial content.

---

## Step 2 — Extract Hook + Takeaways

From what was extracted in Step 1:

**Hook** — use the article's actual opening line or the sharpest sentence in the first paragraph. Do not rewrite it. If the opening is weak (meta-narration, definition), take the next strong sentence instead.

**Key takeaways** — 3–5 statements pulled directly from the article. Prioritize: specific numbers, concrete mechanisms, counterintuitive facts. Do not paraphrase beyond trimming for length. Do not invent takeaways not present in the article.

---

## Step 3 — Generate Platform Posts

Use the hook and takeaways from Step 2 as the raw material. Reformat for each platform — do not rewrite the substance.

---

### X Thread

**Rules:**
- Tweet 1: article hook verbatim or trimmed to fit 260 chars. No "THREAD:" opener.
- Tweets 2–N: one takeaway per tweet, pulled from the article. Each max 260 chars.
- Last tweet: article URL on its own line. No slogan closer, no "follow me."
- Only rewrite if the original text exceeds 260 chars — trim, don't rephrase.

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
- Line 1: article hook. Blank line after.
- Body: takeaways as short paragraphs, blank line between each.
- End with article URL on its own line.
- Only trim for length. Do not add new sentences or reframe the content.

---

### Facebook Post

**Rules:**
- Open with the article hook. Body: 2–3 takeaways as short paragraphs.
- Article URL on its own line after the text.
- Only trim for length. Do not add new sentences.

---

### Threads Post

**Rules:**
- If article is short (< 800 words): single post, max 500 chars — hook + 1–2 takeaways + URL.
- If article is medium/long (≥ 800 words): 3–5 posts, each max 480 chars. Post 1 = hook, posts 2–N = one takeaway each, last post ends with URL.
- Only trim for character limits. Do not rewrite.

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
```

---

## Step 6 — Auto-Post

After presenting the output, ask:

> "Posts ready. Where do you want to post?"
> A) Facebook + LinkedIn + Threads
> B) Facebook only
> C) LinkedIn only
> D) Threads only
> E) Copy-paste — I'll post manually

If E: stop here.

For A–D: check credentials and run the relevant posting sequences below. Read credentials from `/Users/buithang/timbre/.env`.

Check which credentials are present:
```bash
source /Users/buithang/timbre/.env
echo "FB_PAGE_ID=${FB_PAGE_ID:+SET}"
echo "FB_PAGE_ACCESS_TOKEN=${FB_PAGE_ACCESS_TOKEN:+SET}"
echo "LINKEDIN_ACCESS_TOKEN=${LINKEDIN_ACCESS_TOKEN:+SET}"
echo "LINKEDIN_AUTHOR_URN=${LINKEDIN_AUTHOR_URN:+SET}"
echo "THREADS_ACCESS_TOKEN=${THREADS_ACCESS_TOKEN:+SET}"
echo "X_API_KEY=${X_API_KEY:+SET}"
echo "X_API_SECRET=${X_API_SECRET:+SET}"
echo "X_ACCESS_TOKEN=${X_ACCESS_TOKEN:+SET}"
echo "X_ACCESS_TOKEN_SECRET=${X_ACCESS_TOKEN_SECRET:+SET}"
```

Before posting to Threads, auto-refresh the token if it's within 7 days of expiry:
```bash
/Users/buithang/timbre/scripts/threads-token.sh refresh
```
If refresh fails with "expired" or "invalid token": print instructions below and skip Threads. Do not stop other platforms.

Post to the platforms selected by the user. Skip silently if credentials are missing for a selected platform — list it as skipped in the summary. X is not supported (requires paid API plan).

If Threads token is expired and refresh failed:
> "Threads token expired. Run: cd /Users/buithang/timbre && ./scripts/threads-token.sh exchange <new_short_lived_token>
> Get a new short-lived token at: Meta app dashboard → Threads API → Getting Started"

---

### Post to Facebook

Split the Facebook post: body text → `FB_TEXT`, article URL → `FB_LINK`.

**Step 1 — Force scrape (ensures image appears in preview):**
```bash
source /Users/buithang/timbre/.env
curl -s -X POST "https://graph.facebook.com/?id=${FB_LINK}&scrape=true&access_token=${FB_PAGE_ACCESS_TOKEN}" > /dev/null
```

**Step 2 — Post:**
```bash
source /Users/buithang/timbre/.env
FB_RESPONSE=$(curl -s -X POST "https://graph.facebook.com/v19.0/${FB_PAGE_ID}/feed" \
  --data-urlencode "message=${FB_TEXT}" \
  --data-urlencode "link=${FB_LINK}" \
  -d "access_token=${FB_PAGE_ACCESS_TOKEN}")
echo "$FB_RESPONSE"
```

- Response contains `"id"` → success. Say "Facebook posted ✓"
- Response contains `"error"` → extract `error.message`, display it, do not retry.

---

### Post to LinkedIn

LinkedIn requires the post text and article URL combined into a JSON payload. The article URL becomes a content card (LinkedIn scrapes the OG image automatically).

Use `LINKEDIN_AUTHOR_URN` from `.env` — either `urn:li:person:{id}` (personal profile) or `urn:li:organization:{id}` (company page).

```bash
source /Users/buithang/timbre/.env
LI_PAYLOAD=$(python3 -c "
import json, sys
text = sys.argv[1]
url  = sys.argv[2]
urn  = sys.argv[3]
print(json.dumps({
  'author': urn,
  'lifecycleState': 'PUBLISHED',
  'specificContent': {
    'com.linkedin.ugc.ShareContent': {
      'shareCommentary': {'text': text},
      'shareMediaCategory': 'ARTICLE',
      'media': [{'status': 'READY', 'originalUrl': url}]
    }
  },
  'visibility': {
    'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
  }
}))
" "$LI_TEXT" "$LI_LINK" "$LINKEDIN_AUTHOR_URN")

LI_RESPONSE=$(curl -s -X POST "https://api.linkedin.com/v2/ugcPosts" \
  -H "Authorization: Bearer ${LINKEDIN_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -d "$LI_PAYLOAD")
echo "$LI_RESPONSE"
```

Before running, set:
- `LI_TEXT` = LinkedIn post body (without the article URL — it appears as the content card)
- `LI_LINK` = article URL

- Empty response or response contains `"id"` → success. Say "LinkedIn posted ✓"
- Response contains `"errorDetails"` or `"message"` → display the error, do not retry.

---

### Post to Threads

For single Threads post: create container → publish.
For multi-post thread (3–5 posts): create and publish post 1, then create and publish each subsequent post as a reply with `reply_to_id` pointing to post 1's ID.

**Step 1 — Get user ID:**
```bash
source /Users/buithang/timbre/.env
curl -s "https://graph.threads.net/v1.0/me?fields=id&access_token=${THREADS_ACCESS_TOKEN}"
```

**Step 2 — Create container for each post:**
```bash
source /Users/buithang/timbre/.env
# First post (no reply_to_id)
CONTAINER=$(curl -s -X POST "https://graph.threads.net/v1.0/${THREADS_USER_ID}/threads" \
  --data-urlencode "text=${POST_TEXT}" \
  -d "media_type=TEXT" \
  -d "access_token=${THREADS_ACCESS_TOKEN}")
CONTAINER_ID=$(echo "$CONTAINER" | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")

# Reply posts (add reply_to_id=${FIRST_POST_ID} after publishing post 1)
```

**Step 3 — Publish (wait 3s after container creation before publishing):**
```bash
source /Users/buithang/timbre/.env
sleep 3
PUBLISH=$(curl -s -X POST "https://graph.threads.net/v1.0/${THREADS_USER_ID}/threads_publish" \
  -d "creation_id=${CONTAINER_ID}" \
  -d "access_token=${THREADS_ACCESS_TOKEN}")
echo "$PUBLISH"
```

- Response contains `"id"` → success. Say "Threads posted ✓"
- Response contains `"error"` → extract `error.message`, display it. If error_subcode is 190 (expired token): say "Threads token expired — refresh at Meta developer dashboard and update THREADS_ACCESS_TOKEN in /Users/buithang/timbre/.env"

---

### Post summary

```
--- POST SUMMARY ---
Facebook: ✓ posted / ✗ failed — [error message] / — skipped (not selected / no credentials)
LinkedIn: ✓ posted / ✗ failed — [error message] / — skipped (not selected / no credentials)
Threads:  ✓ posted / ✗ failed — [error message] / — skipped (not selected / no token)
```

---

## What This Skill Does NOT Do

- Does not create content from scratch — use /content-seo for that
- Does not post to X — X API requires a paid plan
- Does not rewrite the article — it recaps and adapts
- Does not skip the posting prompt — user selects platforms before any post is sent
