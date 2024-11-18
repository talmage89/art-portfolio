#!/bin/bash

#
# Run frontend deployment from repo root
#
# ```bash
# bash ./server/deploy_frontend.sh
# ```
#

set -e

echo -e "\n\n🚀 Starting frontend deployment..."

echo -e "\n\n📥 Pulling latest changes...\n\n"
git pull

echo -e "\n\n🏗️ Building frontend...\n"
cd frontend
npm install
npm run build
cd ..

echo -e "\n\n🔄 Restarting services..."
sudo systemctl reload nginx

echo -e "\n\n✅ Frontend deployment complete!\n\n" 