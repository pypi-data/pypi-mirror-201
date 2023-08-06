
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Dict, Union
from uuid import UUID

from pydantic import BaseModel


class ImageLink(BaseModel):
    id: str
    url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    alt: Optional[str] = None
    contentType: Optional[str] = None


class MetadataItem(BaseModel):
    type: str
    value: Union[str, float]
    id: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    label: Optional[str] = None
    wkt: Optional[str] = None
    options: Optional[Dict[str, Union[str, float, bool]]] = None


class Metadata(BaseModel):
    origin: str
    data: List[MetadataItem]


class Accuracy(str, Enum):
    UNKNOWN = "UNKNOWN"
    CONFIRMED = "CONFIRMED"
    PROBABLY_TRUE = "PROBABLY_TRUE"
    POSSIBLY_TRUE = "POSSIBLY_TRUE"
    DOUBTFUL = "DOUBTFUL"
    IMPROBABLE = "IMPROBABLE"
    TRUTH_CANNOT_BE_JUDGED = "TRUTH_CANNOT_BE_JUDGED"


class DisinfoType(str, Enum):
    UNKNOWN = "UNKNOWN"
    DISMISS = "DISMISS"
    DISTORT = "DISTORT"
    DISTRACt = "DISTRACt"
    DISMAY = "DISMAY"
    DIVIDE = "DIVIDE"


class Article(BaseModel):
    id: str
    feedId: str
    sourceId: str
    title: Optional[str] = None
    type: str
    url: str
    text: str = ""
    summary: Optional[str] = None
    language: str = "xx"
    original: Optional[str] = None
    originalLanguage: Optional[str] = None
    images: Optional[List[ImageLink]] = None
    metadata: Optional[List[Metadata]] = None
    credMan: bool = False
    cred: Optional[float] = None
    affiliation: Optional[str] = None
    target: Optional[str] = None
    storyId: Optional[str] = None
    storyCount: Optional[int] = None
    languageFlags: Optional[float] = None
    anger: Optional[float] = None
    disgust: Optional[float] = None
    fear: Optional[float] = None
    joy: Optional[float] = None
    neutral: Optional[float] = None
    readability: Optional[float] = None
    sadness: Optional[float] = None
    surprise: Optional[float] = None
    polarisation: Optional[float] = None
    sarcasm: Optional[float] = None
    accuracy: Accuracy = "UNKNOWN"
    disinfoType: DisinfoType = "UNKNOWN"
    commentsCount: Optional[int] = None
    likesCount: Optional[int] = None
    dislikesCount: Optional[int] = None
    viewsCount: Optional[int] = None
    sharesCount: Optional[int] = None
    version: int = 1
    pub_date: Optional[int] = None
    created: int
    updated: int


main_class = Article
