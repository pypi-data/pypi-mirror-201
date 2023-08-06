import copy
import logging
import os
from pathlib import Path
import time
from typing import Dict

import gradio as gr
import yaml

from .core import init_chat_components, interact
from .utils import RoleInfo

small_and_beautiful_theme = gr.themes.Soft(
    primary_hue=gr.themes.Color(
        c50="#02C160",
        c100="rgba(2, 193, 96, 0.2)",
        c200="#02C160",
        c300="rgba(2, 193, 96, 0.32)",
        c400="rgba(2, 193, 96, 0.32)",
        c500="rgba(2, 193, 96, 1.0)",
        c600="rgba(2, 193, 96, 1.0)",
        c700="rgba(2, 193, 96, 0.32)",
        c800="rgba(2, 193, 96, 0.32)",
        c900="#02C160",
        c950="#02C160",
    ),
    secondary_hue=gr.themes.Color(
        c50="#576b95",
        c100="#576b95",
        c200="#576b95",
        c300="#576b95",
        c400="#576b95",
        c500="#576b95",
        c600="#576b95",
        c700="#576b95",
        c800="#576b95",
        c900="#576b95",
        c950="#576b95",
    ),
    neutral_hue=gr.themes.Color(
        name="gray",
        c50="#f9fafb",
        c100="#f3f4f6",
        c200="#e5e7eb",
        c300="#d1d5db",
        c400="#B2B2B2",
        c500="#808080",
        c600="#636363",
        c700="#515151",
        c800="#393939",
        c900="#272727",
        c950="#171717",
    ),
    radius_size=gr.themes.sizes.radius_sm,
).set(
    button_primary_background_fill="#06AE56",
    button_primary_background_fill_dark="#06AE56",
    button_primary_background_fill_hover="#07C863",
    button_primary_border_color="#06AE56",
    button_primary_border_color_dark="#06AE56",
    button_primary_text_color="#FFFFFF",
    button_primary_text_color_dark="#FFFFFF",
    button_secondary_background_fill="#F2F2F2",
    button_secondary_background_fill_dark="#2B2B2B",
    button_secondary_text_color="#393939",
    button_secondary_text_color_dark="#FFFFFF",
    # background_fill_primary="#F7F7F7",
    # background_fill_primary_dark="#1F1F1F",
    block_title_text_color="*primary_500",
    block_title_background_fill="*primary_100",
    input_background_fill="#F6F6F6",
)


def hide_middle_chars(s):
    if s is None:
        return ""
    if len(s) <= 8:
        return s
    else:
        head = s[:4]
        tail = s[-4:]
        hidden = "*" * (len(s) - 8)
        return head + hidden + tail


HIDE_MY_KEY = False
MODELS = [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-32k",
    "gpt-4-32k-0314",
]  # 可选的模型

TOP_P = 1.0
TEMPERATURE = 0.9

HISTORY_DIR = "history"
TEMPLATES_DIR = "templates"

asset_dir = Path(__file__).parent / 'assets'
with open(asset_dir / "custom.css", "r", encoding="utf-8") as f:
    customCSS = f.read()

title = """<h1 align="left" style="min-width:200px; margin-top:6px; white-space: nowrap;">MistressGPT</h1>"""


footer = """\
<div class="versions">{versions}</div>
"""


def wrap_init_chat_components(role_info, temperature, top_p, max_token_limit, debug=False):
    """
    包装一下init_chat_components函数，以便在gradio中使用.
    """
    conversation, prompt, memory, parser, fix_parser, retry_parser = init_chat_components(
        role_info, temperature, top_p, max_token_limit, debug=debug)

    return {
        "conversation": conversation,
        "prompt": prompt,
        "memory": memory,
        "parser": parser,
        "fix_parser": fix_parser,
        "retry_parser": retry_parser,
        'temperature': temperature,
        'top_p': top_p,
    }


def wrap_interact(chat_info, user_input, debug=False):
    """
    包装一下interact函数，以便在gradio中使用"""
    conversation = chat_info['conversation']
    prompt = chat_info['prompt']
    memory = chat_info['memory']
    parser = chat_info['parser']
    fix_parser = chat_info['fix_parser']
    retry_parser = chat_info['retry_parser']

    return interact(
        conversation, user_input, prompt, memory, parser, fix_parser,
        retry_parser, debug=debug,
        temperature=chat_info['temperature'],
        top_p=chat_info['top_p'],
        openai_api_key=chat_info['openai_api_key']
    )


