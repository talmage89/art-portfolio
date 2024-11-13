#!/bin/bash

#
# RUN DEPLOYMENT FROM REPO ROOT
#
# ```bash
# ./server/deploy.sh
# ```
#

set -e

echo "🚀 Starting deployment..."

echo "📥 Pulling latest changes..."
git pull

echo "🏗️ Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "🧱 Updating backend..."
cd backend
source venv/bin/activate
pip-compile --upgrade requirements.in
pip-sync requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
deactivate
cd ..

echo "🔄 Restarting services..."
sudo systemctl restart gunicorn
sudo systemctl reload nginx

echo "✅ Deployment complete!"
