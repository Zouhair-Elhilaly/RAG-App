from fastapi import FastAPI, UploadFile , APIRouter , Depends , status
from fastapi.responses import JSONResponse
from helpers.config import get_settings , Settings
from controllers import DataController , ProjectController
import os
import aiofiles 
from models import ResponseSignal
import logging

logger = logging.getLogger('uvicorn.error')

data = APIRouter()

@data.post("/upload/{project_id}")
async def upload_data(project_id : str , file : UploadFile , app_settings : Settings = Depends(get_settings)):
            
            data_controller = DataController()
            is_valid , msg = data_controller.validate_upload_file(file)
            
            if not is_valid :
              return JSONResponse(content={"message": msg} , status_code=status.HTTP_400_BAD_REQUEST)
            
            project_dir = ProjectController().get_project_path(project_id)

            file_path , cleaned = data_controller.generate_unique_filepath(file.filename , project_id)

            # async with aiofiles.open(file_path, 'wb') as out_file:
            #     while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE) : # Read the file content
            #         await out_file.write(chunk)  # Write the content to the new file
            try:
                async with aiofiles.open(file_path, "wb") as f:
                    while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                        await f.write(chunk)
            except Exception as e:

                logger.error(f"Error while uploading file: {e}")

                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
                    }
                )
            
            return JSONResponse(content={"message": ResponseSignal.FILE_UPLOAD_SUCCES.value} , status_code=status.HTTP_200_OK)