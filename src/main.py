from fastapi import FastAPI 
# Load environment variables from .env file

from routes import base , data

app = FastAPI()
app.include_router(base.router)

app.include_router(data.data)
