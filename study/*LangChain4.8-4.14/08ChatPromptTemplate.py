#PromptTemplate中的from_template只能接收一条信息。from-messages可以接收list消息
#历史会话是动态的，所以历史会话信息要动态注入

#==============================先自己测试并打印出来完整提示词==============================
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

chat_prompt_template=ChatPromptTemplate.from_messages(
    [("system","你是一个诗人"),
    MessagesPlaceholder("history"),
    ("human","再写一首诗")]
)

history_data=[#提前准备好历史数据，在下一步直接注入
    ("human","写诗"),
    ("ai","床前明月光，疑是地上霜")
]

prompt_text = chat_prompt_template.invoke({"history":history_data})#注意invoke里面是字典
#print(prompt_text)

#==========================把问题丢给模型处理==========================
from langchain_community.chat_models.tongyi import ChatTongyi
model = ChatTongyi(model="qwen3-max")
res = model.invoke(prompt_text)
print(res.content,type(res))