from app.services.user_service import register_user, login_user

# --- REGISTER USER ---
success, msg = register_user("alice", "SecurePass123!", "analyst")
print(msg)

# --- LOGIN USER ---
success, msg = login_user("alice", "SecurePass123!")
print(msg)
