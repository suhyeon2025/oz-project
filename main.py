from typing import Annotated  # <- Annotated는 여기서 가져와야 합니다!

from app.models.users import UserModel
from app.schemas.users import UserCreateRequest, UserSearchParams, UserUpdateRequest
from fastapi import (  # <- 여기에 HTTPException 추가!
    FastAPI,
    HTTPException,
    Path,
    Query,
)

# 1. 'app'이라는 이름으로 FastAPI 인스턴스를 만듭니다. (이게 있어야 에러가 안 나요!)
app = FastAPI()

# 2. 서버가 켜질 때 테스트용 데이터를 미리 넣습니다.
UserModel.create_dummy()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# 3. 유저 생성 API
@app.post("/users")
async def create_user(data: UserCreateRequest):
    # 입력받은 데이터를 사용하여 유저 생성
    user = UserModel.create(**data.model_dump())
    return {"id": user.id, "username": user.username}


# 4. 유저 검색 API (반드시 전체 조회보다 위에 있어야 함!)
@app.get('/users/search')
async def search_users(query_params: Annotated[UserSearchParams, Query()]):
    valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}
    filtered_users = UserModel.filter(**valid_query)
    if not filtered_users:
        raise HTTPException(status_code=404, detail="검색 결과가 없습니다.")
    return filtered_users

# 5. 모든 유저 조회 API
@app.get("/users")
async def get_all_users():
    result = UserModel.all()
    if not result:
        raise HTTPException(status_code=404, detail="유저가 존재하지 않습니다.")
    return result

@app.get("/users/{user_id}")
async def get_user(user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    return user

@app.patch("/users/{user_id}")
async def update_user(data: UserUpdateRequest, user_id: int = Path(gt=0)):
    # 1. 입력받은 ID로 유저를 찾습니다.
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    
    # 2. 유저 정보를 업데이트합니다. (값이 있는 것만!)
    user.update(**data.model_dump(exclude_none=True))
    
    # 3. 바뀐 정보를 돌려줍니다.
    return user
@app.delete("/users/{user_id}")
async def delete_user(user_id: int = Path(gt=0)):
    # 1. 삭제할 유저를 먼저 찾습니다.
    user = UserModel.get(id=user_id)
    
    # 2. 만약 유저가 없다면 에러를 던집니다.
    if user is None:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    
    # 3. 진짜로 유저를 삭제합니다.
    user.delete()
    
    # 4. 삭제 성공 메시지를 보여줍니다.
    return {'detail': f'User: {user_id}, Successfully Deleted.'}

# 이 부분은 반드시 파일의 가장 마지막에 와야 합니다!
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)