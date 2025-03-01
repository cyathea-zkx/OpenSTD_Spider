from dataclasses import dataclass
from datetime import date
from enum import Enum


@dataclass
class Gb688Block:
    x: int
    y: int
    img_x: int
    img_y: int


@dataclass
class Gb688Page:
    no: int
    img_id: str
    h: int
    w: int
    blocks: list[Gb688Block]


class StdStatus(Enum):
    ALL = ""
    PUBLISHED = "PUBLISHED"
    TOBEIMP = "TOBEIMP"
    WITHDRAWN = "WITHDRAWN"


class StdType(Enum):
    ALL = 0
    GB = 1
    GBT = 2
    GBZ = 3


@dataclass
class StdMeta:
    std_code: str
    is_ref: bool
    name_cn: str
    name_en: str
    status: StdStatus
    allow_preview: bool
    allow_download: bool
    pub_date: date
    impl_date: date
    ccs: str
    ics: str
    maintenance_depat: str
    centralized_depat: str
    pub_depat: str
    comment: str


@dataclass
class StdListItem:
    id: str
    std_code: str
    is_ref: bool
    name_cn: str
    status: StdStatus
    pub_date: date
    impl_date: date


@dataclass
class StdSearchResult:
    items: list[StdListItem]
    total_item: int
    page: int
    total_page: int
