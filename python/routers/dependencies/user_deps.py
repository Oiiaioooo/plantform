# user_deps.py
from fastapi import HTTPException, status, Depends
from datetime import datetime
from models.users import UserInDB  # 导入或定义 UserInDB 模型
from utils.auth import get_current_user

def verify_user_time(current_user: UserInDB = Depends(get_current_user)):
    now = datetime.now()
    print("verify_user_time called",current_user.valid_from, current_user.valid_until, now)
    if not (current_user.valid_from <= now <= current_user.valid_until):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="当前时间不在允许的实验时间段内"
        )
    return current_user


def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=400, detail="未找到用户")
    return current_user

# 应用在 admin-only的路由中
def get_current_active_admin(current_user: UserInDB = Depends(get_current_active_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="没有足够的权限",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user