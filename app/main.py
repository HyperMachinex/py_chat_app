from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Templates and static objects
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Temp db for test
users_db = {}

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def post_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    user_password = users_db.get(username)
    if user_password and user_password == password:
        # Log in successfull forward chat page
        response = templates.TemplateResponse("index.html", {"request": request, "username": username})
        return response
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Kullanıcı adı veya şifre hatalı."
        })

@app.post("/signup")
async def post_signup(
    request: Request,
    new_username: str = Form(...),
    new_password: str = Form(...)
):
    if new_username in users_db:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "signup_error": "Bu kullanıcı adı zaten kayıtlı."
        })
    
    users_db[new_username] = new_password
    return RedirectResponse(url="/login", status_code=303)

