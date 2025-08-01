from fastapi import FastAPI, Request, Form, Depends, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from hashlib import sha256
from app.redis_client import redis
from app.utils import create_access_token, verify_token
from app.auth import get_current_user
import os

router = APIRouter()
app = FastAPI()
# mongodb settings
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(mongo_uri)
db = client["chat_app"]
users_collection = db["users"]

# redis settings


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

@app.get("/users")
async def get_all_users():
    users = await db["users"].find({}, {"_id": 0, "username": 1}).to_list(length=100)
    usernames = [user["username"] for user in users]
    return JSONResponse(content={"users": usernames})

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# app/main.py
@app.get("/verify-token")
async def verify_token_route(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return JSONResponse(content={"valid": False})

    payload = await verify_token(token)
    if not payload:
        return JSONResponse(content={"valid": False})

    return JSONResponse(content={"valid": True, "username": payload["sub"]})

@app.get("/chat", response_class=HTMLResponse)
async def get_chat(request: Request, user: str = Depends(get_current_user)):
    return templates.TemplateResponse("chat.html", {"request": request, "username": user})


@app.get("/signup", response_class=HTMLResponse)
async def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/logout")
async def logout(request: Request):
    token = request.cookies.get("access_token")
    if token:
        await redis.delete(f"access_token:{token}")
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("access_token")
    return response


@app.post("/login")
async def post_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    user = await users_collection.find_one({"username": username})
    if user and user["password"] == sha256(password.encode()).hexdigest():
        token = await create_access_token({"sub": username})
        response = JSONResponse(content={"access_token": token, "username": username})
        response.set_cookie("access_token", token, httponly=True)
        return response

    return JSONResponse(content={"error": "Wrong username or password"}, status_code=401)


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

