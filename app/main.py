from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
import os
from hashlib import sha256

app = FastAPI()

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(mongo_uri)
db = client["chat_app"]
users_collection = db["users"]
# Templates and static objects
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/mongo-test")
async def mongo_test():
    try:
        await db.command("ping")
        return {"status": "connected"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/login")
async def post_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    hashed_input = sha256(password.encode()).hexdigest()
    user = await users_collection.find_one({"username": username})
    
    if user and user["password"] == hashed_input:
        return RedirectResponse(url=f"/chat?username={username}", status_code=303)
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Wrong username or password."
        })

@app.post("/signup")
async def post_signup(
    request: Request,
    new_username: str = Form(...),
    new_password: str = Form(...)
):
    user = await users_collection.find_one({"username": new_username})
    if user:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "signup_error": "This username has taken."
        })
    
    hashed_password = sha256(new_password.encode()).hexdigest()
    await users_collection.insert_one({
        "username": new_username,
        "password": hashed_password
    })
    return RedirectResponse(url="/login", status_code=303)

