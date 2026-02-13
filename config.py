import os

# API Keys (Reads from Environment Variables on Cloud, fallback to hardcoded locally)
LODGIFY_API_KEY = os.environ.get("LODGIFY_API_KEY", "h2y9Uq3F5BvSmrmcMrMKSGpBQGHMpZNFs0smOX2P7NhXSCZ1LRxse24muBCeSJNi")
RETELL_API_KEY = os.environ.get("RETELL_API_KEY", "key_2373d5c84a67dcb735b1a4f4074c")

# Server Settings
PORT = int(os.environ.get("PORT", 5000))

# Database URL (Render provides this automatically)
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///properties.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
