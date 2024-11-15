#!/bin/bash

#
# Run deployment from repo root. Make sure you have pip-tools installed in the backend venv.
#
# ```bash
# bash ./server/deploy.sh
# ```
#

set -e

echo -e "\n\n🚀 Starting deployment..."

echo -e "\n\n📥 Pulling latest changes...\n\n"
git pull

echo -e "\n\n🏗️ Building frontend...\n\n"
cd frontend
npm install
npm run build
cd ..

echo -e "\n\n🧱 Updating backend...\n\n"
cd backend
source venv/bin/activate
pip-compile --upgrade requirements.in
pip-sync requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
deactivate
cd ..

echo -e "\n\n🔄 Restarting services..."
sudo systemctl restart gunicorn
sudo systemctl reload nginx

echo -e "\n\n✅ Deployment complete!\n\n"
