from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .generator import generate_images
from .cache import store_selection

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/generate")
def generate():
    images = generate_images()
    return JSONResponse(content={"images": images})

@app.post("/select")
async def select(request: Request):
    data = await request.json()
    selected_id = data.get("selected_id")
    store_selection(selected_id)
    return {"status": "cached"}