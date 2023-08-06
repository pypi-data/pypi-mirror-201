# -*- coding: utf-8 -*-
import copy
ﱢ=None
ۮ=len
𡟭=False
玜=open
𣐢=Exception
歿=type
ࢭ=dict
ꌻ=True
𞡔=list
𐫍=str
𣨨=hasattr
𐨩=copy.deepcopy
import logging
𘈅=logging.info
𞸞=logging.debug
import os
𐪌=os.getenv
from pathlib import Path
import time
䚟=time.sleep
from typing import Dict
import gradio as gr
𡴛=gr.Slider
𭙆=gr.File
𭿤=gr.Accordion
ﮕ=gr.Tab
𧙓=gr.Textbox
𒅛=gr.Request
ߕ=gr.Markdown
ߨ=gr.HTML
𛁗=gr.Column
𧃖=gr.Row
䕾=gr.State
𦹠=gr.Blocks
ﶘ=gr.update
𧜬=gr.Button
ه=gr.Dropdown
舛=gr.Chatbot
𞢡=gr.Error
벧=gr.themes
import yaml
𭷎=yaml.dump
𡪏=yaml.safe_load
from.core import init_chat_components,interact
from.utils import RoleInfo
𡹘=벧.Soft(primary_hue=벧.Color(c50="#02C160",c100="rgba(2, 193, 96, 0.2)",c200="#02C160",c300="rgba(2, 193, 96, 0.32)",c400="rgba(2, 193, 96, 0.32)",c500="rgba(2, 193, 96, 1.0)",c600="rgba(2, 193, 96, 1.0)",c700="rgba(2, 193, 96, 0.32)",c800="rgba(2, 193, 96, 0.32)",c900="#02C160",c950="#02C160"),secondary_hue=벧.Color(c50="#576b95",c100="#576b95",c200="#576b95",c300="#576b95",c400="#576b95",c500="#576b95",c600="#576b95",c700="#576b95",c800="#576b95",c900="#576b95",c950="#576b95"),neutral_hue=벧.Color(name="gray",c50="#f9fafb",c100="#f3f4f6",c200="#e5e7eb",c300="#d1d5db",c400="#B2B2B2",c500="#808080",c600="#636363",c700="#515151",c800="#393939",c900="#272727",c950="#171717"),radius_size=벧.sizes.radius_sm).set(button_primary_background_fill="#06AE56",button_primary_background_fill_dark="#06AE56",button_primary_background_fill_hover="#07C863",button_primary_border_color="#06AE56",button_primary_border_color_dark="#06AE56",button_primary_text_color="#FFFFFF",button_primary_text_color_dark="#FFFFFF",button_secondary_background_fill="#F2F2F2",button_secondary_background_fill_dark="#2B2B2B",button_secondary_text_color="#393939",button_secondary_text_color_dark="#FFFFFF",block_title_text_color="*primary_500",block_title_background_fill="*primary_100",input_background_fill="#F6F6F6")
def 芽(s):
 if s is ﱢ:
  return ""
 if ۮ(s)<=8:
  return s
 else:
  𪐹=s[:4]
  𫖘=s[-4:]
  阮="*"*(ۮ(s)-8)
  return 𪐹+阮+𫖘
ꕢ=𡟭
𬣺=["gpt-3.5-turbo","gpt-3.5-turbo-0301","gpt-4","gpt-4-0314","gpt-4-32k","gpt-4-32k-0314"]
ﮬ=1.0
𤼊=0.9
ﶦ="history"
ࠕ="templates"
ﱂ=Path(__file__).parent/'assets'
with 玜(ﱂ/"custom.css","r",encoding="utf-8")as f:
 姖=f.read()
