"""
author：msy
功能：重写pandasai处理逻辑，新增对于 Deepseek 返回包含思维链的数据结果进行处理，以及对 Pandas-ai 中部分功能模板英文改成中文回答
"""
from pandasai.prompts.clarification_questions_prompt import ClarificationQuestionPrompt
import re, json
from typing import List
from pandasai import Agent
from pandasai.prompts.base import BasePrompt
from pandasai.exceptions import InvalidLLMOutputType
from jinja2 import FileSystemLoader, Environment

# 添加本地模板路径到搜索路径
template_loader = FileSystemLoader([
    "/Users/gedun/jupyter-ai-main/Rewrite_code",  # 本地模板路径
    "/Users/gedun/anaconda3/envs/jupyter-ai/lib/python3.10/site-packages/pandasai/prompts/templates"  # 默认路径
])
template_env = Environment(loader=template_loader)

def remove_think_tags(text: str) -> str:
    # 添加正则表达式匹配 think 模块
    Think_TAGS = re.compile(r'.*?</think>', re.DOTALL)
    return re.sub(Think_TAGS, '', text)


# 重写ClarificationQuestionPrompt中的validate方法
class CustomClarificationQuestionPrompt(ClarificationQuestionPrompt):
    """新增 Deepseek 类返回数据有 think 模块的情况处理"""
    # template_path = "/Users/gedun/jupyter-ai-main/Rewrite_code/clarification_questions_prompt.tmpl"
    template_path = template_env.get_template("clarification_questions_prompt.tmpl")
    print("使用新澄清模板")

    def validate(self, output) -> bool:
        # print("***********模板验证开始***************")
        try:
            # print("验证---------output 进行replace前\n")
            # print(output)
            output = output.replace("```json", "").replace("```", "")
            # print("验证---------output 进行replace后\n")
            # print(output)
            json_data = json.loads(output)
            return isinstance(json_data, List)
        except json.JSONDecodeError:
            return False


# 重写 Agent 继承的BaseAgent 中的一些方法
class CustomAgent(Agent):
    """新增 Deepseek 类返回数据有 think 模块的情况处理"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clarification_questions(self, query: str) -> List[str]:
        """
        Generate clarification questions based on the data
        """
        prompt = CustomClarificationQuestionPrompt(
            context=self.context,
            query=query,
        )

        result = self.call_llm_with_prompt(prompt)
        # print("澄清函数中，获取到的大模型返回结果是：\n", result)
        self.logger.log(
            f"""Clarification Questions:  {result}
            """
        )
        result = result.replace("```json", "").replace("```", "")
        # print("澄清函数中，获取到的大模型返回结果进行 replace 后结果：\n", result)
        questions: list[str] = json.loads(result)
        return questions[:3]

    def call_llm_with_prompt(self, prompt: BasePrompt):
        """
        Call LLM with prompt using error handling to retry based on config
        Args:
            prompt (BasePrompt): BasePrompt to pass to LLM's
        """
        retry_count = 0
        while retry_count < self.context.config.max_retries:
            try:
                result: str = self.context.config.llm.call(prompt)
                result = remove_think_tags(result).replace("'", '"')
                # 处理 explain 的\\n问题
                result = result.replace(r"\\n", "\n")
                # print("大模型返回结果----------去掉 think 替换单引号后\n")
                # print(result)
                if prompt.validate(result):
                    # print("验证正常，返回大模型去除 think 模块后的结果---------")
                    return result
                else:
                    raise InvalidLLMOutputType("当前模型返回数据格式异常无法处理，请重新尝试")
            except Exception:
                if (
                    not self.context.config.use_error_correction_framework
                    or retry_count >= self.context.config.max_retries - 1
                ):
                    raise
                retry_count += 1


    def explain(self) -> str:
        """
        Returns the explanation of the code how it reached to the solution
        """
        try:
            prompt = ExplainPromptMsy(
                context=self.context,
                code=self.last_code_executed,
            )
            response = self.call_llm_with_prompt(prompt)
            # print("进入重构后的 explain 函数，获取到的大模型返回结果是：\n")
            # print(response)
            self.logger.log(
                f"""Explanation:  {response}
                 """
            )
            return response
        except Exception as exception:
            return (
                "Unfortunately, I was not able to explain, "
                "because of the following error:\n"
                f"\n{exception}\n"
            )


class ExplainPromptMsy(BasePrompt):
    """Prompt to generate Python code from a dataframe."""

    # template_path = "/Users/gedun/jupyter-ai-main/Rewrite_code/explain.tmpl"
    template_path = template_env.get_template("explain.tmpl")
    print("使用新explain模板")

# 备选
class RephraseQueryPrompt(BasePrompt):
    """Prompt to generate Python code from a dataframe."""

    template_path = template_env.get_template("rephrase_query.tmpl")
