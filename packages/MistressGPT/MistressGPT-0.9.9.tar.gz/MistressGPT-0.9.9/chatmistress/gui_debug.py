import os
from typing import Dict
from dotenv import load_dotenv

from .utils import RoleInfo, load_roles
from .webbot2 import creat_gui_chat
load_dotenv()
roles: Dict[str, RoleInfo] = load_roles()
debug = True
max_token_limit = 1000
demo = creat_gui_chat(
    roles, debug=debug, max_token_limit=max_token_limit)
if __name__ == "__main__":
    demo.launch()
