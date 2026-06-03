# content-recap — Social Auto-Post Setup

Add these variables to `/Users/buithang/timbre/.env`:

```
FB_PAGE_ID=
FB_PAGE_ACCESS_TOKEN=
LINKEDIN_ACCESS_TOKEN=
LINKEDIN_AUTHOR_URN=
```

---

## Facebook Setup

You need a **Facebook Page** (not personal profile) and a **Page access token**.

### Step 1 — Create a Facebook developer app

1. Go to https://developers.facebook.com/apps/
2. Click **Create App** → choose **Other** → **Business**
3. Name it anything (e.g. "timbre-poster")
4. Add the **Pages API** product

### Step 2 — Get your Page ID

1. Go to your Facebook Page
2. Click **About** → scroll to the bottom
3. Copy the **Page ID** (a long number)
4. Add to `.env`: `FB_PAGE_ID=your_page_id`

### Step 3 — Get a long-lived Page access token

1. Go to https://developers.facebook.com/tools/explorer/
2. Select your app from the dropdown
3. Click **Generate Access Token** — grant `pages_manage_posts` and `pages_read_engagement` permissions
4. Copy the short-lived token
5. Exchange for a long-lived token (60 days):

```bash
curl "https://graph.facebook.com/v19.0/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=SHORT_LIVED_TOKEN"
```

6. Use the returned token to get the **Page token** (which never expires):

```bash
curl "https://graph.facebook.com/v19.0/me/accounts?access_token=LONG_LIVED_USER_TOKEN"
```

Find your page in the response. Copy its `access_token`.

7. Add to `.env`: `FB_PAGE_ACCESS_TOKEN=your_page_token`

---

## LinkedIn Setup

LinkedIn supports posting to your **personal profile** or a **company page** — same setup, different URN.

### Step 1 — Create a LinkedIn developer app

1. Go to https://www.linkedin.com/developers/apps/new
2. Fill in app name (e.g. "timbre-poster"), associate with a LinkedIn Page (required, can be a dummy page)
3. Under **Products** → request **Share on LinkedIn** and **Sign In with LinkedIn using OpenID Connect**
4. Wait for approval (usually instant for Share on LinkedIn)

### Step 2 — Get an access token

1. Go to your app → **Auth** tab
2. Copy your **Client ID** and **Client Secret**
3. Add `https://www.linkedin.com/developers/tools/oauth/redirect` as a redirect URL under **OAuth 2.0 settings**
4. Go to the OAuth 2.0 token generator: https://www.linkedin.com/developers/tools/oauth
5. Select your app, check `w_member_social` (personal) and/or `w_organization_social` (company page)
6. Click **Request access token** → authorize
7. Copy the token
8. Add to `.env`: `LINKEDIN_ACCESS_TOKEN=your_token`

Token expiry: 60 days. Refresh by repeating step 4-8.

### Step 3 — Get your Author URN

**For personal profile:**
```bash
curl -s -H "Authorization: Bearer YOUR_TOKEN" "https://api.linkedin.com/v2/userinfo" | python3 -c "import json,sys; d=json.load(sys.stdin); print('urn:li:person:' + d['sub'])"
```

**For company page:**
```bash
curl -s -H "Authorization: Bearer YOUR_TOKEN" "https://api.linkedin.com/v2/organizationAcls?q=roleAssignee" | python3 -c "import json,sys; d=json.load(sys.stdin); [print(e['organization']) for e in d.get('elements',[])]"
```
This returns your org URN (e.g. `urn:li:organization:12345678`).

Add to `.env`: `LINKEDIN_AUTHOR_URN=urn:li:person:ABC123` (or `urn:li:organization:12345678` for a page)

---

## Verify setup

```bash
source /Users/buithang/timbre/.env
echo "FB_PAGE_ID: ${FB_PAGE_ID:0:6}..."
echo "FB_PAGE_ACCESS_TOKEN: ${FB_PAGE_ACCESS_TOKEN:0:8}..."
echo "LINKEDIN_ACCESS_TOKEN: ${LINKEDIN_ACCESS_TOKEN:0:8}..."
echo "LINKEDIN_AUTHOR_URN: ${LINKEDIN_AUTHOR_URN}"
```

## Token expiry

| Token | Expiry | Refresh |
|-------|--------|---------|
| FB Page access token | Never (if generated correctly) | Re-run Facebook Step 3 |
| LinkedIn access token | 60 days | Re-run LinkedIn Step 4-8 |