𧛻="""<h1 align="left" style="min-width:200px; margin-top:6px; white-space: nowrap;">chatmistress</h1>"""
ⷉ="""<div class="versions">{versions}</div>
"""
def 𢖏(𦞛,𫵩,ﱑ,𗽧,debug=𡟭):
 ﵖ,ݲ,𘊕,옂,ࠔ,ﶮ=init_chat_components(𦞛,𫵩,ﱑ,𗽧,debug=debug)
 return{"conversation":ﵖ,"prompt":ݲ,"memory":𘊕,"parser":옂,"fix_parser":ࠔ,"retry_parser":ﶮ,'temperature':𫵩,'top_p':ﱑ}
def 𩌾(𞤕,𘄦,debug=𡟭):
 ﵖ=𞤕['conversation']
 ݲ=𞤕['prompt']
 𘊕=𞤕['memory']
 옂=𞤕['parser']
 ࠔ=𞤕['fix_parser']
 ﶮ=𞤕['retry_parser']
 return interact(ﵖ,𘄦,ݲ,𘊕,옂,ࠔ,ﶮ,debug=debug,temperature=𞤕['temperature'],top_p=𞤕['top_p'],openai_api_key=𞤕['openai_api_key'])
def ﺖ(慫,𘪸):
 try:
  ri=RoleInfo(**𡪏(慫))
  if ri.mistress_name in 𘪸:
   del 𘪸[ri.mistress_name]
  𘪸[ri.mistress_name]=ri
 except 𣐢 as e:
  raise 𞢡(f"格式错误! {e}")
 return 𘪸
def 𡿠(𞤕,햽,𫵩,ﱑ,𘪸,ޡ,systemPromptTxt=ﱢ,chatbot=ﱢ,user_name=ﱢ):
 鱺=ޡ
 𦞛=𘪸[鱺]if 歿(𘪸)is ࢭ else 𘪸.value[鱺]
 systemPromptTxt=𭷎(𦞛.ࢭ(),allow_unicode=ꌻ)
 𗽧=300
 𐭭=𢖏(𦞛,𫵩,ﱑ,𗽧,debug=𡟭)
 if chatbot is ﱢ:
  return 𐭭,systemPromptTxt
 else:
  return 𐭭,systemPromptTxt,舛.update(label=鱺,value=[]),[]
def 𞡙(𘪸,plain=𡟭):
 if 歿(𘪸)is not ࢭ:
  ﰖ=𞡔(𘪸.value.keys())
 else:
  ﰖ=𞡔(𘪸.keys())
 if plain is ꌻ:
  return ﰖ
 else:
  return ه.update(choices=ﰖ,value=ﰖ[-1])
def 𐤇(𐬡,慫,ﻹ,햽,𐠎):
 𐠬=f'## 场景\n{systemPromptTxt}\n\n\n# 聊天记录:\n\n'
 for ﵖ in ﻹ:
  𫎅,𐿂=ﵖ
  𐠬+=f'{user_name}: {user}\n\n'
  𐠬+=f'{role_selected}: {bot}\n\n'
 with 玜(f'{saveFileName}.md','w',encoding='utf-8')as f:
  f.write(𐠬)
def 𘈕(ﻹ,ﶬ):
 return ﻹ,ﶬ,''
def ﴂ(𠶮,ﻹ,ﶬ):
 return 𠶮,ﻹ,ﶬ,''
def 𰝇(𐦈,慫,ﻹ,𠶮,𐠎):
 𐬡=''
 return 𐬡,慫,ﻹ,𠶮
def ﵪ():
 𞸁=""
 return ﮬ,𤼊,𞸁
def 䠒():
 𞸞("显示取消按钮，隐藏发送按钮")
 return 𧜬.update(visible=𡟭),𧜬.update(visible=ꌻ)
def 𪆳():
 return(ﶘ(interactive=ꌻ),𧜬.update(visible=ꌻ))
def 𦗢():
 𞸞("重置文本框")
 return ﶘ(value="")
def 𐼶(openai_api_key):
 pass
