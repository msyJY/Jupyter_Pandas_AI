from IPython.core.magic import Magics, magics_class, cell_magic, line_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from pandas import DataFrame
from pandasai import SmartDataframe, SmartDatalake
from pandasai.llm.local_llm import LocalLLM
import pandas as pd
import matplotlib.pyplot as plt
from typing import Union, Optional, Dict, Any, List, Type, Callable
import warnings
from IPython import get_ipython
from Rewrite_code.Rewrite_pandas_ai_ import CustomAgent
from pandasai.skills import skill
from pandasai.connectors import PandasConnector
from IPython.display import Markdown, display
import ast


class PandasAIError(Exception):
    """Base exception for all Pandas-AI magic errors"""
    pass


class EnvironmentError(PandasAIError):
    """环境配置异常"""

    def __init__(self, missing: Optional[str] = None):
        msg = "需要Jupyter/IPython环境"
        if missing:
            msg += f"，缺少依赖: {missing}"
        super().__init__(msg)


class VisualizationError(PandasAIError):
    """图形渲染异常"""

    def __init__(self, result: Any):
        if isinstance(result, type):
            msg = f"无法显示类型: {result.__name__}"
        else:
            msg = f"无法显示对象: {type(result).__name__} ({str(result)[:50]}...)"
        super().__init__(msg)


