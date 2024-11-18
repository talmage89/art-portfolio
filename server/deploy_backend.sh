#!/bin/bash

#
# Run backend deployment from repo root. Make sure you have pip-tools installed in the backend venv.
#
# ```bash
# bash ./server/deploy_backend.sh
# ```
#

set -e

echo -e "\n\n🚀 Starting backend deployment..."

echo -e "\n\n📥 Pulling latest changes...\n\n"
git pull

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
sudo systemctl restart gunicorn.service
sudo systemctl reload nginx

echo -e "\n\n✅ Backend deployment complete!\n\n" 