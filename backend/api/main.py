from fastapi import FastAPI

app = FastAPI(title="Disease Outbreak Reporting System", version="0.1.0")


@app.get("/")
def read_root():
    return {"message": "Hello World!"}
