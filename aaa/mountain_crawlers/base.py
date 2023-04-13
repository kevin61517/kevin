from attr import attrib, attrs
from .tools import Valid


@attrs
class Config:
    """配置"""
    # 隊伍名稱
    team_data = attrib(dict, validator=Valid.pass_if_type(dict))
    # 會員
    member_data = attrib(list, validator=Valid.pass_if_type(list))
