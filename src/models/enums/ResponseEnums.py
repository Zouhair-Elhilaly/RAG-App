from enum import Enum


class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED = "file not supp"
    FILE_SIZE_EXCEEDED = "FILE_SIZE_EXCEEDED"
    FILE_UPLOAD_SUCCES = "file_upload_succes"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    FILE_PROCESSING_FAILED = "file_processing_failed"