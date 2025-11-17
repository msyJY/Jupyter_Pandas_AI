# Jupyter_Pandas_AI

<img src="/Users/gedun/github_testcode/Jupyter_Pandas_AI/Jupyter_Pandas_AI/pic/image-20251117160732144.png" alt="image-20251117160732144" style="zoom:25%;" />

<img src="/Users/gedun/github_testcode/Jupyter_Pandas_AI/Jupyter_Pandas_AI/pic/image-20251117160926490.png" alt="image-20251117160926490" style="zoom:25%;" />

<img src="/Users/gedun/github_testcode/Jupyter_Pandas_AI/Jupyter_Pandas_AI/pic/image-20251117114532233.png" alt="image-20251117114532233" style="zoom:25%;" />

<img src="/Users/gedun/github_testcode/Jupyter_Pandas_AI/Jupyter_Pandas_AI/pic/image-20251117114425539.png" alt="image-20251117114425539" style="zoom:25%;" />

<img src="/Users/gedun/github_testcode/Jupyter_Pandas_AI/Jupyter_Pandas_AI/pic/image-20251117160540640.png" alt="image-20251117160540640" style="zoom:25%;" />

<img src="/Users/gedun/github_testcode/Jupyter_Pandas_AI/Jupyter_Pandas_AI/pic/image-20251117161606747.png" alt="image-20251117161606747" style="zoom:25%;" />

<img src="/Users/gedun/github_testcode/Jupyter_Pandas_AI/Jupyter_Pandas_AI/pic/image-20251117161218252.png" alt="image-20251117161218252" style="zoom:25%;" />

## Jupyter_AI  个人优化适配(20251117)部分主要包含：
1. Chat：Language Model 和 Embedding Model 适配调用本地模型服务且只显示本地模型

2. Chat：增加Chat 部分使用所有功能为流式输出
3. Chat:   进入后/help 显示为中文，更换助手名称和用户名称
4. Chat：优化/lean 功能使用为按钮的形式，且限定上传文件路径为 Jupyterlab 工作区
5. Chat:   新增"上下文" 功能，一键使用，且限定上传文件路径为 Jupyterlab 工作区
6. Chat:   对自由对话和 ask 等功能实现"追问"功能
7. Notebook:  Jupyter-ai 默认启动命令封装到自启动中
8. Notebook:  设置Notebook 部分默认使用模型
9. Notebook:(随缘更新) 设计 Notebook 的 shell 中新增"代码补全"功能(需微调一个代码模型)
10. Chat 待新增功能(随缘更新)： mcp 功能
11. Chat 待新增功能(随缘更新)： 多 role 适配



## Pandas-ai 个人优化适配部分主要包含：

1. Pandas-ai 调用本地模型服务

2. 将 Pandas-ai 功能的调用封装成 Jupyterlab 中 Notebook 部分的 magic 功能(其实是 ipython 的 magic 功能)

   

## 解释说明：

1. 如果有适配 Jupyter-ai 到本地的需求，务必先看官方文档，下载官方代码后，再将该项目代码放在 Jupyter-ai 目录下即可
2. `code_bk`目录下存放的是`Jupyter-ai`在 Notebook 的 Cell 中被调用输出流式/非流式，以及 Pandas-ai 的一些测试用例
3. `msy_packages`下放置的为调用本地语言模型适配代码以及 toml 文件
4. `msy_packages1 `下放置的为调用本地Eembdding模型适配代码以及 toml 文件
5. `rewrite_code`目录下放置的是针对 Pandas-ai 功能的一些适配优化代码文件
6. `model` 目录下放了 embedding 模型和启动文件，Language 语言模型个人使用的是 ollama 模型服务，执行安装测试即可
7. `node_modules` 目录主要存放的是前端重构后更新的前端代码和依赖包
8. `run.py` 可以作为测试用的启动文件，可以不每次需要测试都使用`Jupyter lab`命令
9. Jupyter-AI原项目地址：https://github.com/jupyterlab/jupyter-ai
   Jupyter-AI原项目官方文档：https://jupyter-ai.readthedocs.io/en/latest/
10. Pandas-AI 原项目地址：https://github.com/sinaptik-ai/pandas-ai
11. Pandas-AI 原项目官方文档：https://docs.getpanda.ai/v2/intro
12. 注：如果需要省去每次使用 ipython 中 magic 包初始化指令如`%load_ext jupyter_ai_magics`，可以生成 ipython 文件即`ipthon_config.py`，使用项目中同名文件替换，注意生成文件位置，确保生效
13. 注意如果需要重构前端文件，下载本地项目直接 build 即可，但是如果需要修改后端服务需要更改 Jupyter-ai 包对应 py 文件，不然无法生效(也可以换个方式自行实现)
14. mcp 和多 role 功能可以参考 Jupyter-ai 中 beta 未发布版本



## 版本

`Jupyter-ai`：2.22.0

`jupyter_ai_magics`:2.22.0

`Jupyterlab`:4.2.5

`python`:3.10.16

`pandasai`:2.4.2



## 其他

1. 当前为 demo 版本，有问题可以 issue 我看到后会进行解答

修改模型下拉列表：
extension 中允许供应商列表添加

提示内容变成中文：
chat_handlers下，文件 help 部分修改
