# -*- coding: utf-8 -*-
from typing import List
𐫍=str
ﱢ=None
𥴀=print
import requests
ݸ=requests.get
import yaml
𡪏=yaml.safe_load
㗈=yaml.FullLoader
ܖ=yaml.load
from pathlib import Path
from pydantic import BaseModel,Field
class 𩣢(BaseModel):
 𭇤:𐫍=Field(description="mistress_name")
 mistress_role:𐫍=Field(description="mistress_role")
 user_role:𐫍=Field(description="user_role")
 user_nickname:𐫍=Field(description="user_nickname")
 user_description:𐫍=Field(description="user_description")
 story_settings:𐫍=Field(description="story_settings")
 mistress_tasks:List[𐫍]=Field(description="mistress_tasks")
def 𤻪(roles_dir=ﱢ):
 ﴣ={}
 if roles_dir is not ﱢ:
  ﭻ=Path(roles_dir)
 else:
  ﭻ=Path(__file__).parent/'roles'
 𥴀(ﭻ.resolve())
 for p in ﭻ.glob('*.yml'):
  𣾣=ܖ(p.read_text(),Loader=㗈)
  ﴣ[𣾣['mistress_name']]=𩣢(**𣾣)
 return ﴣ
def 엡(url):
 𠏣=ݸ(url)
 辪=𡪏(𠏣.text)
 ri=𩣢(**辪)
 return{ri.mistress_name:ri}
if __name__=='__main__':
 𥴀(엡('https://pastebin.com/raw/Q0Si6SKr'))
# Created by pyminifier (https://github.com/dzhuang/pyminifier3)
