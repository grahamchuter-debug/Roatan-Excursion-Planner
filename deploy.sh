#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f node_modules/.bin/wrangler ]]; then
  npm install
fi

echo "Building Roatan Excursion Planner (World 2.0 finalize)..."
npm run build

echo "Deploying Roatan Excursion Planner to Cloudflare Workers Assets..."
npx wrangler deploy

echo "Done. Check https://roatanexcursionplanner.com/ shortly."
