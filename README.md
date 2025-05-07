# Jupyter_Pandas_AI
## Jupyter_AI  个人优化适配部分主要包含：
1. Language Model 和 Embedding Model 调用本地模型服务

2. Jupyterlab 中 Notebook 的 Cell 部分增加流式输出
3.  Jupyter-ai 左侧 Chat 的/help 显示为中文
   


## Pandas-ai 个人优化适配部分主要包含：

1. Pandas-ai 调用本地模型服务

2. 将 Pandas-ai 功能的调用封装成 Jupyterlab 中 Notebook 部分的 magic 功能(其实是 ipython 的 magic 功能)

   

## 解释说明：

1. 如果有适配 Jupyter-ai 到本地的需求，务必先看官方文档，下载官方代码后，再将该项目代码放在 Jupyter-ai 目录下即可
2. `code_bk`目录下存放的是`Jupyter-ai`在 Notebook 的 Cell 中被调用输出流式/非流式，以及 Pandas-ai 的一些测试用例
3. `msy_packages`下放置的为调用本地语言模型适配代码以及 toml 文件
4. `msy_packages1 `下放置的为调用本地Eembdding模型适配代码以及 toml 文件
5. `rewrite_code`目录下放置的是针对 Pandas-ai 功能的一些适配优化代码文件
6. Jupyter-AI原项目地址：https://github.com/jupyterlab/jupyter-ai
   Jupyter-AI原项目官方文档：https://jupyter-ai.readthedocs.io/en/latest/
7. Pandas-AI 原项目地址：https://github.com/sinaptik-ai/pandas-ai
8. Pandas-AI 原项目官方文档：https://docs.getpanda.ai/v2/intro
9. 注：如果需要省去每次使用 ipython 中 magic 包初始化指令如`%load_ext jupyter_ai_magics`，可以生成 ipython 文件即`ipthon_config.py`，使用项目中同名文件替换，注意生成文件位置，确保生效



## 版本

`Jupyter-ai`：2.22.0

`jupyter_ai_magics`:2.22.0

`Jupyterlab`:4.2.5

`python`:3.10.16

`pandasai`:2.4.2



## 其他

1. 当前为 demo 版本，有问题可以 issue 我看到后会进行解答
