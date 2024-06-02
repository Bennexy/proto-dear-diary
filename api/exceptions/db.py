import sys
sys.path.append('.')

from api.exceptions.base import DiaryServerHTTPException


class DiaryServerDBException(DiaryServerHTTPException):
    def __init__(self, message: str, detail: dict = {}, db_model=None, status_code: int = 400, exception: Exception = None) -> None:

        if 'message' not in detail.keys():
            detail['message'] = ""
        detail['message'] = message
        super().__init__(400, detail, exception)
        

class DiaryServerDBStringItemToLong(DiaryServerDBException):
    def __init__(self, message: str, detail: dict = {}, db_model=None) -> None:
        super().__init__(message, detail, db_model)