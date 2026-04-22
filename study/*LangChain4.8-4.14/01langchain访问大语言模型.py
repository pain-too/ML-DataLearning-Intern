from langchain_community.llms import Tongyi
import os

# 自动读取环境变量，无需明文写死
llm = Tongyi(
    model="qwen-max",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)

response = llm.invoke("你好，通义千问！")
print(response)