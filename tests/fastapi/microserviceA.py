from fastapi import FastAPI

# Create an instance of FastAPI
app = FastAPI()

# Define a root path route
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

# Define a path with a dynamic parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}