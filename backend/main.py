from fastapi import FastAPI
from backend.routes import upload, receipts

app = FastAPI(title="Receipt Analyzer")

# Register routes
app.include_router(upload.router)
app.include_router(receipts.router)

@app.get("/")
def home():
    return {"message": "Receipt Analyzer API is running!"}
