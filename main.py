from fastapi import FastAPI

# Create an instance of FastAPI
app = FastAPI()

# Define a route using a decorator, the endpoint's path will be '/'
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Run the FastAPI application with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
