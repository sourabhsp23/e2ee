from fastapi import FastAPI, WebSocket, HTTPException, Depends
from security import generate_rsa_keys, encrypt_message, decrypt_message
from models import User, Message, init_db
from tortoise.contrib.fastapi import register_tortoise
import jwt
import datetime
import os

app = FastAPI()

# Secret key for JWT authentication
SECRET_KEY = "your_secret_key"

# Initialize database
init_db(app)

# Generate RSA keys on startup
RSA_KEYS = {}

@app.on_event("startup")
async def startup_event():
    users = await User.all()
    for user in users:
        RSA_KEYS[user.username] = generate_rsa_keys()

@app.post("/register")
async def register(username: str, password: str):
    existing_user = await User.get_or_none(username=username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    user = await User.create(username=username, password=password)
    RSA_KEYS[username] = generate_rsa_keys()
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(username: str, password: str):
    user = await User.get_or_none(username=username, password=password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"sub": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, SECRET_KEY, algorithm="HS256")
    return {"token": token}

@app.post("/send_message")
async def send_message(sender: str, recipient: str, message: str):
    if recipient not in RSA_KEYS:
        raise HTTPException(status_code=404, detail="Recipient not found")

    enc_aes_key, enc_message = encrypt_message(message, RSA_KEYS[recipient]["public_key"])
    await Message.create(sender=sender, recipient=recipient, encrypted_message=enc_message, encrypted_aes_key=enc_aes_key)
    return {"message": "Message sent securely"}

@app.post("/decrypt_message")
async def decrypt_message_api(username: str):
    message_entry = await Message.filter(recipient=username).first()
    if not message_entry:
        raise HTTPException(status_code=404, detail="No messages found")

    decrypted_msg = decrypt_message(
        message_entry.encrypted_message,
        message_entry.encrypted_aes_key,
        RSA_KEYS[username]["private_key"]
    )
    return {"decrypted_message": decrypted_msg}

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            await websocket.send_text(f"Encrypted message received: {data}")
        except Exception as e:
            await websocket.close()
            break
