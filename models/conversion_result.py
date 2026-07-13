from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ConversionResult(BaseModel):
    success: bool
    output_path: str
    download_name: str
    content_type: str


class HistoryRecord(BaseModel):
    id: int
    source_format: str
    target_format: str
    original_file_name: Optional[str] = None
    converted_file_name: Optional[str] = None
    status: str
    error_message: Optional[str] = None
    created_by: Optional[int] = None
    created_date: datetime

    class Config:
        from_attributes = True
