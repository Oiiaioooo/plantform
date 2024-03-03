from datetime import timedelta
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.users import UserInDB, Token
from utils.auth import get_current_user, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, fake_users_db, create_access_token,invalidate_token
from routers.dependencies.user_deps import verify_user_time




router = APIRouter()

@router.post("/logout")
def logout(current_user: UserInDB = Depends(get_current_user)):
    try:
        invalidate_token(current_user.token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while logging out",
        )
    return {"detail": "Successfully logged out"}

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # 这里以后要使用ORM来修改数据库，这里图方便直接使用假数据库了
    fake_users_db[user.username]["token"] = access_token
    return {"access_token": access_token, "token_type": "Bearer"}


@router.get("/users/me", response_model=UserInDB)
def read_current_user(current_user: UserInDB = Depends(get_current_user)):
    print("read_current_user called")  # 确认此行是否被打印
    return current_user
