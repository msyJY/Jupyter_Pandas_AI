from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np

# 初始化 FastAPI 应用
app = FastAPI()

# 加载 Embedding 模型
model = SentenceTransformer('./all-MiniLM-L6-v2')

# 定义请求体格式（兼容 OpenAI 的 Embedding API）
class EmbeddingRequest(BaseModel):
    input: str | list[str]
    model: str = "all-MiniLM-L6-v2"  # 默认模型名称

# 定义响应体格式（兼容 OpenAI 的 Embedding API）
class EmbeddingResponse(BaseModel):
    object: str = "list"
    data: list[dict]
    model: str
    usage: dict

# Embedding 接口
@app.post("/v1/embeddings", response_model=EmbeddingResponse)
async def create_embedding(request: EmbeddingRequest):
    try:
        # 生成 Embedding
        if isinstance(request.input, str):
            sentences = [request.input]
        else:
            sentences = request.input

        embeddings = model.encode(sentences)

        # 构造 OpenAI 兼容的响应
        response_data = [
            {
                "object": "embedding",
                "embedding": embedding.tolist(),  # 将 numpy 数组转换为列表
                "index": i,
            }
            for i, embedding in enumerate(embeddings)
        ]

        return EmbeddingResponse(
            object="list",
            data=response_data,
            model=request.model,
            usage={
                "prompt_tokens": sum(len(sentence.split()) for sentence in sentences),
                "total_tokens": sum(len(sentence.split()) for sentence in sentences),
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 启动服务
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
