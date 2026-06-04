#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f node_modules/.bin/wrangler ]]; then
  npm install
fi

echo "Deploying Roatan Excursion Planner to Cloudflare..."
npx wrangler deploy

echo "Done. Check https://roatanexcursionplanner.com/ shortly."
