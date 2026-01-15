#!/bin/bash

# Deployment script for L'amitié 2025
# Run this script after pushing code to GitHub to update the production server

set -e  # Exit on error

SERVER="gamesploit@20.120.179.111"
KEY="/Users/wathsarawunmal/Applications/lamitie-25/bot-testing_key.pem"
BACKEND_PATH="/home/gamesploit/lamitie-25/backend"
FRONTEND_PATH="/home/gamesploit/lamitie-25/frontend"

echo "🚀 Starting deployment to production server..."

# Function to run commands on server
run_remote() {
    ssh -i "$KEY" "$SERVER" "$@"
}

# 1. Update backend code
echo "📦 Updating backend files..."
scp -i "$KEY" -r backend/src "$SERVER:$BACKEND_PATH/"
scp -i "$KEY" -r backend/alembic "$SERVER:$BACKEND_PATH/"
scp -i "$KEY" backend/requirements.txt "$SERVER:$BACKEND_PATH/"
scp -i "$KEY" backend/alembic.ini "$SERVER:$BACKEND_PATH/" 2>/dev/null || true

# 2. Install/update Python packages if requirements changed
echo "📚 Checking Python dependencies..."
run_remote "cd $BACKEND_PATH && ./.venv/bin/pip install -r requirements.txt --quiet"

# 3. Restart backend service
echo "🔄 Restarting backend service..."
run_remote "sudo systemctl restart lamitie.service"

# 4. Update frontend code
echo "🎨 Updating frontend files..."
scp -i "$KEY" -r frontend/src "$SERVER:$FRONTEND_PATH/"
scp -i "$KEY" frontend/package.json "$SERVER:$FRONTEND_PATH/"
scp -i "$KEY" frontend/vite.config.ts "$SERVER:$FRONTEND_PATH/"
scp -i "$KEY" frontend/tsconfig.json "$SERVER:$FRONTEND_PATH/" 2>/dev/null || true

# 5. Rebuild frontend
echo "🏗️  Building frontend..."
run_remote "cd $FRONTEND_PATH && npm install --quiet && npm run build"

# 6. Deploy frontend build
echo "📤 Deploying frontend to nginx..."
run_remote "sudo rm -rf /var/www/html/* && sudo cp -r $FRONTEND_PATH/dist/* /var/www/html/"

# 7. Check service status
echo "✅ Checking service status..."
run_remote "sudo systemctl status lamitie.service --no-pager | head -10"

echo ""
echo "🎉 Deployment complete!"
echo "🌐 Visit: http://20.120.179.111"
echo "🔑 Login password: Lam#&faS25"
