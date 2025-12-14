from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId

load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        # Use gemini-2.5-flash for fast, free-tier friendly responses
        # Alternatives: 'gemini-2.5-pro', 'gemini-flash-latest', 'gemini-pro-latest'
        model = genai.GenerativeModel('gemini-2.5-flash')
        print("[OK] Gemini API configured successfully with gemini-2.5-flash")
    except Exception as e:
        print(f"ERROR configuring Gemini API: {e}")
        model = None
else:
    model = None
    print("[WARNING] GEMINI_API_KEY not set. LLM features will be disabled.")

# Configure MongoDB
MONGODB_URI = os.getenv('MONGODB_URI', '')
collection = None
if MONGODB_URI:
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        # Test connection
        client.admin.command('ping')
        db = client['feedback_db']
        collection = db['feedback']
        print("[OK] MongoDB connected successfully")
    except Exception as e:
        print(f"[WARNING] MongoDB connection failed: {e}")
        print("   Falling back to JSON file storage")
        collection = None
else:
    print("[WARNING] MONGODB_URI not set. Using JSON file storage.")

# Fallback to JSON if MongoDB not available
DATA_FILE = 'feedback_data.json'

def load_data():
    """Load feedback data from MongoDB or JSON fallback"""
    if collection is not None:
        try:
            # Get all documents and convert ObjectId to string
            cursor = collection.find({}).sort('timestamp', -1)
            data = []
            for doc in cursor:
                doc_dict = dict(doc)
                # Convert ObjectId to string for JSON serialization
                if '_id' in doc_dict:
                    doc_dict['id'] = str(doc_dict.pop('_id'))
                data.append(doc_dict)
            return data
        except Exception as e:
            print(f"Error loading from MongoDB: {e}")
            # Fallback to JSON
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
    else:
        # JSON fallback
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

def save_feedback(feedback_entry):
    """Save a single feedback entry to MongoDB or JSON fallback"""
    if collection is not None:
        try:
            # Convert string id to ObjectId if it exists, otherwise let MongoDB create one
            entry_copy = feedback_entry.copy()
            if 'id' in entry_copy:
                try:
                    # Try to use existing ObjectId if it's a valid ObjectId string
                    entry_copy['_id'] = ObjectId(entry_copy.pop('id'))
                except:
                    # If not a valid ObjectId, remove id and let MongoDB create _id
                    entry_copy.pop('id', None)
            # Insert the document
            result = collection.insert_one(entry_copy)
            print(f"[OK] Feedback saved to MongoDB with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error saving to MongoDB: {e}, falling back to JSON")
            # Fallback to JSON
            all_data = load_data()
            all_data.append(feedback_entry)
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=2, ensure_ascii=False)
            return feedback_entry.get('id', '')
    else:
        # JSON fallback
        all_data = load_data()
        all_data.append(feedback_entry)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        return feedback_entry.get('id', '')

