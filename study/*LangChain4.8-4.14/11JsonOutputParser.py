from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatTongyi

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

model = ChatTongyi(model = "qwen3-max")
first_prompt = PromptTemplate.from_template("帮我的狗儿{breed}起个名字，三个月大。只给我回复一个名字，别的都不要，封装成json格式返回。要求key就是name，value是你起的名字。")
second_prompt = PromptTemplate.from_template("你看看{name}这个名字怎么样")
chain = first_prompt | model | json_parser | second_prompt | model | str_parser

for chunk in chain.stream({"breed":"五黑犬"}):
    print(chunk,end="",flush=True)
