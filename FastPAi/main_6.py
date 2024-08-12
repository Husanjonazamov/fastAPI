from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get('/')
async def root():
    return {'Hello': 'World'}



