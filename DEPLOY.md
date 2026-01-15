# L'amitié 2025 - Deployment Guide

## 🚀 Automatic Deployment (Recommended)

**Just push to GitHub and relax!** 

The GitHub Actions workflow automatically deploys everything:

```bash
git add -A
git commit -m "Your changes"
git push
```

That's it! GitHub Actions will:
1. ✅ Build the frontend
2. ✅ Deploy backend code
3. ✅ Install Python dependencies
4. ✅ Deploy frontend to nginx
5. ✅ Restart services

Check deployment status: [GitHub Actions](https://github.com/shaveenudayanga/lamitie-25/actions)

---

## 🛠️ Manual Deployment (Backup Method)

If GitHub Actions fails or you need to deploy manually:

```bash
./deploy.sh
```

**Note:** Manual deployment is slower. Use automatic deployment whenever possible.

---

If you need to deploy manually:

### Backend:

```bash
# SSH into server
ssh -i bot-testing_key.pem gamesploit@20.120.179.111

# Pull latest code (if git is set up)
cd /home/gamesploit/lamitie-25/backend

# Install dependencies
./.venv/bin/pip install -r requirements.txt

# Restart service
sudo systemctl restart lamitie.service
```

### Frontend:

```bash
# SSH into server
ssh -i bot-testing_key.pem gamesploit@20.120.179.111

# Build frontend
cd /home/gamesploit/lamitie-25/frontend
npm install
npm run build

# Deploy to nginx
sudo rm -rf /var/www/html/*
sudo cp -r dist/* /var/www/html/
```

## 🔐 Authentication

- **Password:** `Lam#&faS25`
- All endpoints except `/auth/login` are protected
- Users must log in at `/login` before accessing the app

## 📝 Common Issues

### Backend 500 Errors
- Check logs: `sudo journalctl -u lamitie.service -n 50`
- Restart service: `sudo systemctl restart lamitie.service`

### Frontend Not Updating
- Clear browser cache
- Check nginx is serving from `/var/www/html`

### Database Columns Missing
- The production database doesn't have `created_at` and `updated_at` columns yet
- The model has been updated to not use them for now

## 🔧 Server Info

- **IP:** 20.120.179.111
- **SSH User:** gamesploit
- **Backend Path:** /home/gamesploit/lamitie-25/backend
- **Frontend Path:** /home/gamesploit/lamitie-25/frontend
- **Service:** lamitie.service
- **Nginx Root:** /var/www/html
