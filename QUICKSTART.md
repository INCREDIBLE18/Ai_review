# Quick Start Guide

Get the AI Feedback System up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

## Step 3: Create .env File

Create a file named `.env` in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with the key you copied in Step 2.

## Step 4: Run the Application

```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

## Step 5: Access the Dashboards

Open your browser and visit:

- **User Dashboard**: http://localhost:5000/
- **Admin Dashboard**: http://localhost:5000/admin

## Step 6: Test It Out

1. Go to the User Dashboard
2. Select a star rating (1-5)
3. Write a review
4. Click "Submit Feedback"
5. See the AI-generated response!

6. Open the Admin Dashboard in another tab
7. See your submission appear with:
   - AI-generated summary
   - Recommended action
   - Analytics

## Troubleshooting

### "Module not found" error
Run: `pip install -r requirements.txt`

### "GEMINI_API_KEY not set" warning
- Make sure you created the `.env` file
- Check the file is in the project root
- Verify the key is correct (no extra spaces)

### Port already in use
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

## Next Steps

- Deploy to production (see DEPLOYMENT.md)
- Customize the UI (edit HTML files in `static/`)
- Adjust AI prompts (edit functions in `app.py`)

## Need Help?

Check the full README.md for detailed documentation.

