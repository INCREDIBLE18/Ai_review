# Pre-Deployment Checklist

Use this checklist to ensure everything is ready before deployment.

## Setup Checklist

- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with `GEMINI_API_KEY`
- [ ] Tested locally (`python app.py`)
- [ ] User dashboard accessible at http://localhost:5000/
- [ ] Admin dashboard accessible at http://localhost:5000/admin
- [ ] Submitted test feedback from user dashboard
- [ ] Verified feedback appears in admin dashboard
- [ ] Confirmed AI responses are generated
- [ ] Confirmed AI summaries are generated
- [ ] Confirmed recommended actions are generated
- [ ] Verified analytics are updating

## Code Checklist

- [ ] All files committed to Git
- [ ] `.env` file is in `.gitignore` (not committed)
- [ ] `feedback_data.json` is in `.gitignore` (not committed)
- [ ] No hardcoded API keys in code
- [ ] No sensitive data in code

## Deployment Checklist

- [ ] Repository pushed to GitHub
- [ ] Deployment platform account created
- [ ] Environment variable `GEMINI_API_KEY` set on deployment platform
- [ ] Build command configured: `pip install -r requirements.txt`
- [ ] Start command configured: `gunicorn app:app`
- [ ] Deployment successful
- [ ] User dashboard URL working
- [ ] Admin dashboard URL working
- [ ] Tested submission from deployed user dashboard
- [ ] Verified data persistence on deployed platform

## Documentation Checklist

- [ ] README.md reviewed
- [ ] QUICKSTART.md reviewed
- [ ] DEPLOYMENT.md reviewed
- [ ] All URLs documented
- [ ] API endpoints documented

## Final Verification

- [ ] Both dashboards are publicly accessible
- [ ] All features working on deployed version
- [ ] Mobile responsive design verified
- [ ] Error handling works correctly
- [ ] Ready for submission!

## Submission Format

When ready to submit, provide:

```
GitHub Repository: [your-repo-url]
User Dashboard URL: [your-deployed-url]/
Admin Dashboard URL: [your-deployed-url]/admin
```

