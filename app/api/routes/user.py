from fastapi import APIRouter

from app.api.depends import CurrentUser, SessionDep
from app.crud.UserCRUD import UserCRUD
from app.models.base_models.UserBase import UserUpdate
from app.models.public_models.Out import ErrorMod, RespMod

router = APIRouter()


@router.get("/ping", summary="健康检查接口", description="用于检查API服务是否正常运行")
def health_check() -> dict:
    """执行简单的健康检查。

    返回一个包含状态信息的字典,用于确认API服务正常运行。

    Returns:
        dict: 包含状态信息的响应字典
            - status (str): 服务状态
            - message (str): 状态描述
    """
    return {"status": "healthy", "message": "API服务运行正常"}


@router.get(
    "/profile", summary="获取用户详细信息", description="获取当前登录用户的完整个人信息"
)
def get_user_profile(user: CurrentUser, session: SessionDep):
    user = UserCRUD(session=session).get_user(user.id)
    if user:
        return RespMod(data=user.model_dump())
    else:
        raise ErrorMod(message="用户不存在")


@router.post(
    "/update", summary="更新用户信息", description="更新当前登录用户的个人信息"
)
def update_user_profile(user: CurrentUser, session: SessionDep, update_data: UserUpdate):
    # 将Pydantic模型转换为字典，排除None值
    update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)

    updated_user = UserCRUD(session=session).update_user(user.id, update_dict)
    if updated_user:
        return RespMod(data=updated_user.model_dump())
    else:
        raise ErrorMod(message="用户不存在或更新失败")
