import jwt
from datetime import datetime, timedelta, timezone

SECRET = "CHANGE-ME-IN-PRODUCTION"
ALGO = "HS256"

# Create token like the app does
payload = {"sub": "0d62b1ff-590e-40e3-ba4f-63d3cfc7e720", "exp": datetime.now(timezone.utc) + timedelta(minutes=15), "type": "access"}
token = jwt.encode(payload, SECRET, algorithm=ALGO)

print(f"Token: {token}")

# Try to decode like the app does in the first block
try:
    decoded = jwt.decode(token, SECRET, algorithms=[ALGO])
    print(f"First decode success: {decoded}")
except Exception as e:
    print(f"First decode failed: {type(e).__name__}: {e}")

# Try to decode with an audience like the app does in the second block
# (This simulates what happens when it falls back to Supabase logic)
try:
    decoded = jwt.decode(token, SECRET, algorithms=[ALGO], audience="authenticated")
    print(f"Second decode success: {decoded}")
except Exception as e:
    print(f"Second decode failed: {type(e).__name__}: {e}")