def change_prompt(systemPromptTxt, role_cards):
    # print(f'change_prompt: {type(role_cards)}')
    try:
        ri = RoleInfo(**yaml.safe_load(systemPromptTxt))
        if ri.mistress_name in role_cards:
            del role_cards[ri.mistress_name]
        role_cards[ri.mistress_name] = ri
    except Exception as e:
        raise gr.Error(f"格式错误! {e}")

    return role_cards


def read_template_create_chat(chat_info, role_selected, temperature, top_p, role_cards, templateSelectDropdown, systemPromptTxt=None, chatbot=None, user_name=None):
    """
    从模板文件中读取模板内容, 并更新系统提示文本. 如果有必要，重置对话
    """
    role_name_selected = templateSelectDropdown
    role_info = role_cards[role_name_selected] if type(
        role_cards) is dict else role_cards.value[role_name_selected]
    systemPromptTxt = yaml.dump(role_info.dict(), allow_unicode=True)
    # 由于重新选择了角色，就要重新初始化聊天机器人

    max_token_limit = 300
    chat_info_res = wrap_init_chat_components(
        role_info, temperature, top_p, max_token_limit, debug=False)

    if chatbot is None:
        return chat_info_res, systemPromptTxt
    else:
        # 重置对话
        # chat_info, systemPromptTxt, chatbot, history
        return chat_info_res, systemPromptTxt, gr.Chatbot.update(label=role_name_selected, value=[]), []


def get_templates(role_cards, plain=False):
    """
    从网上或者本地文件获取模板列表.
    TODO: 默认情况下从本地和网上获取模板列表
    """

    # roles = {}

    # role_dir = Path(__file__).parent / 'roles'
    # for p in role_dir.glob('*.yml'):
    #     role_config = yaml.load(p.read_text(), Loader=yaml.FullLoader)
    #     roles[role_config['mistress_name']] = RoleInfo(**role_config)
    # return selected template name

    if type(role_cards) is not dict:
        templates = list(role_cards.value.keys())
    else:
        templates = list(role_cards.keys())
    if plain is True:
        return templates
    else:
        # 选择最新的那个prompt
        return gr.Dropdown.update(choices=templates, value=templates[-1])


def save_chat_history(saveFileName, systemPromptTxt, history, role_selected, user_name):
    """
    """
    contents = f'## 场景\n{systemPromptTxt}\n\n\n# 聊天记录:\n\n'
    for conversation in history:
        user, bot = conversation
        contents += f'{user_name}: {user}\n\n'
        contents += f'{role_selected}: {bot}\n\n'

    with open(f'{saveFileName}.md', 'w', encoding='utf-8') as f:
        f.write(contents)


# def get_history_names(plain=False, user_name=""):
#     """
#     TODO 读取本地的历史记录文件名列表
#     注意，这里的对话要先被解析，所以我们暂时不处理这部分内同
#     """
#     logging.info(f"从用户 {user_name} 中获取历史记录文件名列表")
#     return ['s', 'k']


def delete_first_conversation(history, token_count):
    return history, token_count, ''


def delete_last_conversation(chatbot, history, token_count):
    return chatbot, history, token_count, ''


def load_chat_history(downloadFile, systemPromptTxt, history, chatbot, user_name):
    saveFileName = ''
    return saveFileName, systemPromptTxt, history, chatbot


def reset_default():
    status_display = ""
    return TOP_P, TEMPERATURE, status_display


def start_outputing():
    logging.debug("显示取消按钮，隐藏发送按钮")
    return gr.Button.update(visible=False), gr.Button.update(visible=True)


def end_outputing():
    return (
        gr.update(interactive=True),
        gr.Button.update(visible=True),
    )


def reset_textbox():
    logging.debug("重置文本框")
    return gr.update(value="")


def get_usage(openai_api_key):
    pass


def submit_key(key):
    key = key.strip()
    msg = f"API密钥更改为了{hide_middle_chars(key)}"
    logging.info(msg)
    return key, msg


def reset_state():
    logging.info("重置状态")
    status_display = ""
    return [], [], [], status_display


def transfer_input(inputs, chatbot):
    # 一次性返回，降低延迟
    textbox = reset_textbox()
    chatbot.append([inputs, None])
    return (
        inputs,
        chatbot,
        gr.update(value="", interactive=False),
        gr.Button.update(visible=False),
        gr.Button.update(visible=True),
    )


