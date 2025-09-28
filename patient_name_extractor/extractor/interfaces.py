from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


class NeedsOcrCase(str, Enum):
    NO_OCR: str = "no_ocr"
    OCR: str = "ocr"
    # fill in with other values if necessary


class BoundingBox(BaseModel):
    x_min: float = Field(ge=0.0, le=1.0)
    x_max: float = Field(ge=0.0, le=1.0)
    y_min: float = Field(ge=0.0, le=1.0)
    y_max: float = Field(ge=0.0, le=1.0)


class Word(BaseModel):
    text: str
    bbox: BoundingBox


class Page(BaseModel):
    words: list[Word]


class Document(BaseModel):
    pages: list[Page]
    original_page_count: Optional[int]
    needs_ocr_case: Optional[NeedsOcrCase]


class Gender(str, Enum):
    MALE: str = "male"
    FEMALE: str = "female"


class Patient(BaseModel):
    gender: Gender
    first_name: str
    last_name: str
