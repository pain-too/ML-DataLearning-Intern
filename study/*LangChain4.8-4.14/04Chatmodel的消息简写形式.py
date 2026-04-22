from langchain_community.chat_models.tongyi import ChatTongyi


model=ChatTongyi(model="qwen3-max")
messages=[
    ("system","你是一位战术分析师"),
    ("human","对比国内篮球战术"),
    ("ai","我可以给出2024-25赛季广州龙狮与北汽战术对比 "),
    ("human","进行总结对比"),
]

res = model.stream(messages)

for chunk in res:
    print(chunk.content,end="",flush=True)