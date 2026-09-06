import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get Firebase credentials path
credentials_path = os.getenv(
    "FIREBASE_CREDENTIALS_PATH",
    "firebase-service-account.json"
)

# Convert to absolute path relative to the backend folder
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
credentials_path = os.path.join(backend_dir, credentials_path)

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(credentials_path)

    firebase_admin.initialize_app(cred)

# Firestore database instance
db = firestore.client()