# pip install "fastapi[standard]"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware





"""
///To be added where needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]


@app.post("/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""