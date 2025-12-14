# MongoDB Atlas Setup Guide

This guide will walk you through setting up MongoDB Atlas (free tier) for your AI Feedback System.

## Step 1: Create MongoDB Atlas Account

1. **Visit MongoDB Atlas**
   - Go to https://www.mongodb.com/cloud/atlas/register
   - Click "Try Free" or "Sign Up"

2. **Sign Up**
   - Use your email or sign up with Google/GitHub
   - Fill in your details and verify your email

## Step 2: Create a Free Cluster

1. **Choose Deployment Type**
   - After logging in, you'll see "Deploy a cloud database"
   - Select **"M0 FREE"** (Free Shared Cluster)
   - Click "Create"

2. **Choose Cloud Provider & Region**
   - Select a cloud provider (AWS, Google Cloud, or Azure)
   - Choose a region closest to you (or where you'll deploy)
   - Click "Create Cluster"

3. **Wait for Cluster Creation**
   - This takes 3-5 minutes
   - You'll see "Your cluster is being created"

## Step 3: Create Database User

1. **Set Up Database Access**
   - In the left sidebar, click "Database Access"
   - Click "Add New Database User"

2. **Configure User**
   - **Authentication Method**: Password
   - **Username**: Create a username (e.g., `feedback_admin`)
   - **Password**: 
     - Click "Autogenerate Secure Password" OR
     - Create your own strong password
   - **IMPORTANT**: Copy and save the password! You'll need it for the connection string.
   - **Database User Privileges**: "Atlas admin" (or "Read and write to any database")
   - Click "Add User"

## Step 4: Configure Network Access

1. **Allow IP Addresses**
   - In the left sidebar, click "Network Access"
   - Click "Add IP Address"

2. **Add IP Address**
   - For development: Click "Add Current IP Address"
   - For production (Render): Click "Allow Access from Anywhere" (0.0.0.0/0)
   - Click "Confirm"

   **Note**: For security, you can add specific IPs later, but for now, allow from anywhere to ensure your Render deployment can connect.

## Step 5: Get Connection String

1. **Go to Database**
   - In the left sidebar, click "Database"
   - Click "Connect" on your cluster

2. **Choose Connection Method**
   - Select "Drivers" (or "Connect your application")

3. **Get Connection String**
   - **Driver**: Python
   - **Version**: Latest (3.6 or later)
   - Copy the connection string
   - It looks like:
     ```
     mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
     ```

4. **Replace Placeholders**
   - Replace `<username>` with your database username
   - Replace `<password>` with your database password
   - Example:
     ```
     mongodb+srv://feedback_admin:MySecurePassword123@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
     ```

5. **Add Database Name (Optional but Recommended)**
   - Add the database name to the connection string:
     ```
     mongodb+srv://feedback_admin:MySecurePassword123@cluster0.xxxxx.mongodb.net/feedback_db?retryWrites=true&w=majority
     ```
   - The database name `feedback_db` will be created automatically when you first connect

## Step 6: Set Environment Variable

### For Local Development:

1. **Update `.env` file**
   - Open your `.env` file in the project root
   - Add the MongoDB connection string:
     ```
     MONGODB_URI=mongodb+srv://feedback_admin:MySecurePassword123@cluster0.xxxxx.mongodb.net/feedback_db?retryWrites=true&w=majority
     GEMINI_API_KEY=your_gemini_api_key_here
     ```
   - Replace with your actual connection string

2. **Test Connection**
   - Run your Flask app: `python app.py`
   - Check the console for: `✓ MongoDB connected successfully`

### For Render Deployment:

1. **Go to Render Dashboard**
   - Navigate to your service
   - Click "Environment" tab

2. **Add Environment Variable**
   - Click "Add Environment Variable"
   - **Key**: `MONGODB_URI`
   - **Value**: Your full MongoDB connection string
   - Click "Save Changes"

3. **Redeploy**
   - Render will automatically redeploy
   - Check logs to verify MongoDB connection

## Step 7: Verify Connection

1. **Check Application Logs**
   - When you start the app, you should see:
     ```
     ✓ MongoDB connected successfully
     ```

2. **Test Submission**
   - Submit a test feedback from the user dashboard
   - Check admin dashboard to see if it appears
   - If it works, MongoDB is connected!

3. **Verify in MongoDB Atlas**
   - Go to MongoDB Atlas → Database → Browse Collections
   - You should see:
     - Database: `feedback_db`
     - Collection: `feedback`
     - Documents with your feedback entries

## Troubleshooting

### Connection Failed Error

**Problem**: `MongoDB connection failed`

**Solutions**:
1. Check your connection string is correct
2. Verify username and password are correct (no special characters need URL encoding)
3. Check Network Access - ensure your IP is allowed (or 0.0.0.0/0 for anywhere)
4. Verify the cluster is running (not paused)

### Authentication Failed

**Problem**: `Authentication failed`

**Solutions**:
1. Double-check username and password in connection string
2. Ensure the database user has proper permissions
3. Try creating a new database user

### Connection Timeout

**Problem**: Connection times out

**Solutions**:
1. Check your internet connection
2. Verify Network Access settings in MongoDB Atlas
3. For Render: Make sure you added 0.0.0.0/0 to Network Access

### Special Characters in Password

If your password has special characters, you need to URL-encode them:
- `@` becomes `%40`
- `#` becomes `%23`
- `$` becomes `%24`
- `%` becomes `%25`
- etc.

Or better: Use MongoDB's autogenerated password which avoids special characters.

## Security Best Practices

1. **Don't commit `.env` file** - It's already in `.gitignore`
2. **Use strong passwords** - MongoDB autogenerated passwords are recommended
3. **Limit IP Access** - For production, consider restricting to Render's IP ranges
4. **Regular Backups** - MongoDB Atlas free tier includes automated backups
5. **Monitor Usage** - Check MongoDB Atlas dashboard for usage and limits

## MongoDB Atlas Free Tier Limits

- **Storage**: 512 MB
- **RAM**: Shared
- **Backup**: Automated daily backups (7-day retention)
- **Connections**: 500 concurrent connections
- **Data Transfer**: Unlimited

For this feedback system, the free tier is more than sufficient!

## Next Steps

Once MongoDB is set up:
1. Test locally with `.env` file
2. Deploy to Render
3. Add `MONGODB_URI` environment variable in Render
4. Test the deployed application

Your data will now persist across deployments! 🎉

