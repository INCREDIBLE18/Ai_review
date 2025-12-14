# Complete Deployment Steps - Quick Reference

Follow these steps in order to deploy your AI Feedback System to Render with MongoDB.

## Step 1: Set Up MongoDB Atlas (15 minutes)

📖 **Full Guide**: See [MONGODB_SETUP.md](MONGODB_SETUP.md)

**Quick Steps**:
1. Sign up at https://www.mongodb.com/cloud/atlas/register
2. Create a FREE M0 cluster
3. Create a database user (save username & password!)
4. Add Network Access: Allow from anywhere (0.0.0.0/0)
5. Get connection string: `mongodb+srv://username:password@cluster.mongodb.net/feedback_db?retryWrites=true&w=majority`
6. **Save this connection string** - you'll need it for Render!

## Step 2: Prepare Your Code

1. **Verify all files are ready**:
   ```bash
   # Check these files exist:
   - app.py
   - requirements.txt
   - Procfile
   - render.yaml
   - static/user_dashboard.html
   - static/admin_dashboard.html
   ```

2. **Test locally** (optional but recommended):
   ```bash
   # Create .env file with:
   GEMINI_API_KEY=your_gemini_key
   MONGODB_URI=your_mongodb_connection_string
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run locally
   python app.py
   
   # Test at http://localhost:5000
   # Check console for: ✓ MongoDB connected successfully
   ```

## Step 3: Push to GitHub

1. **Initialize Git** (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - AI Feedback System"
   ```

2. **Create GitHub Repository**:
   - Go to https://github.com/new
   - Create a new repository (public or private)
   - **Don't** initialize with README (you already have one)

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git branch -M main
   git push -u origin main
   ```

## Step 4: Deploy to Render

1. **Sign up/Login to Render**:
   - Go to https://render.com
   - Sign up with GitHub (recommended)

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub account (if not already)
   - Select your repository

3. **Configure Service**:
   - **Name**: `ai-feedback-system` (or your choice)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

4. **Add Environment Variables**:
   - Click "Advanced" → "Add Environment Variable"
   - Add **GEMINI_API_KEY**:
     - Key: `GEMINI_API_KEY`
     - Value: Your Gemini API key
   - Add **MONGODB_URI**:
     - Key: `MONGODB_URI`
     - Value: Your MongoDB connection string from Step 1
   - Click "Save Changes"

5. **Deploy**:
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment
   - Watch the logs for:
     - `✓ MongoDB connected successfully`
     - `✓ Gemini API configured successfully`

## Step 5: Verify Deployment

1. **Check Your URLs**:
   - User Dashboard: `https://your-app-name.onrender.com/`
   - Admin Dashboard: `https://your-app-name.onrender.com/admin`

2. **Test the Application**:
   - Submit a test review from User Dashboard
   - Check Admin Dashboard to see if it appears
   - Verify AI responses are generated

3. **Check MongoDB Atlas**:
   - Go to MongoDB Atlas → Database → Browse Collections
   - You should see `feedback_db` database with `feedback` collection
   - Your test submission should be there!

## Troubleshooting

### Deployment Fails

**Check Build Logs**:
- Go to Render → Your Service → Logs
- Look for error messages
- Common issues:
  - Missing dependencies in `requirements.txt`
  - Syntax errors in code
  - Missing files

### MongoDB Connection Fails

**Check**:
1. Connection string is correct in Render environment variables
2. MongoDB Atlas Network Access allows 0.0.0.0/0
3. Username and password are correct (no special characters need encoding)
4. Check Render logs for specific error messages

### AI Not Working

**Check**:
1. `GEMINI_API_KEY` is set correctly in Render
2. API key is valid (test at https://makersuite.google.com/app/apikey)
3. Check Render logs for API errors

### App Shows "Spinning Down"

**This is normal** on Render free tier:
- App spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Subsequent requests are fast
- Consider upgrading to paid tier for always-on

## Success Checklist

- [ ] MongoDB Atlas cluster created and running
- [ ] Database user created
- [ ] Network access configured (0.0.0.0/0)
- [ ] Connection string saved
- [ ] Code pushed to GitHub
- [ ] Render service created
- [ ] Environment variables set in Render
- [ ] Deployment successful
- [ ] User dashboard accessible
- [ ] Admin dashboard accessible
- [ ] Test submission works
- [ ] Data appears in MongoDB Atlas

## Your Deployment URLs

After successful deployment, you'll have:

```
User Dashboard: https://your-app-name.onrender.com/
Admin Dashboard: https://your-app-name.onrender.com/admin
```

**Save these URLs for your submission!** 🎉

## Next Steps

1. Test thoroughly on both dashboards
2. Submit your deployment URLs
3. Monitor MongoDB Atlas for data
4. Check Render logs periodically

---

**Need Help?**
- MongoDB Setup: See [MONGODB_SETUP.md](MONGODB_SETUP.md)
- Full Deployment Guide: See [DEPLOYMENT.md](DEPLOYMENT.md)
- Quick Start: See [QUICKSTART.md](QUICKSTART.md)

