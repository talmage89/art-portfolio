#!/bin/bash

#
# Run deployment from repo root. Make sure you have pip-tools installed.
#
# ```bash
# bash ./server/deploy.sh
# ```
#

set -e

echo "\n\n🚀 Starting deployment..."

echo "\n\n📥 Pulling latest changes...\n\n"
git pull

echo "\n\n🏗️ Building frontend...\n\n"
cd frontend
npm install
npm run build
cd ..

echo "\n\n🧱 Updating backend...\n\n"
cd backend
source venv/bin/activate
pip-compile --upgrade requirements.in
pip-sync requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
deactivate
cd ..

echo "\n\n🔄 Restarting services...\n\n"
sudo systemctl restart gunicorn
sudo systemctl reload nginx

echo "\n\n✅ Deployment complete!\n\n"
