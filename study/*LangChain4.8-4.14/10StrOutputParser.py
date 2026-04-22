from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

parser=StrOutputParser()
model = ChatTongyi(model="qwen3-max")
prompts = PromptTemplate.from_template("我的狗儿品种是{breed}，刚生了一窝一共{number}个狗娃，帮我起个名字")

chain = prompts | model | parser |model

res = chain.invoke({"breed":"五黑犬","number":"3"})
print(res)