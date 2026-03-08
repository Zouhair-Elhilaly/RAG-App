from fastapi import FastAPI, UploadFile , APIRouter , Depends
from helpers.config import get_settings , Settings
from controllers import DataController


data = APIRouter()

@data.post("/upload/{prject_id}")
async def upload_data(prject_id : str , file : UploadFile):
        
            is_valid , msg = DataController.validate_file(file)
            
            return is_valid , msg