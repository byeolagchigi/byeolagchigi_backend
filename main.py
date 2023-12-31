from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from Module import DataBase, GetTime

app = FastAPI()

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RainData:
    data = {}

class Rain(BaseModel):
    rain: int
    
class User(BaseModel):
    username: str
    password: str

users_db = {}

# DB 코드 추가
host = '192.168.38.122'
user = 'admin'
password = 'happy1003!'
db = 'Hackathon'
data = DataBase(host, user, password, db)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/rains")
def receive_rain(data: Rain):
    if data.rain is not None:
        RainData.data = {"rain": data.rain}
        return {"message": "Rain data received"}
    else:
        raise HTTPException(status_code=400, detail="rain field is missing")

@app.get("/show_rain")
def show_rain():
    if "rain" in RainData.data:
        return RainData.data
    else:
        return {"message": "Rain data not available"}


@app.post("/login")
async def login(user: User):
    stored_password = users_db.get(user.username)
    if stored_password is None or stored_password != user.password:
        return {"message": "Invalid credentials"}
    return {"username": user.username, "message": "Login successful"}

@app.post("/signup")
async def signup(user: User):
    if user.username in users_db:
        return {"message": "Username already exists"}
    
    users_db[user.username] = user.password
    return {"Sign up successful"}

@app.get("/get_time")
async def get_time():
    time = GetTime().sendtime()
    print(type(time))

    return {time}
