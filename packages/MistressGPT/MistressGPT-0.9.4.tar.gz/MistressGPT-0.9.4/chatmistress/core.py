import copy
from pathlib import Path
from typing import Dict, List, Optional, Union
import click
import xmltodict
import json
import yaml
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import (
    ConversationSummaryBufferMemory,
    ChatMessageHistory,
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
    ConversationSummaryMemory,
    ConversationKGMemory)
from langchain.output_parsers import (OutputFixingParser, PydanticOutputParser,
                                      RetryWithErrorOutputParser)
from langchain.schema import HumanMessage, AIMessage
from langchain import PromptTemplate, OpenAI
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory, FileHistory
from langchain.chains.llm import LLMChain
from pydantic import BaseModel, Field
from rich.console import Console
from .utils import fetch_template, load_roles, RoleInfo


class DummyConsole:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        pass

    def status(self, message):
        return self


class Response(BaseModel):
    pose: str = Field(description="姿势描述")
    line: str = Field(description="台词")


class ConversationMySummaryBufferWindowMemory(ConversationBufferWindowMemory):
    other_input_keys: List[str] = []
    sum_chain: LLMChain
    llm: ChatOpenAI
    mistress_name: str
    user_role: str
    existing_summary: str = ''
    max_token_limit: int = 1000
    debug: bool = False
    # parser: PydanticOutputParser = parser

    @property
    def memory_variables(self) -> List[str]:
        return [self.memory_key] + self.other_input_keys

    def summrize_lines(self):
        buffer = self.chat_memory.messages
        curr_buffer_length = self.llm.get_num_tokens_from_messages(buffer)
        if self.debug:
            print(
                f"len(buffer)={len(buffer)}, curr_buffer_length={curr_buffer_length}")
        if curr_buffer_length > self.max_token_limit:
            pruned_memory = []
            while curr_buffer_length > self.max_token_limit:
                pruned_memory.append(buffer.pop(0))
                curr_buffer_length = self.llm.get_num_tokens_from_messages(
                    buffer)

            history_str = []
            for i, m in enumerate(pruned_memory):
                if type(m) == HumanMessage:
                    who = self.user_role
                    content = copy.deepcopy(m.content)
                    pass
                elif type(m) == AIMessage:
                    who = self.mistress_name
                    content = copy.deepcopy(m.content)
                    try:
                        content = xmltodict.parse(content)[
                            'res']['line']
                    except:
                        pass
                history_str.append(f"{who}:{content}")

            history_str = '\n'.join(history_str)
            self.existing_summary = self.sum_chain.predict(
                summary=self.existing_summary, new_lines=history_str)


def gen_summarize_template(mistress_name, mistress_role, user_role, story_settings):
    string_prefix = ""
    string_suffix = ""
    gotosuffix = False
    with open(Path(__file__).parent / 'templates/role_play_summary.txt', 'r', encoding="utf-8") as f:
        for line in f:
            if line == '==========\n':
                gotosuffix = True
                continue
            if gotosuffix is False:
                string_prefix += line
            else:
                string_suffix += line

    string_prefix = string_prefix.format(mistress_name=mistress_name,
                                         mistress_role=mistress_role,
                                         user_role=user_role,
                                         story_settings=story_settings)

    summarize_template = string_prefix + string_suffix

    return summarize_template


def gen_sys_template(
        mistress_name: str, mistress_role: str, user_role: str, user_nickname: str, user_description: str, story_settings: str, tasks: list):
    string_prefix = ""
    with open(Path(__file__).parent / 'templates/role_play_sys.txt', 'r', encoding="utf-8") as f:
        for line in f:
            string_prefix += line

    return string_prefix.format(mistress_name=mistress_name,
                                mistress_role=mistress_role,
                                user_role=user_role,
                                user_nickname=user_nickname,
                                user_description=user_description,
                                story_settings=story_settings,
                                tasks=",".join(tasks)
                                ) + "\nBelow is对话总结:\n{summary}\n" + "\nBelow is最近对话记录:\n{history}\n" + f"{user_role}:" + "{input}\n" + f"{mistress_name}:"


def init_chat_components(role_info: RoleInfo, temperature, top_p, max_token_limit, debug=False):
    parser = PydanticOutputParser(pydantic_object=Response)
    llm = ChatOpenAI(temperature=temperature, top_p=top_p)
    # set up model
    system_template = gen_sys_template(
        role_info.mistress_name, role_info.mistress_role, role_info.user_role,
        role_info.user_nickname, role_info.user_description, role_info.story_settings,
        role_info.mistress_tasks)
    #  =============  summarize part ==============

    sum_chain = LLMChain(
        llm=OpenAI(temperature=temperature, top_p=top_p),
        prompt=PromptTemplate(
            input_variables=["summary", "new_lines"],
            template=gen_summarize_template(
                role_info.mistress_name, role_info.mistress_role, role_info.user_role, role_info.story_settings)
        ), verbose=debug)

    prompt = PromptTemplate(
        input_variables=["history", "input", "summary"], template=system_template
    )

    memory = ConversationMySummaryBufferWindowMemory(
        human_prefix=role_info.user_role,
        ai_prefix=role_info.mistress_name,
        memory_key="history",
        other_input_keys=['summary'],
        sum_chain=sum_chain,
        llm=llm,
        max_token_limit=max_token_limit,
        mistress_name=role_info.mistress_name,
        user_role=role_info.user_role,
        debug=debug,
        k=100,
    )
    conversation = ConversationChain(
        memory=memory, prompt=prompt, llm=llm, verbose=debug)

    fix_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
    retry_parser = RetryWithErrorOutputParser.from_llm(parser=parser, llm=llm)
    return conversation, prompt, memory, parser, fix_parser, retry_parser


def parse_llm_output(output, parser, fix_parser, retry_parser, prompt_value: str):
    try:
        output = json.dumps(xmltodict.parse(output)['res'], ensure_ascii=False)
        parsed_response = parser.parse(output)
    except:
        print('发生错误，再次解析')
        # avoid using retry_parser.
        # parsed_response = retry_parser.parse_with_prompt(
        #     output, prompt_value)
        parsed_response = fix_parser.parse(output)

    return parsed_response


def interact(
        conversation: ConversationChain, user_input: str,
        prompt: PromptTemplate, memory: ConversationMySummaryBufferWindowMemory,
        parser: PydanticOutputParser, fix_parser: OutputFixingParser, retry_parser: RetryWithErrorOutputParser,
        console: Optional[Union[Console, DummyConsole]] = None,
        debug: bool = False,
        top_p: Optional[float] = None,
        temperature: Optional[float] = None,
        openai_api_key: Optional[str] = None,
):
    if console is None:
        console = DummyConsole()

    if top_p is not None:
        conversation.llm.model_kwargs['top_p'] = top_p
        conversation.memory.sum_chain.llm.top_p = top_p
    if temperature is not None:
        conversation.llm.model_kwargs['temperature'] = temperature
        conversation.memory.sum_chain.llm.temperature = temperature
    if openai_api_key is not None:
        conversation.llm.openai_api_key = openai_api_key
        conversation.memory.sum_chain.llm.openai_api_key = openai_api_key

    with console.status("loading..."):
        res = conversation.predict(
            input=user_input, summary=memory.existing_summary)
        if debug:
            print(f"original response: {res}")

        prompt_value = prompt.format_prompt(
            input=user_input,
            history=memory.load_memory_variables({})['history'],
            summary=memory.existing_summary,
        )
    parsed_response = parse_llm_output(
        res, parser, fix_parser, retry_parser, prompt_value)

    return parsed_response
