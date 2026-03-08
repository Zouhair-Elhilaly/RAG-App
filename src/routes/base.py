from fastapi import FastAPI , APIRouter , Depends
from helpers.config import get_settings , Settings

router = APIRouter()
@router.get("/")
def welcome_message(app_setting : Settings = Depends(get_settings)):
    # app_setting = get_settings()
    app_name = app_setting.APP_NAME
    app_version = app_setting.APP_VERSION
    app_description = app_setting.APP_DESCRIPTION
    return {"app_name": app_name, "app_description": app_description
            ,"app vers": app_version}