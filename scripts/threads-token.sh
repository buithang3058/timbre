#!/bin/bash
# Usage:
#   Exchange short-lived token:  ./threads-token.sh exchange <short_lived_token>
#   Refresh long-lived token:    ./threads-token.sh refresh

ENV_FILE="$(dirname "$0")/../.env"

exchange() {
  local SHORT_TOKEN="$1"
  local APP_SECRET=$(grep "^THREADS_APP_SECRET=" "$ENV_FILE" | cut -d= -f2-)

  if [ -z "$APP_SECRET" ]; then
    echo "Error: THREADS_APP_SECRET not found in $ENV_FILE"
    exit 1
  fi

  echo "Exchanging short-lived token..."
  RESULT=$(curl -s "https://graph.threads.net/access_token?grant_type=th_exchange_token&client_secret=${APP_SECRET}&access_token=${SHORT_TOKEN}")
  TOKEN=$(echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['access_token'])" 2>/dev/null)
  EXPIRES_IN=$(echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('expires_in',5184000))" 2>/dev/null)

  if [ -z "$TOKEN" ]; then
    echo "Error: $(echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('error',{}).get('message','unknown'))" 2>/dev/null)"
    exit 1
  fi

  EXPIRES_IN=${EXPIRES_IN:-5184000}
  EXPIRES_AT=$(( $(date +%s) + EXPIRES_IN ))
  save_token "$TOKEN" "$EXPIRES_AT"
  echo "Long-lived token saved. Expires in $(( EXPIRES_IN / 86400 )) days."
}

refresh() {
  local CURRENT_TOKEN=$(grep "^THREADS_ACCESS_TOKEN=" "$ENV_FILE" | cut -d= -f2-)
  local EXPIRES_AT=$(grep "^THREADS_TOKEN_EXPIRES_AT=" "$ENV_FILE" | cut -d= -f2-)
  local NOW=$(date +%s)

  if [ -z "$CURRENT_TOKEN" ] || [ -z "$EXPIRES_AT" ]; then
    echo "No token stored. Run: $0 exchange <short_lived_token>"
    exit 1
  fi

  local DAYS_LEFT=$(( (EXPIRES_AT - NOW) / 86400 ))

  if [ "$DAYS_LEFT" -gt 7 ]; then
    echo "Token still valid for $DAYS_LEFT days — no refresh needed."
    exit 0
  fi

  echo "Token expires in $DAYS_LEFT days. Refreshing..."
  RESULT=$(curl -s "https://graph.threads.net/refresh_access_token?grant_type=th_refresh_token&access_token=${CURRENT_TOKEN}")
  TOKEN=$(echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['access_token'])" 2>/dev/null)
  EXPIRES_IN=$(echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('expires_in',5184000))" 2>/dev/null)

  if [ -z "$TOKEN" ]; then
    echo "Refresh failed: $(echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('error',{}).get('message','unknown'))" 2>/dev/null)"
    exit 1
  fi

  EXPIRES_IN=${EXPIRES_IN:-5184000}
  EXPIRES_AT=$(( NOW + EXPIRES_IN ))
  save_token "$TOKEN" "$EXPIRES_AT"
  echo "Token refreshed. Valid for another $(( EXPIRES_IN / 86400 )) days."
}

save_token() {
  local TOKEN="$1" EXPIRES_AT="$2"
  if grep -q "^THREADS_ACCESS_TOKEN=" "$ENV_FILE"; then
    sed -i '' "s|^THREADS_ACCESS_TOKEN=.*|THREADS_ACCESS_TOKEN=${TOKEN}|" "$ENV_FILE"
  else
    echo "THREADS_ACCESS_TOKEN=${TOKEN}" >> "$ENV_FILE"
  fi
  if grep -q "^THREADS_TOKEN_EXPIRES_AT=" "$ENV_FILE"; then
    sed -i '' "s|^THREADS_TOKEN_EXPIRES_AT=.*|THREADS_TOKEN_EXPIRES_AT=${EXPIRES_AT}|" "$ENV_FILE"
  else
    echo "THREADS_TOKEN_EXPIRES_AT=${EXPIRES_AT}" >> "$ENV_FILE"
  fi
}

case "$1" in
  exchange) exchange "$2" ;;
  refresh)  refresh ;;
  *) echo "Usage: $0 exchange <short_token> | refresh" ;;
esac
