import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.controller import users_api
from routers import exp_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 这里可以设置允许的源，或使用通配符 "*" 允许所有源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头部
)
app.include_router(exp_routes.exp_router, prefix='/api')
app.include_router(users_api.router)
if __name__ == '__main__':
    uvicorn.run(app='main:app', host="0.0.0.0", port=8001, reload=True)
