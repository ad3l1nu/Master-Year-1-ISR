import json
import pyrebase
from google.cloud import firestore
from google.oauth2 import service_account
import os

class FirebaseService:
    def __init__(self, config_path="firebase_config.json", key_path="serviceAccountKey.json"):
        # Dacă path-urile nu sunt absolute, caută-le în directorul DS_P2+P3
        if not os.path.isabs(config_path):
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(parent_dir, config_path)
        
        if not os.path.isabs(key_path):
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            key_path = os.path.join(parent_dir, key_path)
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Fișierul '{config_path}' nu a fost găsit.")
            
        with open(config_path) as f:
            config = json.load(f)

        self.pyrebase_app = pyrebase.initialize_app(config)
        self.auth = self.pyrebase_app.auth()

        try:
            creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", key_path)
            if not os.path.exists(creds_path):
                raise FileNotFoundError(f"Cheia Firestore '{key_path}' nu a fost găsită.")
            
            credentials = service_account.Credentials.from_service_account_file(creds_path)
            self.db = firestore.Client(credentials=credentials)
        except Exception as e:
            print(f"Eroare Firestore: {e}")
            self.db = None

    def sign_up(self, email, password):
        try:
            self.auth.create_user_with_email_and_password(email, password)
            return self.auth.sign_in_with_email_and_password(email, password)
        except Exception as e:
            return {"error": str(e)}

    def sign_in(self, email, password):
        try:
            return self.auth.sign_in_with_email_and_password(email, password)
        except Exception as e:
            return {"error": "Email sau parolă incorectă."}

    def save_conversation(self, user_id, conversation_history):
        if not self.db: return False
        try:
            self.db.collection('conversations').document(user_id).set({'history': conversation_history})
            return True
        except Exception:
            return False

    def load_conversation(self, user_id):
        if not self.db: return []
        try:
            doc = self.db.collection('conversations').document(user_id).get()
            return doc.to_dict().get('history', []) if doc.exists else []
        except Exception:
            return []