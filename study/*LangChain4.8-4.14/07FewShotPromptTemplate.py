from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
#==============================先自己测试并打印出来完整提示词==============================
#①示例的模板
example_template = PromptTemplate.from_template("单词:{word},反义词:{antonym}")

#②示例的动态注入(列表内套字典)
example_data=[
    {"word":"大","antonym":"小"},
    {"word":"多","antonym":"少"}
]

few_shot_template=FewShotPromptTemplate(#一共有五个参数
    example_prompt=example_template,    #①示例数据的模板
    examples=example_data,          #②示例数据模板中要注入的数据（列表套字典）
    prefix="告诉我单词的反义词，这是我的例子", #③示例之前的提示词
    suffix="根据我的例子和问题，告诉我{input}的反义词",#④示例之后的提示词
    input_variables=['input']      #⑤占位符名字
)

prompt_text = few_shot_template.invoke(input={"input":"上"}).to_string()
print(prompt_text)


#==========================把问题丢给模型处理==========================
from langchain_community.llms.tongyi import Tongyi
model = Tongyi(model="qwen-max")
print(model.invoke(input=prompt_text))

