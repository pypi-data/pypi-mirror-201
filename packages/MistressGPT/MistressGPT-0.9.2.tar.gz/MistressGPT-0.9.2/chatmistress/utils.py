from typing import List
import requests
import yaml
from pathlib import Path
from pydantic import BaseModel, Field


class RoleInfo(BaseModel):
    mistress_name: str = Field(description="mistress_name")
    mistress_role: str = Field(description="mistress_role")
    user_role: str = Field(description="user_role")
    user_nickname: str = Field(description="user_nickname")
    user_description: str = Field(description="user_description")
    story_settings: str = Field(description="story_settings")
    mistress_tasks: List[str] = Field(description="mistress_tasks")


def load_roles(roles_dir=None):
    roles = {}
    if roles_dir is not None:
        role_dir = Path(roles_dir)
    else:
        role_dir = Path(__file__).parent / 'roles'
    print(role_dir.resolve())
    for p in role_dir.glob('*.yml'):
        role_config = yaml.load(p.read_text(), Loader=yaml.FullLoader)
        roles[role_config['mistress_name']] = RoleInfo(**role_config)
    return roles


def fetch_template(url):
    response = requests.get(url)
    res = yaml.safe_load(response.text)
    ri = RoleInfo(**res)
    return {ri.mistress_name: ri}


if __name__ == '__main__':
    print(fetch_template('https://pastebin.com/raw/Q0Si6SKr'))
