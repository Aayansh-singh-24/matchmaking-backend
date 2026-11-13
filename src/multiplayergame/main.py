from fastapi import FastAPI

app = FastAPI(title="Authorized-server")

@app.get("/")
def home():
    return("Home page  of authorized-server")