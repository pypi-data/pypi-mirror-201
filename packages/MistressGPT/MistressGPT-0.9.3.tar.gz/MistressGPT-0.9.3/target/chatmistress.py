# -*- coding: utf-8 -*-
import os
𡟭=False
ꌻ=True
ﱢ=None
𭣵=input
𐫍=str
ۮ=len
𥴀=print
ݧ=int
𐣦=os.environ
from typing import Dict,List,Optional,Union
import click
𭺬=click.option
𧏞=click.Choice
𭄓=click.argument
𐢌=click.command
from dotenv import load_dotenv
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from rich.console import Console
from.core import init_chat_components,interact
from.utils import RoleInfo,fetch_template,load_roles
from.webbot2 import creat_gui_chat
load_dotenv()
def 馆(role_info:RoleInfo,𐜄:PromptSession,ڀ:WordCompleter,𩆠:Console,temperature=0.5,top_p=1,max_token_limit=200,init_user_input='您好',debug=𡟭):
 𐴚,prompt,memory,parser,fix_parser,retry_parser=init_chat_components(role_info,temperature,top_p,max_token_limit,debug=debug)
 ꙇ=interact(𐴚,init_user_input,prompt,memory,parser,fix_parser,retry_parser,console=𩆠,debug=debug)
 i=0
 while ꌻ:
  i+=1
  𩆠.𥴀(f"{role_info.mistress_name} ({parsed_response.pose}):",ꙇ.line,sep="\n",style="magenta")
  if debug:
   ﵢ='我今天早上出门之前吃了两个苹果'*20
  else:
   ﵢ=𐜄.prompt('我: ',completer=ڀ)
  if ﵢ=='!switch':
   return 𡟭
  if ﵢ=='!exit':
   return ꌻ
  elif ﵢ.startswith('~'):
   ﵢ=ﵢ[1:]
  ꙇ=interact(𐴚,ﵢ,prompt,memory,parser,fix_parser,retry_parser,console=𩆠,debug=debug)
  memory.summrize_lines()
@𐢌()
@𭄓('cmd',type=𧏞(['cli','gui']))
@𭺬('--debug',default=𡟭,help='Debug mode if True')
@𭺬('--max-token-limit',default=1000,help='temperature for openai')
@𭺬('--ext-url',default=ﱢ,help='外部模板URL')
@𭺬('--concurrency',default=20,help='外部模板URL')
def 𠯫(cmd,debug,𤆿,ext_url,concurrency):
 assert cmd in('cli','gui')
 if 'OPENAI_API_KEY' not in 𐣦:
  𐣦['OPENAI_API_KEY']=𭣵('OPENAI_API_KEY 环境变量未设置, 请输入你的OPENAI_API_KEY: ')
 if ext_url is not ﱢ:
  𬷫:Dict[𐫍,RoleInfo]=fetch_template(ext_url)
 else:
  𬷫:Dict[𐫍,RoleInfo]=load_roles()
 if debug:
  𤆿=200
 if cmd=='gui':
  ﬤ=creat_gui_chat(𬷫,debug=debug,max_token_limit=𤆿)
  ﬤ.queue(concurrency_count=concurrency).launch(inbrowser=ꌻ)
 elif cmd=='cli':
  𩆠=Console()
  𐜄=PromptSession(history=FileHistory('./.role_play_history'))
  ڀ=WordCompleter(['!switch','!exit','~是，主人','~抱歉主人','~都听您的'])
  و=𡟭
  while not و:
   ﭩ=[k for k in 𬷫.keys()]
   if ۮ(ﭩ)>1:
    𥴀(f'选择你的主人: {", ".join([f"{i}: {k}" for i, k in enumerate(role_list)])}')
    if debug:
     㼔=ﭩ[0]
    else:
     㼔=ﭩ[ݧ(𐜄.prompt('我想要 (请输入数字): ').strip())]
   else:
    㼔=ﭩ[0]
   𥴀(f'你选择了{role_selected}作为你的主人. 请按照提示进行对话.')
   و=馆(𬷫[㼔],𐜄,ڀ,𩆠,debug=debug,max_token_limit=𤆿)
  𥴀('Bye~')
if __name__=="__main__":
 𠯫()
# Created by pyminifier (https://github.com/dzhuang/pyminifier3)
