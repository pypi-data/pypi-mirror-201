from fastapi import FastAPI
from .package1 import router as package1_router


app = FastAPI()

app.include_router(package1_router.router)

@app.get("/")
async def welcome():
    return "Welcome to FastAPI app"

