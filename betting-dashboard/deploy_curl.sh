#!/bin/bash
# Netlify deploy using curl
set -e

TOKEN="nfp_fGAN5ehwsHaD87oZmJ24AF2Gvi473ZnQ216c"
SITE_ID="3d225a22-04e0-40fa-9629-0fb0f9cb8d40"
DIST_DIR="/c/Users/irfan/rakyathub/betting-dashboard/dist"

cd "$DIST_DIR"

# Build files manifest with SHA256 hashes
MANIFEST="{"
FIRST=true
while IFS= read -r -d '' FILE; do
    REL="${FILE#./}"
    SHA=$(sha256sum "$FILE" | cut -d' ' -f1)
    if [ "$FIRST" = true ]; then
        FIRST=false
    else
        MANIFEST="$MANIFEST,"
    fi
    MANIFEST="$MANIFEST\"$REL\":\"$SHA\""
done < <(find . -type f -print0)
MANIFEST="$MANIFEST}"

echo "Files manifest prepared."

# Create deploy
echo "Creating deploy..."
DEPLOY_RESP=$(curl -s --max-time 30 -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.netlify.com/api/v1/sites/$SITE_ID/deploys" \
  -d "{\"files\":$MANIFEST}")

DEPLOY_ID=$(echo "$DEPLOY_RESP" | python -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null)
STATE=$(echo "$DEPLOY_RESP" | python -c "import sys,json; print(json.load(sys.stdin).get('state',''))" 2>/dev/null)

echo "Deploy ID: $DEPLOY_ID"
echo "State: $STATE"

if [ -z "$DEPLOY_ID" ]; then
    echo "Failed to create deploy"
    echo "$DEPLOY_RESP"
    exit 1
fi

# Upload each file
while IFS= read -r -d '' FILE; do
    REL="${FILE#./}"
    SHA=$(sha256sum "$FILE" | cut -d' ' -f1)
    echo "Uploading $REL..."
    
    # Try by path
    HTTP_CODE=$(curl -s --max-time 30 -o /dev/null -w "%{http_code}" \
      -X PUT \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/octet-stream" \
      --data-binary @"$FILE" \
      "https://api.netlify.com/api/v1/deploys/$DEPLOY_ID/files/$REL")
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo "  OK (path)"
    else
        # Try by SHA
        HTTP_CODE2=$(curl -s --max-time 30 -o /dev/null -w "%{http_code}" \
          -X PUT \
          -H "Authorization: Bearer $TOKEN" \
          -H "Content-Type: application/octet-stream" \
          --data-binary @"$FILE" \
          "https://api.netlify.com/api/v1/deploys/$DEPLOY_ID/files/$SHA")
        
        if [ "$HTTP_CODE2" = "200" ]; then
            echo "  OK (SHA)"
        else
            echo "  FAIL: path=$HTTP_CODE sha=$HTTP_CODE2"
        fi
    fi
done < <(find . -type f -print0)

# Lock deploy
echo "Locking deploy..."
LOCK_CODE=$(curl -s --max-time 15 -o /dev/null -w "%{http_code}" \
  -X POST \
  -H "Authorization: Bearer $TOKEN" \
  "https://api.netlify.com/api/v1/deploys/$DEPLOY_ID/lock")
echo "Lock: $LOCK_CODE"

# Wait for ready
echo "Waiting for deploy..."
for i in $(seq 1 15); do
    sleep 4
    STATUS=$(curl -s --max-time 15 \
      -H "Authorization: Bearer $TOKEN" \
      "https://api.netlify.com/api/v1/deploys/$DEPLOY_ID" | python -c "
import sys, json
d = json.load(sys.stdin)
s = d.get('state','')
pub = d.get('published_at','')
err = d.get('error_message','')
print(f'{s} pub={pub} err={err}')
" 2>/dev/null)
    echo "  [$i] $STATUS"
    if echo "$STATUS" | grep -q "pub=" && ! echo "$STATUS" | grep -q "pub=None"; then
        break
    fi
    if echo "$STATUS" | grep -q "err=" && ! echo "$STATUS" | grep -q "err= none"; then
        break
    fi
done

echo ""
echo "URL: https://sportmania-betting.netlify.app"
