from typing import Any, Dict, List, Optional, AsyncIterator
from jupyter_ai_magics import BaseProvider
from langchain_core.callbacks.manager import (
    CallbackManagerForLLMRun,
    AsyncCallbackManagerForLLMRun
)
from langchain.chat_models.base import BaseChatModel
from langchain_core.messages import (
    BaseMessage,
    AIMessage,
    AIMessageChunk,
    SystemMessage,
    HumanMessage
)
from langchain_core.outputs import ChatGeneration, ChatResult, ChatGenerationChunk
from openai import OpenAI, AsyncOpenAI
import json


class ChatLLM(BaseChatModel):
    def _generate(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> ChatResult:
        print("*********已进入 generate 函数中********")
        # msg = messages[-1].content
        # 构建历史记录
        conversation = [
            {"role": "system", "content": "你是一个可以辅助代码也可以聊天的通用机器人"}
        ]
        for msg in messages:
            if isinstance(msg, HumanMessage):
                conversation.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                conversation.append({"role": "assistant", "content": msg.content})
        print("conversation长度**********", len(conversation))

        result = ''

        if self.model_id in self.models:
            client = OpenAI(
                base_url='http://localhost:11434/v1',
                api_key="not-needed",
            )
            completion = client.chat.completions.create(
                model=self.model_id,
                messages=conversation,
                stream=False
            )
            result = completion.choices[0].message.content

        return ChatResult(generations=[ChatGeneration(
            message=AIMessage(content=result)
        )])

    async def _astream(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        print("*********已进入 _astream 函数中********")
        # msg = messages[-1].content
        # 构建完整对话历史
        conversation = [
            {"role": "system", "content": "你是一个可以辅助代码也可以聊天的通用机器人"}
        ]
        for msg in messages:
            if isinstance(msg, HumanMessage):
                conversation.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                conversation.append({"role": "assistant", "content": msg.content})

        print("conversation**********", conversation)

        if self.model_id in self.models:
            client = AsyncOpenAI(
                base_url='http://localhost:11434/v1',
                api_key="not-needed",
            )
            completion = await client.chat.completions.create(
                model=self.model_id,
                messages=conversation,
                stream=True
            )

            async for chunk in completion:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield ChatGenerationChunk(
                        message=AIMessageChunk(content=chunk.choices[0].delta.content)
                    )

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {"model_name": self.model_id}

    @property
    def _llm_type(self) -> str:
        return self.model_id


class MyProvider(BaseProvider, ChatLLM):
    id = "my_provider"
    name = "My Provider"
    models = ["deepseek-r1:7b", "qwen2-custom:latest"]
    model_id_key = "model"

    def __init__(self, **kwargs):
        model_id = kwargs.get("model_id")
        llm = ChatLLM(model_id=model_id, models=self.models)
        super().__init__( **kwargs)