from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from api.v1.user.login import router as loginRouter
from api.v1.user.register import router as registerRouter
from api.v1.user.token import router as tokenRouter
from api.v1.user.user import router as userRouter
from core.database import create_db_and_tables

app = FastAPI(
    title="Mplify.v2",
    description="TIHLDE Mplify API",
    version="0.0.1",
)

origins = [
    "https://localhost",
    "http://localhost",
    "http://localhost:8080",
    "https://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(userRouter)
app.include_router(tokenRouter)
# app.include_router(loginRouter)
app.include_router(registerRouter)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.on_event("shutdown")
def shutdown_event():
    print("Server stopped!")


@app.get("/")
async def read_root():
    return {"Hello": "World"}
