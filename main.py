from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# Sozdanie FastAPI prilozheniya
app = FastAPI(title="Restaurant Management System", description="API dlya upravleniya restoranom")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Podklyuchenie API marshrutov
from api.posts import router as posts_router
from api.users import router as users_router

app.include_router(posts_router, prefix="/api/posts", tags=["posts"])
app.include_router(users_router, prefix="/api/users", tags=["users"])

# Podklyuchenie API restorana
import restaurant_api
app.include_router(restaurant_api.api_router)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Glavnaya stranica s interfeysom upravleniya restoranom"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Fayl index.html ne nayden</h1>", status_code=404)

@app.get("/health")
async def health_check():
    """Proverka zdorov'ya API"""
    return {"status": "healthy", "message": "Restaurant API rabotayet"}
