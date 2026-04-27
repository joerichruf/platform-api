# main.py
from fastapi import FastAPI

app = FastAPI(title="Platform API", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/services/{name}/status")
def service_status(name: str):
    # we'll wire this to real k8s later
    return {"service": name, "status": "unknown"}