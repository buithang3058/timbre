#!/bin/bash
# auto-social.sh — detect new articles and auto-post to Facebook + LinkedIn
# Called by tokemist deploy.sh after each deployment

set -e

TIMBRE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SEEN_FILE="$TIMBRE_DIR/seen-urls.txt"
SITEMAP_URL="https://tokemist.com/sitemap.xml"
CONTENT_DIR="${TOKEMIST_CONTENT_DIR:-/Users/buithang/tokemist/web/content}"

# Load credentials
source "$TIMBRE_DIR/.env"

# Article URLs come from the content dir (articles live at root level since the
# /vn/ prefix was removed, so the sitemap alone can't tell them apart from hub
# pages). Stubs are excluded. Only URLs also present in the live sitemap are
# considered, so unpublished content is never posted.
CANDIDATE_URLS=$(grep -L "^type: stub" "$CONTENT_DIR"/*/*/index.mdx \
  | xargs -n1 dirname | xargs -n1 basename \
  | sed 's|^|https://tokemist.com/|;s|$|/|')

SITEMAP_URLS=$(curl -s "$SITEMAP_URL" | grep -o '<loc>[^<]*</loc>' | sed 's/<[^>]*>//g')

CURRENT_URLS=$(comm -12 \
  <(echo "$CANDIDATE_URLS" | sort) \
  <(echo "$SITEMAP_URLS" | sort))

# Find new URLs (in sitemap but not in seen file)
NEW_URLS=$(comm -23 \
  <(echo "$CURRENT_URLS" | sort) \
  <(sort "$SEEN_FILE" 2>/dev/null || true))

if [ -z "$NEW_URLS" ]; then
  echo "[auto-social] No new articles found."
  exit 0
fi

echo "[auto-social] New articles detected:"
echo "$NEW_URLS"

# Post each new article
while IFS= read -r URL; do
  [ -z "$URL" ] && continue
  echo "[auto-social] Posting: $URL"

  # Fetch article OG data
  HTML=$(curl -s "$URL")
  TITLE=$(echo "$HTML" | grep -o 'og:title" content="[^"]*"' | head -1 | sed 's/og:title" content="//;s/"//')
  DESC=$(echo "$HTML" | grep -o 'og:description" content="[^"]*"' | head -1 | sed 's/og:description" content="//;s/"//')

  # Build post text from title + description
  POST_TEXT="$TITLE

$DESC

Đọc đầy đủ:"

  # --- Facebook ---
  curl -s -X POST "https://graph.facebook.com/?id=${URL}&scrape=true&access_token=${FB_PAGE_ACCESS_TOKEN}" > /dev/null

  FB_RESPONSE=$(curl -s -X POST "https://graph.facebook.com/v19.0/${FB_PAGE_ID}/feed" \
    --data-urlencode "message=${POST_TEXT}" \
    --data-urlencode "link=${URL}" \
    -d "access_token=${FB_PAGE_ACCESS_TOKEN}")

  if echo "$FB_RESPONSE" | grep -q '"id"'; then
    echo "[auto-social] Facebook ✓"
  else
    echo "[auto-social] Facebook ✗: $FB_RESPONSE"
  fi

  # --- LinkedIn ---
  LI_PAYLOAD=$(python3 -c "
import json, sys
print(json.dumps({
  'author': '${LINKEDIN_AUTHOR_URN}',
  'lifecycleState': 'PUBLISHED',
  'specificContent': {
    'com.linkedin.ugc.ShareContent': {
      'shareCommentary': {'text': sys.argv[1]},
      'shareMediaCategory': 'ARTICLE',
      'media': [{'status': 'READY', 'originalUrl': sys.argv[2]}]
    }
  },
  'visibility': {
    'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
  }
}))
" "$POST_TEXT" "$URL")

  LI_RESPONSE=$(curl -s -X POST "https://api.linkedin.com/v2/ugcPosts" \
    -H "Authorization: Bearer ${LINKEDIN_ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -H "X-Restli-Protocol-Version: 2.0.0" \
    -d "$LI_PAYLOAD")

  if echo "$LI_RESPONSE" | grep -q '"id"'; then
    echo "[auto-social] LinkedIn ✓"
  else
    echo "[auto-social] LinkedIn ✗: $LI_RESPONSE"
  fi

  # Mark as seen
  echo "$URL" >> "$SEEN_FILE"
  echo "[auto-social] Done: $URL"
  echo "---"

done <<< "$NEW_URLS"

echo "[auto-social] All done."
