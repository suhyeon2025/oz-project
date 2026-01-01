from enum import Enum

from pydantic import BaseModel, conint


class GenderEnum(str, Enum):
    male = 'male'
    female = 'female'


class UserCreateRequest(BaseModel):
    username: str
    age: int
    gender: GenderEnum
    
class UserUpdateRequest(BaseModel):
    # 수정하고 싶은 것만 보낼 수 있도록 None을 허용합니다.
    username: str | None = None
    age: int | None = None

class UserSearchParams(BaseModel):
        model_config = {"extra": "forbid"} # 정해진 것 외에 다른 검색어는 금지!

        username: str | None = None
        age: conint(gt=0) | None = None # 나이는 0보다 커야 함
        gender: GenderEnum | None = None
        
# 파일 맨 밑에 추가하세요!
class UserSearchParams(BaseModel):
    model_config = {"extra": "forbid"}

    username: str | None = None
    age: int | None = None
    gender: GenderEnum | None = None