def generate_ai_response(rating, review):
    """Generate AI response for user submission"""
    if not model:
        print("ERROR: Gemini model not initialized. Check GEMINI_API_KEY in .env file")
        return "Thank you for your feedback! We appreciate your input."
    
    prompt = f"""You are a friendly customer service representative. A customer has submitted a review with a {rating}-star rating.

Review: "{review}"

Generate a brief, warm, and professional response (2-3 sentences) that:
- Acknowledges their feedback
- Shows appreciation for their input
- If rating is 3 or below, expresses commitment to improvement
- If rating is 4 or 5, thanks them for their positive feedback

Response:"""
    
    try:
        response = model.generate_content(prompt)
        # Handle different response formats
        if hasattr(response, 'text'):
            result = response.text.strip()
        elif hasattr(response, 'candidates') and response.candidates:
            result = response.candidates[0].content.parts[0].text.strip()
        else:
            result = str(response).strip()
        
        if result and len(result) > 10:  # Ensure we got a real response
            print(f"[OK] AI Response generated successfully ({len(result)} chars)")
            return result
        else:
            print("WARNING: Empty or too short response from AI, using fallback")
            return "Thank you for your feedback! We appreciate your input."
    except Exception as e:
        print(f"ERROR generating AI response: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return "Thank you for your feedback! We appreciate your input."

def generate_summary(review):
    """Generate AI summary of the review"""
    if not model:
        print("ERROR: Gemini model not initialized for summary generation")
        return review[:100] + "..." if len(review) > 100 else review
    
    prompt = f"""Summarize the following customer review in one concise sentence (max 50 words):

Review: "{review}"

Summary:"""
    
    try:
        response = model.generate_content(prompt)
        # Handle different response formats
        if hasattr(response, 'text'):
            result = response.text.strip()
        elif hasattr(response, 'candidates') and response.candidates:
            result = response.candidates[0].content.parts[0].text.strip()
        else:
            result = str(response).strip()
        
        if result and len(result) > 5:  # Ensure we got a real summary
            print(f"[OK] AI Summary generated successfully")
            return result
        else:
            print("WARNING: Empty summary from AI, using fallback")
            return review[:100] + "..." if len(review) > 100 else review
    except Exception as e:
        print(f"ERROR generating summary: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return review[:100] + "..." if len(review) > 100 else review

def generate_recommended_action(rating, review):
    """Generate AI-suggested recommended action"""
    if not model:
        print("ERROR: Gemini model not initialized for action generation")
        if rating <= 2:
            return "Follow up with customer to address concerns"
        elif rating == 3:
            return "Review feedback for improvement opportunities"
        else:
            return "Thank customer and consider featuring positive feedback"
    
    prompt = f"""A customer has given a {rating}-star rating with the following review:

Review: "{review}"

Based on this feedback, suggest ONE specific, actionable next step for the business (one sentence, max 30 words). Be practical and specific.

Recommended Action:"""
    
    try:
        response = model.generate_content(prompt)
        # Handle different response formats
        if hasattr(response, 'text'):
            result = response.text.strip()
        elif hasattr(response, 'candidates') and response.candidates:
            result = response.candidates[0].content.parts[0].text.strip()
        else:
            result = str(response).strip()
        
        if result and len(result) > 10:  # Ensure we got a real action
            print(f"[OK] AI Recommended Action generated successfully")
            return result
        else:
            print("WARNING: Empty action from AI, using fallback")
            if rating <= 2:
                return "Follow up with customer to address concerns"
            elif rating == 3:
                return "Review feedback for improvement opportunities"
            else:
                return "Thank customer and consider featuring positive feedback"
    except Exception as e:
        print(f"ERROR generating recommended action: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        if rating <= 2:
            return "Follow up with customer to address concerns"
        elif rating == 3:
            return "Review feedback for improvement opportunities"
        else:
            return "Thank customer and consider featuring positive feedback"

@app.route('/')
def index():
    """Serve user dashboard"""
    return send_from_directory('static', 'user_dashboard.html')

@app.route('/admin')
def admin():
    """Serve admin dashboard"""
    return send_from_directory('static', 'admin_dashboard.html')

@app.route('/api/submit', methods=['POST'])
def submit_feedback():
    """Handle feedback submission from user dashboard"""
    try:
        data = request.json
        rating = int(data.get('rating', 0))
        review = data.get('review', '').strip()
        
        if not review or rating < 1 or rating > 5:
            return jsonify({'error': 'Invalid rating or review'}), 400
        
        # Generate AI response
        ai_response = generate_ai_response(rating, review)
        
        # Generate summary and recommended action
        summary = generate_summary(review)
        recommended_action = generate_recommended_action(rating, review)
        
        # Create feedback entry
        feedback_entry = {
            'timestamp': datetime.now().isoformat(),
            'rating': rating,
            'review': review,
            'ai_response': ai_response,
            'summary': summary,
            'recommended_action': recommended_action
        }
        
        # Save to MongoDB or JSON
        feedback_id = save_feedback(feedback_entry)
        feedback_entry['id'] = feedback_id
        
        return jsonify({
            'success': True,
            'ai_response': ai_response,
            'id': feedback_id
        })
    
    except Exception as e:
        print(f"Error submitting feedback: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback', methods=['GET'])
def get_feedback():
    """Get all feedback entries for admin dashboard"""
    try:
        data = load_data()
        # Data is already sorted by timestamp descending from MongoDB
        # For JSON, reverse it
        if collection is None:
            data = list(reversed(data))
        return jsonify({'feedback': data})
    except Exception as e:
        print(f"Error fetching feedback: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get analytics statistics for admin dashboard"""
    try:
        data = load_data()
        
        if not data:
            return jsonify({
                'total': 0,
                'average_rating': 0,
                'rating_distribution': {str(i): 0 for i in range(1, 6)},
                'total_reviews': 0
            })
        
        total = len(data)
        ratings = [entry['rating'] for entry in data]
        average_rating = sum(ratings) / total if total > 0 else 0
        
        rating_distribution = {str(i): ratings.count(i) for i in range(1, 6)}
        
        return jsonify({
            'total': total,
            'average_rating': round(average_rating, 2),
            'rating_distribution': rating_distribution,
            'total_reviews': total
        })
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize data file if using JSON fallback and file doesn't exist
    if collection is None and not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    
    # Get port from environment variable (for Render) or use default
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

