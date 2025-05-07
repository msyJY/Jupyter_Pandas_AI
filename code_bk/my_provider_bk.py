"""
author:msy
实现 Jupyterlab 中Notebook 的 Cell 里调用 Jupyter-ai 功能，使用本地大模型服务。
"""
from typing import Any, Dict, Iterator, List, Mapping, Optional, TYPE_CHECKING, cast, Union
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
import json
from jupyter_ai_magics import BaseProvider
from openai import OpenAI
from langchain.chat_models.base import BaseChatModel

from langchain_core.messages import BaseMessage, AIMessage, AIMessageChunk
from langchain_core.outputs import ChatGeneration, LLMResult, ChatResult


# 接收 jupyter-lab 界面聊天框内容信息
class serverLLM(BaseChatModel):

    def _generate(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> ChatResult:
        last_message = messages[-1]
        msg = last_message.content[:]
        # print("最终传入信息为：_______", msg)
        result = ''
        if self.model_id == "local-model":
            print('输入数据为：', msg)
            client = OpenAI(
                base_url='http://localhost:8000/v1',
                api_key="not-needed",
            )
            completion = client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {"role": "system", "content": "你是一个可以辅助代码也可以聊天的通用机器人"},
                    {"role": "user", "content": msg}
                ],
                stream=False)
            res = completion.model_dump_json(indent=2)
            result = json.loads(res)["choices"][0]["message"]["content"]
            print('AI 回答的结果是：___________', result)
        message = AIMessageChunk(content=result)
        generation = ChatGeneration(text=result, message=message)
        return ChatResult(generations=[generation])

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return a dictionary of identifying parameters."""
        return {"model_name": "local-model", }

    @property
    def _llm_type(self) -> str:
        return "local-model"


class MyProvider(BaseProvider, serverLLM):
    id = "my_provider"
    name = "My Provider"
    models = ["local-model"]
    model_id_key = "model"


    def __init__(self, **kwargs):
        model_id = kwargs.get("model_id")
        llm = serverLLM(model_id=model_id)
        super().__init__(**kwargs)