@magics_class
class PandasAIMagics(Magics):
    def __init__(self, shell: Any):
        super().__init__(shell)
        self._init_environment()
        self._instances: Dict[str, Any] = {}  # 存储所有实例
        self._current_key: Optional[str] = None
        self._last_query: Optional[str] = None
        self._last_result: Optional[Any] = None

    def _init_environment(self) -> None:
        """初始化运行环境"""
        self._verify_ipython()
        self._configure_matplotlib()

    def _verify_ipython(self) -> None:
        """验证IPython环境"""
        if not hasattr(self, 'shell'):
            raise EnvironmentError()
        if not hasattr(get_ipython(), 'run_cell'):
            raise EnvironmentError("需要交互式 IPython 环境")

    def _configure_matplotlib(self) -> None:
        """配置Matplotlib"""
        try:
            self.shell.run_line_magic('matplotlib', 'inline')
            plt.ioff()
        except Exception as e:
            warnings.warn(f"Matplotlib配置失败: {str(e)}")

    def _get_dataframes(self, df_names: List[str]) -> Dict[Any, DataFrame]:
        """获取DataFrame集合"""
        dfs_dict: Dict[Any, DataFrame] = {}
        for df_name in df_names:
            df = self.shell.user_ns.get(df_name)
            if df is None:
                raise NameError(f"DataFrame '{df_name}' 不存在/缺少 DataFrame")
            if not isinstance(df, pd.DataFrame):
                raise TypeError(f"'{df_name}' 不是DataFrame")
            dfs_dict[df_name] = df
        return dfs_dict

    def _validate_optional_arg(self, arg_name: str, arg_value: Any, expected_type: Type) -> Any:
        """验证可选参数类型"""
        if arg_value is not None and not isinstance(arg_value, expected_type):
            raise TypeError(f"'{arg_name}' 不是 {expected_type.__name__} 类型")
        return arg_value

    def _initialize_llm(self, api_base: str, model: str) -> LocalLLM:
        """初始化本地LLM"""
        return LocalLLM(
            api_base=api_base,
            model=model,
            temperature=0.3,
            timeout=60
        )

    def _setup_agent(
            self,
            dfs_list: List[DataFrame],
            llm: LocalLLM,
            memory_size: int,
            skills: Optional[List[str]] = None,
            query: Optional[str] = None,
            clarification: bool = False,
            explain: bool = False,
            whitelist: Optional[List[str]] = None
    ) -> Union[CustomAgent, Any]:
        if whitelist is None:
            whitelist = []
        # print("Agent 实例化获取到的参数\n")
        # print(dfs_list, llm, memory_size, skills, query, clarification, explain, whitelist)
        """设置并返回配置好的Agent及其处理结果"""
        agent = CustomAgent(
            dfs_list,
            config={
                "llm": llm,
                "custom_whitelisted_dependencies": whitelist,
                "description": "你是一名数据分析专员。你的主要目标是帮助非技术用户分析数据。返回结果中除去代码部分是英文外，其他部分必须翻译成中文."
            },
            memory_size=memory_size
        )

        if skills:
            agent = self._add_skills_to_agent(agent, skills)
            agent.chat(query)
            return agent

        return agent

    def _add_skills_to_agent(self, agent: CustomAgent, skills: List[str]) -> None:
        """向Agent添加技能函数"""
        for func in skills:
            func_name = self.shell.user_ns.get(func)
            if not func_name:
                raise NameError(f"函数 '{func_name}' 未定义")

            # print("func_name 名称\n")
            # print(func_name.__name__)
            # print(type(func_name), '\n')
            # 无论是否已装饰，都会返回合规的skill函数
            agent.add_skills(skill(func_name))
            print(f"✅ 已加载技能: {func_name.__name__}")
            print("********注意！ Agent 只能使用一个 skill，多个 skill 会发生覆盖*********")
        return agent

    def _handle_agent_modes(
            self,
            agent: CustomAgent,
            query: str,
            clarification: bool,
            explain: bool
    ) -> Any:
        """处理Agent的各种模式"""
        if clarification:
            print("*" * 20, '\t', "启动clarification模式", '\t', "*" * 20)
            result = agent.clarification_questions(query)
            print("Agent澄清功能返回结果\n")
            print(result)
            print("*"*20)

            if explain:
                print("*" * 20, '\t', "启动explain模式", '\t', "*" * 20)
                return display(Markdown(agent.explain()))
            return result

        # print("将要处理的问题是\n", query)
        result = agent.chat(query)
        # print("Agent返回结果\n", result)

        if explain:
            print("*" * 20, '\t', "启动explain模式", '\t', "*" * 20)
            return display(Markdown(agent.explain()))
        return result

    def _setup_smart_dataframe(
            self,
            dfs_list: List[DataFrame],
            llm: LocalLLM,
            example_df: Optional[DataFrame] = None,
            field_descriptions: Optional[Dict] = None
    ) -> Union[SmartDataframe, SmartDatalake]:
        """设置并返回SmartDataframe或SmartDatalake"""
        if len(dfs_list) == 1:
            if field_descriptions:
                connector = PandasConnector(
                    {"original_df": dfs_list[0]},
                    field_descriptions=field_descriptions
                )
                return SmartDataframe(
                    connector,
                    config={
                        "llm": llm,
                        "custom_head": example_df,
                        "connector": connector
                    }
                )
            return SmartDataframe(
                dfs_list[0],
                config={"llm": llm, "custom_head": example_df}
            )
        return SmartDatalake(dfs_list, config={"llm": llm})

    def _get_instance_key(self, args, dfs_list) -> str:
        """生成真正唯一的实例键"""
        from pickle import dumps
        from hashlib import sha256

        # 1. 序列化关键参数
        key_params = {
            k: v for k, v in vars(args).items()
            if k not in ['dfs', 'output_type', 'field_descriptions', 'example_df']
        }

        # 2. 使用稳定可靠的序列化方法
        params_dump = dumps(key_params, protocol=4)
        dfs_dump = dumps([id(df) for df in dfs_list], protocol=4)

        # 3. 使用加密级哈希避免冲突
        params_hash = sha256(params_dump).hexdigest()[:16]
        dfs_hash = sha256(dfs_dump).hexdigest()[:16]

        # 4. 包含参数摘要便于调试
        param_summary = "_".join(
            f"{k[:3]}{int(v) if isinstance(v, bool) else ''}"
            for k, v in key_params.items()
        )[:32]

        return f"pai_{param_summary}_{params_hash}_{dfs_hash}"


    @magic_arguments()
    @argument('dfs', nargs='+', help='将要使用的DF或者DFs')
    @argument('-m', '--model', help='模型名称', default="deepseek-r1:7b")
    @argument('-a', '--api_base', help='模型服务url地址', default="http://localhost:11434/v1")
    @argument('-o', '--output_type',
              help='指定输出类型，辅助模型确认返回结果类型',
              choices=["number", "dataframe", "plot", "string"],
              default="string")
    @argument('--agent', action='store_true',
              help='使用Agent模式（支持clarification和explain功能）')
    @argument('--memory_size', type=int, default=5,
              help='Agent的记忆大小(对话轮数)（仅--agent模式有效）不要轻易超过5轮会导致大模型服务压力过大')
    @argument('-c', '--clarification', action='store_true',
              help='生成澄清问题（需--agent模式）')
    @argument('-e', '--explain', action='store_true',
              help='解释上一次回答的逻辑（需--agent模式）')
    @argument('-s', '--skills', nargs='*',
              help='要添加的技能函数名（多个用空格分隔）必须是在Agent模式下且函数必须有注释说明')
    @argument('-w', '--whitelist', nargs='*', help='要添加的白名单')
    @argument('--example_df', help='示例DF数据头几行')
    @argument('--field_descriptions', help='特征解释说明，必须是Dict类型')
    @cell_magic
    def pandas_ai(self, line: str, cell: str) -> Any:
        """PandasAI魔法命令主入口"""
        args = parse_argstring(self.pandas_ai, line)
        print("当前输入参数为", args, '\n')

        field_descriptions = self.shell.user_ns.get(args.field_descriptions)
        print("获取到的field_descriptions是", field_descriptions)
        print(type(field_descriptions))

        # 获取DF字典
        dfs_dict = self._get_dataframes(args.dfs)
        dfs_list = list(dfs_dict.values())

        #  非 Agent 模式：
        # 验证可选参数
        example_df = self._validate_optional_arg('example_df', args.example_df, pd.DataFrame)
        field_descriptions = self._validate_optional_arg('field_descriptions', field_descriptions, dict)

        llm = self._initialize_llm(args.api_base, args.model)

        if not args.agent:
            llm = self._initialize_llm(args.api_base, args.model)
            return self._setup_smart_dataframe(dfs_list, llm, example_df, field_descriptions).chat(cell.strip())

        # Agent模式：
        # 参数验证
        if (args.clarification or args.explain) and not args.agent:
            raise ValueError("--clarification和--explain必须在--agent模式下使用")

        # Agent模式下 获取或创建实例
        instance_key = self._get_instance_key(args, dfs_list)
        # print("目前获取的 instance_key 是：\n", instance_key)
        self._current_key = instance_key
        if instance_key not in self._instances:
            # print("创建新的key：value 键值对*************")
            # 此处的 key 对应的 value 是模型返回结果
            agent = self._setup_agent(dfs_list=dfs_list, llm=llm, memory_size=args.memory_size,
                                                              skills=args.skills, query=cell.strip(),
                                                              clarification=args.clarification, explain=args.explain,
                                                              whitelist=args.whitelist)
            self._instances[instance_key] = agent
            print("当前agent已缓存，如需继续对话，请重新输入问题")
            result = self._handle_agent_modes(agent, cell.strip(), args.clarification, args.explain)
            # 更新缓存
            self._last_query = cell.strip()
            self._last_result = result
            return result

        # 如果发现复用，此处直接获取 Agent 对象，不需要再次创建
        # print("当前实例字典中包含内容是：\n", self._instances)
        instance_value = self._instances[instance_key]
        # print("将要重复调用的 instance_key是：\n", instance_key)
        # 示例存在直接调用
        # 新问题，需要重新调用
        query = cell.strip()
        # print("追问内容是：\n", query)
        print(self._last_query)
        if str(cell.strip()) == str(self._last_query.strip()):
            print("⚡ Agent 使用缓存结果")
            return self._last_result
        # 组合下新问题
        # if self._last_result:
        #     query = f"{self._last_result}  {query}"
        result = self._handle_agent_modes(instance_value, query, args.clarification, args.explain)

        # 更新缓存
        self._last_query = query
        self._last_result = result
        # print("更新后的 query 和 result \n")
        # print(self._last_query)
        # print(self._last_result)

        # 如果是重复问题，直接返回缓存结果
        return result

    @line_magic
    def pandasai_list(self, line: str) -> None:
        """列出所有存储的实例"""
        if not self._instances:
            print("没有存储的PandasAI实例")
            return

        print("存储的PandasAI实例:")
        for idx, (key, instance_value) in enumerate(self._instances.items(), 1):
            print(f"{idx}. {key}: {type(instance_value).__name__}")
            if hasattr(instance_value, 'config') and hasattr(instance_value.config, 'llm'):
                llm = instance_value.config.llm
                print(f"   Model: {getattr(llm, 'model', 'unknown')}")
            if key == self._current_key:
                print("   (当前活动实例)")

    @line_magic
    def pandasai_clean(self, line: str) -> None:
        """清理指定或所有实例"""
        if line.strip():
            if line.strip() in self._instances:
                del self._instances[line.strip()]
                print(f"已删除实例: {line.strip()}")
                if self._current_key == line.strip():
                    self._current_key = None
            else:
                print("未找到指定实例")
        else:
            self._instances.clear()
            self._current_key = None
            print("已清理所有实例")


def load_ipython_extension(ipython: Any) -> None:
    """注册扩展"""
    try:
        ipython.register_magics(PandasAIMagics)
        print("PandasAI魔法命令已加载。使用方式:")
        print("  %%pandas_ai df1 [df2...] [参数]")
        print("  %pandasai_list - 列出所有实例")
        print("  %pandasai_clean - 清理实例")
    except Exception as e:
        warnings.warn(f"扩展加载失败: {str(e)}")