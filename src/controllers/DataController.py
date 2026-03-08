from BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal


class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576  # 1 MB in bytes  
    
    def validate_upload_file(self, file : UploadFile):
        # Check if the file extension is allowed
        if file.content_type not in self.app_setting.FILE_ALLOWED_TYPES:
            return False  , ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value   
        # Check if the file size is within the limit
        if file.size > self.app_setting.FILE_MAX_SIZE * self.size_scale:
            return False , ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        # Process the file (e.g., save it to disk, database, etc.)
        # For demonstration, we will just return a success message
        return True , ResponseSignal.FILE_UPLOAD_SUCCES.value
