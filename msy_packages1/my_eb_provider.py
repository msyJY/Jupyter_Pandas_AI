from typing import Any, Dict, List, Optional, Union
from jupyter_ai_magics import BaseEmbeddingsProvider
import requests


class MyEmbProvider(BaseEmbeddingsProvider):
    """自定义 embedding 提供者，基于本地 FastAPI 部署的 embedding 服务。"""

    id = "my_emb_provider"
    name = "My Embedding Provider"
    models = ["all-MiniLM-L6-v2", "another-model"]  # 支持的模型列表
    model_id_key = "model"  # 模型 ID 的参数名称

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # 初始化 BaseEmbeddingsProvider
        print(kwargs)
        self.base_url = kwargs.get("base_url", "http://localhost:8001/v1")
        self.model_id = kwargs.get("model_id", "all-MiniLM-L6-v2")  # 默认模型 ID
        self.headers = {
            "Content-Type": "application/json",
        }

        # 检查模型 ID 是否在支持的模型列表中
        if self.model_id not in self.models:
            raise ValueError(f"Model ID '{self.model_id}' is not supported. Supported models: {self.models}")

    def _call_api(self, payload: Dict[str, Any]) -> List[float]:
        """Helper method to call the local FastAPI embedding service."""
        url = f"{self.base_url}/embeddings"
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]  # 提取 embedding 向量

    def embed_query(self, text: str) -> List[float]:
        """将单个文本转换为 embedding 向量。"""
        print("query*******")
        payload = {
            "input": text,
            "model": self.model_id,  # 使用前端选择的模型 ID
        }
        print("self._call_api(payload) ***********", self._call_api(payload))
        return self._call_api(payload)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        print("documents*******")
        """批量将文本列表转换为 embedding 向量列表。"""
        payload = {
            "input": texts,
            "model": self.model_id,  # 使用前端选择的模型 ID
        }
        url = f"{self.base_url}/embeddings"
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return [item["embedding"] for item in response.json()["data"]]

    def __call__(self, input: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """使 MyEmbProvider 的实例可调用，支持单个文本和批量文本。"""
        if isinstance(input, str):
            return self.embed_query(input)
        elif isinstance(input, list):
            return self.embed_documents(input)
        else:
            raise TypeError("Input must be a string or a list of strings.")