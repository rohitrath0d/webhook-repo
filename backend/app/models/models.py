from pydantic import BaseModel, validator
from enum import Enum
from typing import Optional
from datetime import datetime

class ActionEnum(str, Enum):
    PUSH = "PUSH"
    PULL_REQUEST = "PULL_REQUEST"
    MERGE = "MERGE"

class GitHubEvent(BaseModel):
    request_id: str
    author: str
    action: ActionEnum
    from_branch: Optional[str] = None
    to_branch: str
    timestamp: str

    @validator("timestamp")
    def validate_timestamp(cls, v):
        # ensure ISO formatted string
        try:
            datetime.fromisoformat(v.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("timestamp must be ISO formatted UTC string")
        return v
