"""
author:msy
优化功能:
1 Chat 聊天框中通过关键字调用功能时，将该功能的描述信息使用中文显示在聊天框中
2 Chat 中配置Language 和 Embedding 模型时，只显示配置的能用模型服务
"""

from jupyter_ai import AiExtension
from traitlets import List, Unicode


class CustomAiExtension(AiExtension):
    """自定义Chat 部分配置模型列表，下拉只显示配置的能用模型"""

    print("进入重写后的CustomAiExtension中*******")
    # 1. 覆盖父类的默认配置
    allowed_providers = List(
        Unicode(),
        default_value=["my_provider", "my_emb_provider"],  # 只允许自定义提供商
        help="Identifiers of allowlisted providers. If `None`, all are allowed",
        config=True
    )

    # 3. 可选：重写初始化方法添加自定义逻辑
    def initialize_settings(self):
        # 先调用父类初始化
        super().initialize_settings()

        # 添加您的自定义初始化逻辑
        self.log.info("重新自定义模型列表完成")


from jupyter_ai.chat_handlers.ask import AskChatHandler
from jupyter_ai.chat_handlers.clear import ClearChatHandler
from jupyter_ai.chat_handlers.export import ExportChatHandler
from jupyter_ai.chat_handlers.fix import FixChatHandler
from jupyter_ai.chat_handlers.generate import GenerateChatHandler
from jupyter_ai.chat_handlers.help import HelpChatHandler
from jupyter_ai.chat_handlers.learn import LearnChatHandler


# /ask
class ZhAskChatHandler(AskChatHandler):
    help = "根据已学习的数据内容进行提问(使用/learn学习)"  # 自定义帮助信息

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# /clear
class ZhClearChatHandler(ClearChatHandler):
    help = "清屏"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# /export
class ZhExportChatHandler(ExportChatHandler):
    help = "将历史记录导出为 Markdown 格式的文件"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# /fix
class ZhFixChatHandler(FixChatHandler):
    help = "修复你在 Notebook 中选中的 Cell 存在的错误"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# /generate
class ZhGenerateChatHandler(GenerateChatHandler):

    help = "根据一段自然语言描述生成 Jupyter Notebook 文件"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# /help
class ZhHelpChatHandler(HelpChatHandler):

    help = "展示帮助信息"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# /learn
class ZhLearnChatHandler(LearnChatHandler):

    help = "让代码助手学习你上传的文件数据(使用/ask 提问)"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)