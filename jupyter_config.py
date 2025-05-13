"""
根据官方文档提示新建该 config 文件，用于修改 Jupyter-ai 中 Chat 的 Help 提示信息
"""
c.AiExtension.help_message_template = """
Hi～你好！ 我是编程助手。\n
\n
你可以在下面的文本框中向我提问，也可以使用以下命令：\n
\n
• /ask — 根据使用/learn命令学习到的数据内容，使用/ask进行提问。\n
• /clear — 清空聊天窗口。 \n
• /generate — 根据文本提示语，生成新的 Jupyter notebook 页面(消耗资源较多，结果生成较慢！！) \n
• /learn — 让编程助手 学习你系统中的文件(文件路径要写绝对路径，如果使用通配符生成结果较慢！！) \n
. /learn -d/-c/-o/-a 删除学习内容/自定义块大小/自定义块重叠值/学习目录所有文件(会变慢！！详情见 Readme.md)
• /export — 将聊天记录导出为一个Markdown格式的文件 \n
• /fix — 修复右侧notebook 的 cell 中选定的错误单元格 \n
• /help — 显示帮助信息 \n
\n
如果你需要了解 Jupyter AI 更多功能使用方法或者其他功能需求，请联系xxx。\n
""".strip()