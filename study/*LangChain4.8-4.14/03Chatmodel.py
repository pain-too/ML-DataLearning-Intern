from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

model=ChatTongyi(model="qwen3-max")
messages=[
    SystemMessage(content="你是一位战术分析师"),
    HumanMessage(content="对比国内篮球战术"),
    AIMessage(content="我可以给出2024-25赛季广州龙狮与北汽战术对比 "),
    HumanMessage(content="进行总结对比"),
]

res = model.stream(messages)

for chunk in res:
    print(chunk.content,end="",flush=True)