def predict(
    chat_info,
    openai_api_key,
    history,
    inputs,
    chatbot,
    all_token_counts,
    top_p,
    temperature,
    debug=False,
    selected_model=MODELS[0],
    should_check_token_count=True,
):
    # outputing = start_outputing()
    debug = False
    if debug:
        time.sleep(0.1)
        chatbot[-1][1] = f'input is {inputs}'
    else:
        chat_info['temperature'] = temperature
        chat_info['top_p'] = top_p
        chat_info['selected_model'] = selected_model
        chat_info['openai_api_key'] = openai_api_key

        parsed_response = wrap_interact(chat_info, inputs)
        chatbot[-1][1] = f'({parsed_response.pose}): {parsed_response.line}'

    history.append(copy.deepcopy(chatbot[-1]))
    status_display = ""
    token_count = all_token_counts + [1]

    return chatbot, history, status_display, token_count


def creat_gui_chat(roles: Dict[str, RoleInfo], debug=False, max_token_limit=2000):
    with gr.Blocks(css=customCSS, theme=small_and_beautiful_theme) as demo:
        my_api_key = os.getenv("OPENAI_API_KEY", None)
        user_name = gr.State("我")
        history = gr.State([])
        token_count = gr.State([])
        role_cards = gr.State(roles)
        role_selected = gr.State('Hello')
        chat_info = gr.State("")

        user_api_key = gr.State(my_api_key)
        user_question = gr.State("")
        debug = gr.State(debug)

        top_p = 0.9
        temperature = 0.9

        with gr.Row():
            with gr.Column():
                gr.HTML(title)
                user_info = gr.Markdown(value="", elem_id="user_info")
            status_display = gr.Markdown("status", elem_id="status_display")

            # https://github.com/gradio-app/gradio/pull/3296
            def create_greeting(request: gr.Request):
                if hasattr(request, "username") and request.username:  # is not None or is not ""
                    logging.info(f"Get User Name: {request.username}")
                    return gr.Markdown.update(value=f"User: {request.username}"), request.username
                else:
                    return gr.Markdown.update(value=f"User: default", visible=False), ""
            demo.load(create_greeting, inputs=None,
                      outputs=[user_info, user_name])

        with gr.Row().style(equal_height=True):
            with gr.Column(scale=3):
                with gr.Row():
                    chatbot = gr.Chatbot(
                        label=role_selected.value,
                        elem_id="chuanhu_chatbot").style(height="100%")
                with gr.Row():
                    with gr.Column(scale=12):
                        user_input = gr.Textbox(
                            show_label=False, placeholder="在这里输入"
                        ).style(container=False)
                    with gr.Column(min_width=70, scale=1):
                        submitBtn = gr.Button("发送", variant="primary")

                with gr.Row():
                    emptyBtn = gr.Button(
                        "重启对话",
                    )

            with gr.Column(scale=1, min_width=400):
                with gr.Column(min_width=400):
                    role_names = get_templates(role_cards, plain=True)
                    role_name_selected = role_names[0]
                    chatbot.label = role_name_selected
                    chat_info.value, initial_prompt = read_template_create_chat(
                        chat_info, role_selected, temperature, top_p, role_cards, role_name_selected)
                    with gr.Tab(label="Prompt"):
                        systemPromptTxt = gr.Textbox(
                            show_label=True,
                            placeholder=f"在这里输入设定...",
                            label="故事设定",
                            value=initial_prompt,
                            lines=20,
                        ).style(container=False)
                        savePromptBtn = gr.Button(
                            "保存设定",
                        )
                        with gr.Accordion(label="加载设定", open=True):
                            with gr.Column():
                                with gr.Row():
                                    with gr.Column(scale=1):
                                        templateRefreshBtn = gr.Button("🔄 刷新")
                                    with gr.Column():
                                        templateSelectDropdown = gr.Dropdown(
                                            label="选择设定",
                                            choices=role_names,
                                            multiselect=False,
                                            value=role_name_selected,
                                        ).style(container=False)

                    with gr.Tab(label="保存/加载"):
                        with gr.Accordion(label="保存对话历史记录", open=True):
                            with gr.Column():
                                # with gr.Row():
                                #     with gr.Column(scale=6):
                                #         historyFileSelectDropdown = gr.Dropdown(
                                #             label="从列表中加载对话",
                                #             choices=get_history_names(
                                #                 plain=True),
                                #             multiselect=False,
                                #             value=get_history_names(
                                #                 plain=True)[0],
                                #         )
                                #     with gr.Column(scale=1):
                                #         historyRefreshBtn = gr.Button("🔄 刷新")
                                with gr.Row():
                                    with gr.Column(scale=6):
                                        saveFileName = gr.Textbox(
                                            show_label=True,
                                            placeholder=f"设置文件名: 默认为.json，可选为.md",
                                            label="设置保存文件名",
                                            value="对话历史记录",
                                        ).style(container=True)
                                    with gr.Column(scale=1):
                                        saveHistoryBtn = gr.Button("💾 保存对话")

                                        gr.Markdown("默认保存于history文件夹")
                                with gr.Row():
                                    with gr.Column():
                                        downloadFile = gr.File(
                                            interactive=True)

                    with gr.Tab(label="ChatGPT"):
                        keyTxt = gr.Textbox(
                            show_label=True,
                            placeholder=f"OpenAI API-key...",
                            value=hide_middle_chars(my_api_key),
                            type="password",
                            visible=not HIDE_MY_KEY,
                            label="API-Key",
                        )

                    with gr.Tab(label="高级"):
                        gr.Markdown("# ⚠️ 务必谨慎更改 ⚠️\n\n如果无法使用请恢复默认设置")
                        default_btn = gr.Button("🔙 恢复默认设置")

                        with gr.Accordion("参数", open=False):
                            top_p = gr.Slider(
                                minimum=-0,
                                maximum=1.0,
                                value=TOP_P,
                                step=0.05,
                                interactive=True,
                                label="Top-p",
                            )
                            temperature = gr.Slider(
                                minimum=-0,
                                maximum=2.0,
                                value=TEMPERATURE,
                                step=0.1,
                                interactive=True,
                                label="Temperature",
                            )

        transfer_input_args = dict(
            fn=transfer_input, inputs=[user_input, chatbot], outputs=[
                user_question, chatbot, user_input, submitBtn], show_progress=True
        )

        chatgpt_predict_args = dict(
            fn=predict,
            inputs=[
                chat_info,
                user_api_key,
                history,
                user_question,
                chatbot,
                token_count,
                top_p,
                temperature,
                debug

            ],
            outputs=[chatbot, history, status_display, token_count],
            show_progress=True,
        )

        end_outputing_args = dict(
            fn=end_outputing, inputs=[], outputs=[user_input, submitBtn]
        )

        reset_textbox_args = dict(
            fn=reset_textbox, inputs=[], outputs=[user_input]
        )

        user_input.submit(**transfer_input_args).then(**
                                                      chatgpt_predict_args).then(**end_outputing_args)

        submitBtn.click(**transfer_input_args).then(**
                                                    chatgpt_predict_args).then(**end_outputing_args)

        creat_chat_args = dict(
            fn=read_template_create_chat, inputs=[chat_info, role_selected, temperature, top_p, role_cards, templateSelectDropdown,
                                                  systemPromptTxt, chatbot], outputs=[chat_info, systemPromptTxt, chatbot, history]
        )

        emptyBtn.click(
            reset_state,
            outputs=[chatbot, history, token_count, status_display],
            show_progress=True,
        ).then(show_progress=True, **creat_chat_args)
        emptyBtn.click(**reset_textbox_args)

        # ChatGPT
        keyTxt.change(submit_key, keyTxt, [user_api_key, status_display])

        # 重新获取所有模板
        get_all_templates_args = dict(
            fn=get_templates, inputs=[role_cards], outputs=[
                templateSelectDropdown]
        )

        templateRefreshBtn.click(**get_all_templates_args)
        # 选择文件
        templateSelectDropdown.change(
            show_progress=True, **creat_chat_args
        )

        savePromptBtn.click(
            change_prompt, [systemPromptTxt, role_cards], [role_cards]).then(
            **get_all_templates_args
        )

        # S&L
        saveHistoryBtn.click(
            save_chat_history,
            [saveFileName, systemPromptTxt, history, role_selected, user_name],
            show_progress=True,
        )

        # TODO 暂时不让用户加载历史记录，因为从文本文件中完全恢复状态比较困难，暂时不做。
        # saveHistoryBtn.click(get_history_names, [gr.State(
        #     False), user_name], [historyFileSelectDropdown])

        # historyRefreshBtn.click(get_history_names, [gr.State(
        #     False), user_name], [historyFileSelectDropdown])
        # historyFileSelectDropdown.change(
        #     load_chat_history,
        #     [historyFileSelectDropdown, systemPromptTxt,
        #         history, chatbot, user_name],
        #     [saveFileName, systemPromptTxt, history, chatbot],
        #     show_progress=True,
        # )
        downloadFile.change(
            load_chat_history,
            [downloadFile, systemPromptTxt, history, chatbot, user_name],
            [saveFileName, systemPromptTxt, history, chatbot],
        )

        # Advanced
        default_btn.click(
            reset_default, [], [top_p, temperature, status_display], show_progress=True
        )
    return demo


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    demo = creat_gui_chat()
    demo.launch()

# role_selected = role_list[0]
# demo = creat_chat(roles[role_selected])
# demo.launch()
