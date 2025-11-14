import bcrypt

def hash_password(plain_txt_pass):
    # Encode password to bytes
    Bytes_pass = plain_txt_pass.encode('utf-8')
    # Generate a salt and hash the password
    Salt = bcrypt.gensalt()
    Hash_pass = bcrypt.hashpw(Bytes_pass,Salt)
    # Decode the hash back to a string 
    return Hash_pass.decode('utf-8')

def verify(plain_txt_pass,hashed_password):
    # Encode both password and stored hash to bytes
    bytes_pass = plain_txt_pass.encode('utf-8')
    bytes_h = hashed_password.encode('utf-8')
    # Bcrypt will compare it with stored hash
    return bcrypt.checkpw(bytes_pass,bytes_h)

# Test Code
test_password = 'SecurePassword123'

# Test hashing
hashed = hash_password(test_password)
print(f"Original password: {test_password}")
print(f"Hashed password: {hashed}")
print(f"Hash length: {len(hashed)} characters")

# Test verification with correct password
is_valid = verify(test_password, hashed)
print(f"\nVerification with correct password: {is_valid}")

# Test verification with incorrect password
is_invalid = verify("WrongPassword", hashed)
print(f"Verification with incorrect password: {is_invalid}")
