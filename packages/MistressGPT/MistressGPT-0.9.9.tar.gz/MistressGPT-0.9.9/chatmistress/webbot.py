import gradio as gr
from chatmistress.core import init_chat_components, interact
from chatmistress.utils import RoleInfo


def creat_gui_chat(role_info: RoleInfo, init_user_input="hi",
                   temperature=0.7,
                   max_token_limit=2000,
                   debug=False,
                   ):
    conversation, prompt, memory, parser, fix_parser, retry_parser = init_chat_components(
        role_info, temperature, max_token_limit, debug=debug)

    init_response = interact(
        conversation, init_user_input, prompt, memory, parser, fix_parser,
        retry_parser, debug=debug)

    def add_text(history, text):
        history = history + [(text, None)]
        return history, ""

    def bot(history):
        user_input = history[-1][0].strip()

        parsed_response = interact(
            conversation, user_input, prompt, memory, parser, fix_parser,
            retry_parser, debug=debug)
        history[-1][1] = f'({parsed_response.pose}): {parsed_response.line}'
        return history

    with gr.Blocks() as demo:
        chatbot = gr.Chatbot([
            (None, f'({init_response.pose}): {init_response.line}')
        ], elem_id="chatbot",
            label=role_info.mistress_name).style(height=750)

        with gr.Row():
            with gr.Column(scale=1.0):
                info_after_chat = f'输入文字然后Enter'
                txt = gr.Textbox(
                    label=role_info.user_role,
                    show_label=False,
                    placeholder=info_after_chat,
                ).style(container=False)

        txt.submit(add_text, [chatbot, txt], [chatbot, txt]).then(
            bot, chatbot, chatbot
        )
        # mistress_selection.change(change_role, [mistress_selection])

    return demo


# role_selected = role_list[0]
# demo = creat_chat(roles[role_selected])
# demo.launch()
