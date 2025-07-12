import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    
    def __init__(self, error_message, error_detail:sys):
        self.error_message = error_message
        _,_, exc_tb = error_detail.exc_info()
        
        self.line_no = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename
        
    def __str__(self):
        return f"Error occurred in script: [{self.file_name}] at line number: [{self.line_no}] with message: [{self.error_message}]"