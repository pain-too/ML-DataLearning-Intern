#=====================================================================================以下全部是08的代码
#======================先自己测试并打印出来完整提示词======================
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

chat_prompt_template=ChatPromptTemplate.from_messages(
    [("system","你是一个诗人"),
    MessagesPlaceholder("history"),
    ("human","再写一首诗")]
)

history_data=[
    ("human","写诗"),
    ("ai","床前明月光，疑是地上霜")
]

prompt_text = chat_prompt_template.invoke({"history":history_data})
#print(prompt_text)

#==================把问题丢给模型处理==================
from langchain_community.chat_models.tongyi import ChatTongyi
model = ChatTongyi(model="qwen3-max")
res = model.invoke(prompt_text)
#print(res.content,type(res))


#==========================================================================================08代码结束


#刚才先准备提示词，再丢给大模型，是两步。组链可以变成一步
chain = chat_prompt_template | model

#通过链chain调用invoke/stream
res = chain.invoke({"history":history_data})
for chunk in res:
    print(chunk,end="",flush=True)