def 𧀊(𦿷):
 𦿷=𦿷.strip()
 䋒=f"API密钥更改为了{hide_middle_chars(key)}"
 𘈅(䋒)
 return 𦿷,䋒
def 𞡊():
 𘈅("重置状态")
 𞸁=""
 return[],[],[],𞸁
def 𬱢(inputs,𠶮):
 𐳍=𦗢()
 𠶮.append([inputs,ﱢ])
 return(inputs,𠶮,ﶘ(value="",interactive=𡟭),𧜬.update(visible=𡟭),𧜬.update(visible=ꌻ))
def ﱊ(𞤕,openai_api_key,ﻹ,inputs,𠶮,all_token_counts,ﱑ,𫵩,debug=𡟭,selected_model=𬣺[0],should_check_token_count=ꌻ):
 debug=𡟭
 if debug:
  䚟(0.1)
  𠶮[-1][1]=f'input is {inputs}'
 else:
  𞤕['temperature']=𫵩
  𞤕['top_p']=ﱑ
  𞤕['selected_model']=selected_model
  𞤕['openai_api_key']=openai_api_key
  𣤡=𩌾(𞤕,inputs)
  𠶮[-1][1]=f'({parsed_response.pose}): {parsed_response.line}'
 ﻹ.append(𐨩(𠶮[-1]))
 𞸁=""
 ﶬ=all_token_counts+[1]
 return 𠶮,ﻹ,𞸁,ﶬ
