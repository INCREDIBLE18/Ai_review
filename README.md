# AI Feedback System - Two-Dashboard Application

🌟 **Live demo & dashboards linked below!** 🌟

## Live Demo

- **User Dashboard:** [https://ai-feedback-system-lavl.onrender.com/](https://ai-feedback-system-lavl.onrender.com/)
- **Admin Dashboard:** [https://ai-feedback-system-lavl.onrender.com/admin](https://ai-feedback-system-lavl.onrender.com/admin)

## Features

### User Dashboard (Public-Facing)
- ⭐ Interactive star rating system (1-5 stars)
- 📝 Review submission form
- 🤖 AI-generated personalized responses
- ✨ Modern, responsive UI

### Admin Dashboard (Internal-Facing)
- 📊 Real-time analytics and statistics
- 📈 Rating distribution visualization
- 📋 Live-updating list of all submissions
- 🤖 AI-generated summaries for each review
- 💡 AI-suggested recommended actions
- 🔄 Auto-refresh every 5 seconds

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI/LLM**: Google Gemini API (gemini-2.5-flash)
- **Data Storage**: MongoDB Atlas (cloud database) with JSON fallback
- **Deployment**: Render (configured), also compatible with Heroku, Railway, etc.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the root directory:

```
GEMINI_API_KEY=your_gemini_api_key_here
MONGODB_URI=your_mongodb_connection_string
```

**To get a Gemini API key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy it to your `.env` file

**To get MongoDB connection string:**
1. Visit [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register) and create a Free M0 cluster
2. Create a user and database
3. Allow Network Access from anywhere (0.0.0.0/0)
4. Copy the connection string from the Atlas UI
5. Full steps: See your MongoDB dashboard for details

### 3. Run the Application

```bash
python app.py
```

The application will be available at:
- **User Dashboard**: http://localhost:5000/
- **Admin Dashboard**: http://localhost:5000/admin

## Project Structure

```
AI_feedback_system/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── .gitignore           # Git ignore file
├── README.md            # This file
├── static/
│   ├── user_dashboard.html    # User-facing dashboard
│   └── admin_dashboard.html   # Admin dashboard
└── feedback_data.json   # Data storage (auto-created)
```

## API Endpoints

### POST `/api/submit`
Submit feedback from user dashboard.

**Request Body:**
```json
{
  "rating": 5,
  "review": "Great service!"
}
```

**Response:**
```json
{
  "success": true,
  "ai_response": "Thank you for your positive feedback!",
  "id": "20240101120000000000"
}
```

### GET `/api/feedback`
Get all feedback entries for admin dashboard.

**Response:**
```json
{
  "feedback": [
    {
      "id": "20240101120000000000",
      "timestamp": "2024-01-01T12:00:00",
      "rating": 5,
      "review": "Great service!",
      "ai_response": "...",
      "summary": "...",
      "recommended_action": "..."
    }
  ]
}
```

### GET `/api/stats`
Get analytics statistics.

**Response:**
```json
{
  "total": 10,
  "average_rating": 4.2,
  "rating_distribution": {
    "1": 0,
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4
  },
  "total_reviews": 10
}
```

## Deployment

### Option 1: Render

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app:app`
6. Add environment variables:
   - `GEMINI_API_KEY=your_key`
   - `MONGODB_URI=your_connection_string`
7. Deploy!

### Other Options
- Heroku, Railway, HuggingFace Spaces (see their docs)

## Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required for AI features)
- `MONGODB_URI`: Your MongoDB Atlas connection string (cloud database)

## Notes

- ✅ **MongoDB Atlas** is now the primary data storage (persistent, cloud-hosted)
- The application falls back to JSON file storage if MongoDB is not configured
- Auto-refresh on admin dashboard is set to 5 seconds. Adjust in `admin_dashboard.html` if needed
- The application gracefully handles missing API keys (falls back to default responses)
- For deployment, MongoDB Atlas ensures data persists across deployments

## Submission Links

- GitHub Repo: https://github.com/INCREDIBLE18/Ai_review
- User Dashboard: https://ai-feedback-system-lavl.onrender.com/
- Admin Dashboard: https://ai-feedback-system-lavl.onrender.com/admin

## License

This project is created for the Fynd AI Intern Take Home Assessment.

