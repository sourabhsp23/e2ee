# 🛡️ End-to-End Encrypted Chat App (FastAPI + RSA + AES)

## 📌 Overview
This project is a **secure real-time chat application** that ensures privacy using **End-to-End Encryption (E2EE)**.  
It uses **RSA for key exchange** and **AES for message encryption**, ensuring only the intended recipient can decrypt messages.

## 🚀 Tech Stack
- **Backend**: FastAPI, Python  
- **Encryption**: RSA (Public-Private Key System), AES (Message Encryption)  
- **Real-Time Messaging**: WebSockets  
- **Database**: SQLite (via Tortoise ORM)  

---
##🔐 Features
- ✅ User Registration & Authentication (JWT-based)
- ✅ RSA Key Generation & Exchange (Public-Private Key System)
- ✅ AES Encryption for Messages (Secure Content Encryption)
- ✅ RSA Encryption for AES Key (Secure Key Exchange)
- ✅ REST API for Sending & Receiving Messages
- ✅ Real-Time Encrypted Messaging (WebSockets)

## 🛠️ Setup & Installation

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-username/encrypted-chat.git
```

### install dependencies
```sh
pip install -r requirements.txt 
```


### start the server
```sh
uvicorn main:app
```








