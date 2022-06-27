# imports
from fastapi import FastAPI, Request, Body
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from server.routes.person import router as PersonRouter
from fastapi.middleware.cors import CORSMiddleware

from server.models.person import UserSchema, UserLoginSchema
from server.auth.auth_bearer import JWTBearer
from server.auth.auth_handler import signJWT

user = UserSchema(fullname="admin",
                  email="admin@admin.com", password="admin")
users = [user]

IsLogged = False
# Initialize
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]    
)

"""
CORS(app, resources={r"/app/*": {"origins": "http://localhost:3000",
                                 "allow_headers": ["Origin", "Authorization", "X-Frame-Options", "X-Requested-With", "DNT", "User-Agent", "If-Modified-Since", "Cache-Control", "Range", "X-Real-IP", "HOST", "X-NginX-Proxy", "Content-Type", "If-Match"],
                                 "expose_headers": ["ETag", "Content-Length", "Content-Range", "Access-Control-Allow-Origin"],
                                 "max_age": "3600"}})
"""

# helpers


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

# route handlers


app.include_router(PersonRouter, tags=["Person"], prefix="/people")

# Static file serv
app.mount("/static", StaticFiles(directory="app/server/static"), name="static")
# Jinja2 Template directory
templates = Jinja2Templates(directory="app/server/templates")


@app.get("/login")
def read_all_people(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/")
def read_all_people(request: Request):
    if IsLogged is True:
        return templates.TemplateResponse("list_people.html", {"request": request})
    else:
        return templates.TemplateResponse("login.html", {"request": request})


@app.get("/view/{id}")
def read_person(request: Request):
    return templates.TemplateResponse("view_person.html", {"request": request})


@app.get("/createui")
async def create_person_ui(request: Request):
    return templates.TemplateResponse("new_person.html", {"request": request})


@app.get("/edit/{id}")
def edit_person(request: Request):
    return templates.TemplateResponse("edit_person.html", {"request": request})


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    # replace with db call, making sure to hash the password first
    print(user)
    users.append(user)
    print(users)
    return signJWT(user.email)


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        global IsLogged  # global variable
        IsLogged = True
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }
