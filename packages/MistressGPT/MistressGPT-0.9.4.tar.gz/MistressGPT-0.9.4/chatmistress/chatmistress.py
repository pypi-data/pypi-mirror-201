import os
from typing import Dict, List, Optional, Union

import click
from dotenv import load_dotenv
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from rich.console import Console

from .core import init_chat_components, interact
from .utils import RoleInfo, fetch_template, load_roles
from .webbot2 import creat_gui_chat

load_dotenv()


def launch_cli_chat(
        role_info: RoleInfo, session: PromptSession,
        res_completer: WordCompleter, console: Console, temperature=0.5, top_p=1, max_token_limit=200,
        init_user_input='您好',
        debug=False):
    conversation, prompt, memory, parser, fix_parser, retry_parser = init_chat_components(
        role_info, temperature, top_p, max_token_limit, debug=debug)

    parsed_response = interact(conversation, init_user_input,
                               prompt, memory, parser, fix_parser, retry_parser,
                               console=console, debug=debug)
    i = 0
    while True:
        i += 1
        console.print(f"{role_info.mistress_name} ({parsed_response.pose}):",
                      parsed_response.line, sep="\n", style="magenta")
        if debug:
            user_input = '我今天早上出门之前吃了两个苹果' * 20
        else:
            user_input = session.prompt('我: ', completer=res_completer)

        if user_input == '!switch':
            return False
        if user_input == '!exit':
            return True
        elif user_input.startswith('~'):
            user_input = user_input[1:]

        parsed_response = interact(conversation, user_input,
                                   prompt, memory, parser, fix_parser, retry_parser,
                                   console=console, debug=debug)

        memory.summrize_lines()


@click.command()
@click.argument('cmd', type=click.Choice(['cli', 'gui']))
@click.option('--debug', default=False, help='Debug mode if True')
@click.option('--max-token-limit', default=1000, help='temperature for openai')
@click.option('--ext-url', default=None, help='外部模板URL')
@click.option('--concurrency', default=20, help='外部模板URL')
def main(cmd, debug, max_token_limit, ext_url, concurrency):
    assert cmd in ('cli', 'gui')

    if 'OPENAI_API_KEY' not in os.environ:
        os.environ['OPENAI_API_KEY'] = input(
            'OPENAI_API_KEY 环境变量未设置, 请输入你的OPENAI_API_KEY: ')

    if ext_url is not None:
        roles: Dict[str, RoleInfo] = fetch_template(ext_url)
    else:
        roles: Dict[str, RoleInfo] = load_roles()
    if debug:
        max_token_limit = 200

    if cmd == 'gui':
        gui = creat_gui_chat(roles, debug=debug,
                             max_token_limit=max_token_limit)
        gui.queue(concurrency_count=concurrency).launch(inbrowser=True)

    elif cmd == 'cli':
        console = Console()
        session = PromptSession(history=FileHistory('./.role_play_history'))
        res_completer = WordCompleter([
            '!switch',
            '!exit',
            '~是，主人',
            '~抱歉主人',
            '~都听您的',
        ])
        exited = False
        while not exited:
            role_list = [k for k in roles.keys()]
            if len(role_list) > 1:
                print(
                    f'选择你的主人: {", ".join([f"{i}: {k}" for i, k in enumerate(role_list)])}')
                if debug:
                    role_selected = role_list[0]
                else:
                    role_selected = role_list[int(
                        session.prompt('我想要 (请输入数字): ').strip())]
            else:
                role_selected = role_list[0]

            print(f'你选择了{role_selected}作为你的主人. 请按照提示进行对话.')
            exited = launch_cli_chat(roles[role_selected],
                                     session, res_completer, console, debug=debug, max_token_limit=max_token_limit)

        print('Bye~')


if __name__ == "__main__":
    main()

# roles: Dict[str, RoleInfo] = load_roles()
# debug = True
# max_token_limit = 1000
# demo = creat_gui_chat(
#     roles, debug=debug, max_token_limit=max_token_limit)
# if __name__ == "__main__":
#     demo.launch()
