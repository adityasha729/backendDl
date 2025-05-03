from fastapi import APIRouter, Form, HTTPException
from db.mongo import users_collection
import bcrypt

router = APIRouter()

@router.post("/signup/")

def signup_user(username: str = Form(...), password: str = Form(...), email: str = Form(...)):
    if users_collection.find_one({"username": username}) or users_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    users_collection.insert_one({"username": username, "password": hashed_pw, "email": email})

    return {"message": "User signed up successfully"}

@router.post("/login/")

def login_user(username: str = Form(...), password: str = Form(...)):
    user = users_collection.find_one({"$or": [{"username": username}, {"email": username}]})

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": f"Welcome {user['username']}!"}
