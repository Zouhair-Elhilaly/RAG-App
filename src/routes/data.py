from fastapi import FastAPI, UploadFile , APIRouter , Depends , status
from fastapi.responses import JSONResponse
from helpers.config import get_settings , Settings
from controllers import DataController , ProjectController , ProcessController
import os
import aiofiles 
from models import ResponseSignal
import logging
from routes.schemes.data import ProcessRequest


logger = logging.getLogger('uvicorn.error')

data = APIRouter()

@data.post("/upload/{project_id}")
async def upload_data(project_id : str , file : UploadFile , app_settings : Settings = Depends(get_settings)):
            
            data_controller = DataController()
            is_valid , msg = data_controller.validate_upload_file(file)
            
            if not is_valid :
              return JSONResponse(content={"message": msg} , status_code=status.HTTP_400_BAD_REQUEST)
            
            project_dir = ProjectController().get_project_path(project_id)

            file_path , file_id = data_controller.generate_unique_filepath(file.filename , project_id)

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
            
            return JSONResponse(content={"message": ResponseSignal.FILE_UPLOAD_SUCCES.value , "file_id" : file_id} , status_code=status.HTTP_200_OK)


@data.post("/process/{project_id}")
async def process_endpoint(project_id : str , process_request : ProcessRequest , app_settings : Settings = Depends(get_settings)):
         file_id = process_request.file_id
         chunk_size = process_request.chunk_size
         overlap_size = process_request.overlap_size
         process_controller = ProcessController(project_id=project_id)

         file_content = process_controller.get_file_content(file_id)
         file_chunk = process_controller.process_file_content(file_content=file_content , file_id=file_id , chunk_size=chunk_size , overlap_size=overlap_size)

         if file_chunk is None or len(file_chunk) == 0:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.FILE_PROCESSING_FAILED.value
                }
            )

         return file_chunk , 