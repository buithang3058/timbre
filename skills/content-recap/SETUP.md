# content-recap — Social Auto-Post Setup

Add these 4 variables to `/Users/buithang/timbre/.env`:

```
FB_PAGE_ID=
FB_PAGE_ACCESS_TOKEN=
THREADS_USER_ID=
THREADS_ACCESS_TOKEN=
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

## Threads Setup

Threads API uses Meta's Graph API with a separate token.

### Step 1 — Enable Threads API access

1. Go to https://developers.facebook.com/apps/
2. Open your app (same one from Facebook setup, or create a new one)
3. Add the **Threads API** product
4. Under Threads API → **Permissions**: request `threads_basic` and `threads_content_publish`

### Step 2 — Get your Threads User ID

1. Use the Graph API Explorer: https://developers.facebook.com/tools/explorer/
2. Select your app, generate a token with Threads permissions
3. Make a GET request to: `https://graph.threads.net/v1.0/me?fields=id,username`
4. Copy the `id` value
5. Add to `.env`: `THREADS_USER_ID=your_threads_user_id`

### Step 3 — Get a Threads access token

1. In the Graph API Explorer, generate a token with `threads_basic` and `threads_content_publish` permissions
2. Exchange for a long-lived token (60 days):

```bash
curl "https://graph.threads.net/refresh_access_token?grant_type=th_refresh_token&access_token=SHORT_LIVED_TOKEN"
```

3. Add to `.env`: `THREADS_ACCESS_TOKEN=your_threads_token`

---

## Verify setup

Run this to confirm all 4 vars are loaded:

```bash
source /Users/buithang/timbre/.env
echo "FB_PAGE_ID: ${FB_PAGE_ID:0:6}..."
echo "FB_PAGE_ACCESS_TOKEN: ${FB_PAGE_ACCESS_TOKEN:0:8}..."
echo "THREADS_USER_ID: ${THREADS_USER_ID:0:6}..."
echo "THREADS_ACCESS_TOKEN: ${THREADS_ACCESS_TOKEN:0:8}..."
```

## Token expiry

| Token | Expiry | Refresh |
|-------|--------|---------|
| FB Page access token | Never (if generated correctly) | Re-run Step 3 |
| Threads access token | 60 days | Run the refresh curl command above |
