from dataclasses import (
    dataclass,
    field,
)
from ..main import _base


@dataclass
class ApiPagination(_base.AlphaDataclass):
    total: int = None
    total_pages: int = None
    page: int = None
    previous_page: int = None
    next_page: int = None
    per_page: int = None


@dataclass
class ApiAnswer(_base.AlphaDataclass):
    token_status: str = "success"
    status: str = "success"
    error: int = 0
    warning: int = 0
    status_code: int = 200
    status_description: str = ""
    requester: str = "unknow"
    data: dict = field(default_factory=lambda: {})
    pagination: ApiPagination = field(default_factory=lambda: {})

    def to_json(self):
        return self.get_fields_dict()
