# -*- coding: utf-8 -*-
import gradio as gr
𡟭=False
ﱢ=None
𧙓=gr.Textbox
𛁗=gr.Column
𧃖=gr.Row
舛=gr.Chatbot
𦹠=gr.Blocks
from chatmistress.core import init_chat_components,interact
from chatmistress.utils import RoleInfo
def 𐦁(role_info:RoleInfo,init_user_input="hi",temperature=0.7,max_token_limit=2000,debug=𡟭):
 킡,prompt,memory,parser,fix_parser,retry_parser=init_chat_components(role_info,temperature,max_token_limit,debug=debug)
 𦺶=interact(킡,init_user_input,prompt,memory,parser,fix_parser,retry_parser,debug=debug)
 def ߧ(𩇺,text):
  𩇺=𩇺+[(text,ﱢ)]
  return 𩇺,""
 def 𐠳(𩇺):
  𢃇=𩇺[-1][0].strip()
  ﭞ=interact(킡,𢃇,prompt,memory,parser,fix_parser,retry_parser,debug=debug)
  𩇺[-1][1]=f'({parsed_response.pose}): {parsed_response.line}'
  return 𩇺
 with 𦹠()as demo:
  𞤰=舛([(ﱢ,f'({init_response.pose}): {init_response.line}')],elem_id="chatbot",label=role_info.mistress_name).style(height=750)
  with 𧃖():
   with 𛁗(scale=1.0):
    𨻮=f'输入文字然后Enter'
    𧦺=𧙓(label=role_info.user_role,show_label=𡟭,placeholder=𨻮).style(container=𡟭)
  𧦺.submit(ߧ,[𞤰,𧦺],[𞤰,𧦺]).then(𐠳,𞤰,𞤰)
 return demo
# Created by pyminifier (https://github.com/dzhuang/pyminifier3)
