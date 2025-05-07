from typing import Any, Dict, Iterator, List, Mapping, Optional, TYPE_CHECKING, cast, Union

from jupyter_ai import AiExtension, _jupyter_server_extension_points
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
import json
from jupyter_ai_magics import BaseProvider
from openai import OpenAI
from langchain.chat_models.base import BaseChatModel

from langchain_core.messages import BaseMessage, AIMessage, AIMessageChunk
from langchain_core.outputs import ChatGeneration, LLMResult, ChatResult


# 接收 jupyter-lab 界面聊天框内容信息
class ChatLLM(BaseChatModel):
    # print('进入serverLLM中了————————————————————————————')

    def _generate(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> ChatResult:
        # print("进入_generate模块*************")
        # print("messages*************", messages)
        last_message = messages[-1]
        # print("last_message*************", last_message)
        msg = last_message.content[:]
        # print("最终传入信息为：_______", msg)
        result = ''
        if self.model_id == "deepseek-r1:7b":
            #print('输入数据为：', msg)
            client = OpenAI(
                base_url='http://localhost:11434/v1',
                api_key="not-needed",
            )
            # print('实例化客户端---------')
            completion = client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {"role": "system", "content": "你是一个可以辅助代码也可以聊天的通用机器人"},
                    {"role": "user", "content": msg}
                ],
                stream=False)
            # print('实例化complition----------')
            res = completion.model_dump_json(indent=2)
            # print('加载成 json 格式', res)
            result = json.loads(res)["choices"][0]["message"]["content"]
            #print('AI 回答的结果是：___________', result)
        message = AIMessageChunk(content=result)
        # message = AIMessage(content=result)
        # print("最终的message*************", message)
        # generation = ChatGeneration(message=message)
        generation = ChatGeneration(text=result, message=message)
        # print("最终的会话生成为***********：", ChatResult(generations=[generation]))
        return ChatResult(generations=[generation])

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return a dictionary of identifying parameters."""
        return {"model_name": "deepseek-r1:7b", }

    @property
    def _llm_type(self) -> str:
        return "deepseek-r1:7b"


class MyProvider(BaseProvider, ChatLLM):
    # print('已进入类MyProvider中————————————----')
    id = "my_provider"
    name = "My Provider"
    models = ["deepseek-r1:7b"]
    model_id_key = "model"

    # print('准备进行 init')

    def __init__(self, **kwargs):
        kwarg_dict = kwargs
        # print('打印变量接受 1', kwarg_dict.keys())
        # print('打印变量接受 2', kwarg_dict.values())
        model_id = kwargs.get("model_id")
        llm = ChatLLM(model_id=model_id)
        # print("llm返回结果——————————————", llm)
        super().__init__(**kwargs)