from fastapi import APIRouter, Response,Depends
from pydantic import BaseModel
import aiofiles
import json
from models.users import UserInDB
from utils.auth import get_current_user
from utils.database import get_database
from routers.dependencies.user_deps import get_current_active_admin

def get_circuit_collection():
    db = get_database()
    circuit_collection = db['circuits']
    return circuit_collection

def get_init_circuit_collection():
    db = get_database()
    init_circuit_collection = db['init_circuits']
    return init_circuit_collection

router = APIRouter()

class circuit_Item(BaseModel):
    data: str
    # name: str  # 添加一个新的字段来保存电路图的名称

@router.get('/circuit/raw', status_code=200)
async def get_node_config():
    init_circuit_collection = get_init_circuit_collection()
    init_circuit = init_circuit_collection.find_one({"name": "exp1"})
    if init_circuit and "circuit_data" in init_circuit and 'cnode_anchor' in init_circuit:
        return {'circuit_data':init_circuit["circuit_data"],'cnode_anchor':init_circuit["cnode_anchor"]}
    else:
        return {'circuit_data':{"nodes":[],"edges":[]},'cnode_anchor':{}}

def get_Cnode_Anchor_data(circuit_data):
    # anchor-Cnode 字典
    A_CNode_dict = {}
    # 得到每一个电路节点对应的锚点(即节点id+锚点type)
    for node in circuit_data['nodes']:
        # 检查anchorCnode是否存在
        if 'anchorCnode' not in node['properties']:
            continue
        else:
            anchorCnode = node['properties']['anchorCnode']
            for anchor in node['Anchors']:
                print(anchor['id'])
                try:
                    A_CNode_dict[anchor['id']] = anchorCnode[anchor['type']]
                except:
                    pass
    # 创建一个空字典来存储结果
    CNode_A_dict = {}

    # 遍历 A_CNode_dict 字典
    for anchor, cnode in A_CNode_dict.items():
        # 如果 cnode 已经在 CNode_A_dict 字典中，就将 anchor 添加到对应的列表中
        if cnode in CNode_A_dict:
            CNode_A_dict[cnode].append(anchor)
        # 否则，创建一个新的列表来存储 anchor
        else:
            CNode_A_dict[cnode] = [anchor]
    return CNode_A_dict

# 用来保存实验初始的电路图和节点数据,这个是仅管理员使用的
# 值得注意的是，每次保存初始的电路图时，也同时生成nodes和nodeType数据，用于relay_matrix的初始化
@router.post('/circuit/saveinit', status_code=200)
async def save_node_config(item: circuit_Item, current_user: UserInDB = Depends(get_current_active_admin)):

    circuit_data = json.loads(item.data)
    # 得到每一个电路节点对应的锚点(即节点id+锚点type)
    CNode_A_dict = get_Cnode_Anchor_data(circuit_data)

    init_circuit_collection = get_init_circuit_collection()
    # 使用"exp1"作为索引，将电路图数据保存到新的集合中
    result = init_circuit_collection.update_one(
        {"name": "exp1"},
        {"$set": {"circuit_data": circuit_data,"cnode_anchor": CNode_A_dict}},
        upsert=True
    )
    if result.upserted_id or result.modified_count > 0:
        return {'code': 200,"message": "成功保存初始电路"}
    else:
        return {'code': 400, 'message': "保存初始电路失败"}

# 用来加载电路图和节点数据，但是要结合用户进行修改，即每个用户都有自己的电路图连线
@router.get('/circuit/load', status_code=200)
async def get_node_config(current_user: UserInDB = Depends(get_current_user)):
    circuit_collection = get_circuit_collection()
    user_circuit = circuit_collection.find_one({"username": current_user.username})
    if user_circuit and "circuit_data" in user_circuit:
        return user_circuit["circuit_data"]
    else:
        return {"detail": "No circuit data found for this user"}


@router.post('/circuit/save', status_code=200)
async def save_node_config(item: circuit_Item, current_user: UserInDB = Depends(get_current_user)):
    # 将电路图数据保存到MongoDB中，使用用户名作为索引
    circuit_collection = get_circuit_collection()
    circuit_collection.update_one(
        {"username": current_user.username},
        {"$set": {"circuit_data": json.loads(item.data)}},
        upsert=True
    )
    return item