def 琄(roles:Dict[𐫍,RoleInfo],debug=𡟭,max_token_limit=2000):
 with 𦹠(css=姖,theme=𡹘)as ﱰ:
  𞸇=𐪌("OPENAI_API_KEY",ﱢ)
  𐠎=䕾("我")
  ﻹ=䕾([])
  ﶬ=䕾([])
  𘪸=䕾(roles)
  햽=䕾('Hello')
  𞤕=䕾("")
  㽿=䕾(𞸇)
  𞡷=䕾("")
  debug=䕾(debug)
  ﱑ=0.9
  𫵩=0.9
  with 𧃖():
   with 𛁗():
    ߨ(𧛻)
    ࢲ=ߕ(value="",elem_id="user_info")
   𞸁=ߕ("status",elem_id="status_display")
   def 𧘂(request:𒅛):
    if 𣨨(request,"username")and request.username:
     𘈅(f"Get User Name: {request.username}")
     return ߕ.update(value=f"User: {request.username}"),request.username
    else:
     return ߕ.update(value=f"User: default",visible=𡟭),""
   ﱰ.load(𧘂,inputs=ﱢ,outputs=[ࢲ,𐠎])
  with 𧃖().style(equal_height=ꌻ):
   with 𛁗(scale=3):
    with 𧃖():
     𠶮=舛(label=햽.value,elem_id="chuanhu_chatbot").style(height="100%")
    with 𧃖():
     with 𛁗(scale=12):
      𘄦=𧙓(show_label=𡟭,placeholder="在这里输入").style(container=𡟭)
     with 𛁗(min_width=70,scale=1):
      𐬩=𧜬("发送",variant="primary")
    with 𧃖():
     𩪐=𧜬("重启对话")
   with 𛁗(scale=1,min_width=400):
    with 𛁗(min_width=400):
     𞠫=𞡙(𘪸,plain=ꌻ)
     鱺=𞠫[0]
     𠶮.label=鱺
     𞤕.value,initial_prompt=𡿠(𞤕,햽,𫵩,ﱑ,𘪸,鱺)
     with ﮕ(label="Prompt"):
      慫=𧙓(show_label=ꌻ,placeholder=f"在这里输入System Prompt...",label="System prompt",value=initial_prompt,lines=20).style(container=𡟭)
      𐲐=𧜬("保存 Prompt")
      with 𭿤(label="加载Prompt模板",玜=ꌻ):
       with 𛁗():
        with 𧃖():
         with 𛁗(scale=1):
          𗀄=𧜬("🔄 刷新")
         with 𛁗():
          ޡ=ه(label="从Prompt模板中加载",choices=𞠫,multiselect=𡟭,value=鱺).style(container=𡟭)
     with ﮕ(label="保存/加载"):
      with 𭿤(label="保存对话历史记录",玜=ꌻ):
       with 𛁗():
        with 𧃖():
         with 𛁗(scale=6):
          𐬡=𧙓(show_label=ꌻ,placeholder=f"设置文件名: 默认为.json，可选为.md",label="设置保存文件名",value="对话历史记录").style(container=ꌻ)
         with 𛁗(scale=1):
          𒆡=𧜬("💾 保存对话")
          ߕ("默认保存于history文件夹")
        with 𧃖():
         with 𛁗():
          𐦈=𭙆(interactive=ꌻ)
     with ﮕ(label="ChatGPT"):
      𧙩=𧙓(show_label=ꌻ,placeholder=f"OpenAI API-key...",value=芽(𞸇),歿="password",visible=not ꕢ,label="API-Key")
     with ﮕ(label="高级"):
      ߕ("# ⚠️ 务必谨慎更改 ⚠️\n\n如果无法使用请恢复默认设置")
      𐱀=𧜬("🔙 恢复默认设置")
      with 𭿤("参数",玜=𡟭):
       ﱑ=𡴛(minimum=-0,maximum=1.0,value=ﮬ,step=0.05,interactive=ꌻ,label="Top-p")
       𫵩=𡴛(minimum=-0,maximum=2.0,value=𤼊,step=0.1,interactive=ꌻ,label="Temperature")
  𐦓=ࢭ(fn=𬱢,inputs=[𘄦,𠶮],outputs=[𞡷,𠶮,𘄦,𐬩],show_progress=ꌻ)
  ﯖ=ࢭ(fn=ﱊ,inputs=[𞤕,㽿,ﻹ,𞡷,𠶮,ﶬ,ﱑ,𫵩,𞠻],outputs=[𠶮,ﻹ,𞸁,ﶬ],show_progress=ꌻ)
  ﳻ=ࢭ(fn=𪆳,inputs=[],outputs=[𘄦,𐬩])
  𞺐=ࢭ(fn=𦗢,inputs=[],outputs=[𘄦])
  𘄦.submit(**𐦓).then(**ﯖ).then(**ﳻ)
  𐬩.click(**𐦓).then(**ﯖ).then(**ﳻ)
  גּ=ࢭ(fn=𡿠,inputs=[𞤕,햽,𫵩,ﱑ,𘪸,ޡ,慫,𠶮],outputs=[𞤕,慫,𠶮,ﻹ])
  𩪐.click(𞡊,outputs=[𠶮,ﻹ,ﶬ,𞸁],show_progress=ꌻ).then(show_progress=ꌻ,**גּ)
  𩪐.click(**𞺐)
  𧙩.change(𧀊,𧙩,[㽿,𞸁])
  𐤄=ࢭ(fn=𞡙,inputs=[𘪸],outputs=[ޡ])
  𗀄.click(**𐤄)
  ޡ.change(show_progress=ꌻ,**גּ)
  𐲐.click(ﺖ,[慫,𘪸],[𘪸]).then(**𐤄)
  𒆡.click(𐤇,[𐬡,慫,ﻹ,햽,𐠎],show_progress=ꌻ)
  𐦈.change(𰝇,[𐦈,慫,ﻹ,𠶮,𐠎],[𐬡,慫,ﻹ,𠶮])
  𐱀.click(ﵪ,[],[ﱑ,𫵩,𞸁],show_progress=ꌻ)
 return ﱰ
if __name__=='__main__':
 from dotenv import load_dotenv
 load_dotenv()
 ﱰ=琄()
 ﱰ.launch()
# Created by pyminifier (https://github.com/dzhuang/pyminifier3)
