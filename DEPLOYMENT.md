# Deployment Guide

This guide provides step-by-step instructions for deploying the AI Feedback System to various platforms.

## Prerequisites

- GitHub account
- API key from Google Gemini (get it from https://makersuite.google.com/app/apikey)
- MongoDB Atlas account (free tier) - See [MONGODB_SETUP.md](MONGODB_SETUP.md) for detailed setup

## Deployment Options

### Option 1: Render (Recommended - Easiest)

**Before deploying, set up MongoDB Atlas** - See [MONGODB_SETUP.md](MONGODB_SETUP.md) for complete instructions.

1. **Push to GitHub**
   - Create a new repository on GitHub
   - Push all project files to the repository
   - **Important**: Make sure `.env` is NOT committed (it's in `.gitignore`)

2. **Create Render Account**
   - Go to https://render.com
   - Sign up or log in with your GitHub account

3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

4. **Configure Service**
   - **Name**: `ai-feedback-system` (or your preferred name)
   - **Region**: Choose closest to you
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty (or `.` if needed)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

5. **Add Environment Variables**
   - Go to "Environment" tab
   - Add the following variables:
     - **Key**: `GEMINI_API_KEY`
       **Value**: Your Gemini API key
     - **Key**: `MONGODB_URI`
       **Value**: Your MongoDB Atlas connection string
       (Format: `mongodb+srv://username:password@cluster.mongodb.net/feedback_db?retryWrites=true&w=majority`)
   - Click "Save Changes"

6. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete (2-3 minutes)
   - Check the logs to verify:
     - `✓ MongoDB connected successfully`
     - `✓ Gemini API configured successfully`
   - Your app will be live at: `https://your-app-name.onrender.com`

**Note**: 
- Free tier on Render spins down after inactivity. First request may take 30-60 seconds.
- Make sure MongoDB Atlas Network Access allows connections from anywhere (0.0.0.0/0) for Render to connect.

---

### Option 2: Heroku

1. **Install Heroku CLI**
   - Download from https://devcenter.heroku.com/articles/heroku-cli

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

4. **Set Environment Variable**
   ```bash
   heroku config:set GEMINI_API_KEY=your_api_key_here
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Open App**
   ```bash
   heroku open
   ```

---

### Option 3: Railway

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure**
   - Railway auto-detects Python
   - Add environment variable: `GEMINI_API_KEY`

4. **Deploy**
   - Railway automatically deploys
   - Get your public URL from the dashboard

---

### Option 4: HuggingFace Spaces

1. **Create Space**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"

2. **Configure Space**
   - **Space name**: `ai-feedback-system`
   - **SDK**: `Docker`
   - **Hardware**: CPU Basic (free)

3. **Upload Files**
   - Upload all project files
   - Create `Dockerfile` (see below)

4. **Set Secrets**
   - Go to Settings → Secrets
   - Add `GEMINI_API_KEY`

5. **Dockerfile for HuggingFace**:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 7860
   CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
   ```

---

## Post-Deployment Checklist

- [ ] Test User Dashboard: Submit a review
- [ ] Test Admin Dashboard: Verify feedback appears
- [ ] Check AI responses are generated
- [ ] Verify analytics are updating
- [ ] Test on mobile devices (responsive design)

## Troubleshooting

### App not starting
- Check logs in your deployment platform
- Verify `GEMINI_API_KEY` is set correctly
- Ensure `requirements.txt` is correct

### AI features not working
- Verify API key is valid
- Check API quota/limits
- Review error logs

### Data not persisting
- ✅ **This is now solved!** The app uses MongoDB Atlas for persistent storage
- If data isn't saving, check:
  - MongoDB connection string is correct in environment variables
  - MongoDB Atlas Network Access allows connections (0.0.0.0/0 for Render)
  - Check application logs for MongoDB connection errors

## URLs After Deployment

After successful deployment, you'll have:
- **User Dashboard**: `https://your-app-url.com/`
- **Admin Dashboard**: `https://your-app-url.com/admin`

## Production Recommendations

1. ✅ **Database**: Now using MongoDB Atlas (persistent, cloud-hosted)
2. **Authentication**: Add admin authentication for admin dashboard
3. **Rate Limiting**: Implement to prevent abuse
4. **Error Monitoring**: Add Sentry or similar
5. ✅ **Backup**: MongoDB Atlas free tier includes automated daily backups
6. **SSL/HTTPS**: Render provides HTTPS by default ✅

