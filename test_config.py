#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Print relevant environment variables (first 50 chars)
print("Environment variables:")
for key in ['DATABASE_URL', 'REDIS_URL', 'SECRET_KEY', 'JWT_SECRET_KEY', 'ALGORITHM', 'ACCESS_TOKEN_EXPIRE_MINUTES']:
    value = os.environ.get(key, 'NOT SET')
    if 'KEY' in key or 'SECRET' in key:
        print(f"  {key}: {value[:20]}..." if len(value) > 20 else f"  {key}: {value}")
    else:
        print(f"  {key}: {value}")

# Now try to import and test the settings
sys.path.insert(0, '/home/theca/hermes-agent/refugee-crisis-prediction/backend')
try:
    from app.core.config import settings
    print("\nSettings loaded successfully!")
    print(f"Environment: {settings.env}")
    print(f"Database URL: {settings.database_url}")
    print(f"JWT Algorithm: {settings.jwt_algorithm}")
except Exception as e:
    print(f"\nError loading settings: {e}")
    import traceback
    traceback.print_exc()