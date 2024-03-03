# Purpose: 路由的集合，包含所有的exp路由,并添加依赖
from fastapi import APIRouter, Depends
from routers.controller import tfg6930a_api, dm3058_api, node_json_config_api, relay_matrix_api,DM8720_api, tbs1202b_api, dp832_api
from routers.dependencies.user_deps import verify_user_time

# 为所有的exp路由创建一个router, 并添加依赖
exp_router = APIRouter(dependencies=[Depends(verify_user_time)])
exp_router.include_router(dm3058_api.router)
exp_router.include_router(dp832_api.router)
exp_router.include_router(node_json_config_api.router)
exp_router.include_router(tbs1202b_api.router)
exp_router.include_router(tfg6930a_api.router)
exp_router.include_router(relay_matrix_api.router)
exp_router.include_router(DM8720_api.router)
