"""
Script to verify data is stored in MongoDB
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI', '')

if not MONGODB_URI:
    print("[ERROR] MONGODB_URI not found in .env file")
    exit(1)

try:
    print("Connecting to MongoDB...")
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    
    # Test connection
    client.admin.command('ping')
    print("[OK] Connected to MongoDB successfully!\n")
    
    # Get database and collection
    db = client['feedback_db']
    collection = db['feedback']
    
    # Count documents
    count = collection.count_documents({})
    print(f"Total feedback entries in MongoDB: {count}\n")
    
    if count > 0:
        print("Recent feedback entries:")
        print("-" * 80)
        
        # Get all documents, sorted by timestamp (newest first)
        cursor = collection.find({}).sort('timestamp', -1).limit(10)
        
        for i, doc in enumerate(cursor, 1):
            print(f"\n[{i}] Entry ID: {doc.get('_id')}")
            print(f"    Timestamp: {doc.get('timestamp', 'N/A')}")
            print(f"    Rating: {doc.get('rating', 'N/A')} stars")
            print(f"    Review: {doc.get('review', 'N/A')[:50]}...")
            print(f"    Summary: {doc.get('summary', 'N/A')[:50]}...")
            print("-" * 80)
    else:
        print("[INFO] No feedback entries found in MongoDB yet.")
        print("       Submit some feedback from the user dashboard first!")
    
    # Show database info
    print(f"\nDatabase: feedback_db")
    print(f"Collection: feedback")
    print(f"Total documents: {count}")
    
    client.close()
    print("\n[OK] Verification complete!")
    
except Exception as e:
    print(f"[ERROR] Failed to connect or query MongoDB: {e}")
    print("\nTroubleshooting:")
    print("1. Check if MONGODB_URI is correct in .env file")
    print("2. Verify MongoDB Atlas Network Access allows your IP")
    print("3. Check if the cluster is running (not paused)")

