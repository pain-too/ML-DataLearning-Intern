#在上一步的基础上，把检索这一步加入链中
#复制代码，在上一步基础上修改
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


model = ChatTongyi(model = "qwen3-max")
prompt = ChatPromptTemplate.from_messages([
    ("system","以提供的参考资料为例，回答用户的问题。参考资料是{context}"),
    ("user","我的问题是{input}")
])

vector_store = InMemoryVectorStore(
    embedding = DashScopeEmbeddings(model = "text-embedding-v4"))

vector_store.add_texts(["减肥就是少吃多练","减肥期间吃的东西很重要，清淡少油控卡并且运动起来","跑步是很好的运动"])
input_text = "怎么减肥？"

#============================================以上复制，以下新增===========================================
retriever = vector_store.as_retriever(search_kwargs = {"k" : 2})
#想象中的链
chain =  retriever | prompt | model | StrOutputParser()
'''
retriever:
        输入：用户的提问        str
        输出：向量库检索结果     list[document]
promot:
        输入：用户提问+检索结果   dict
        输出：完整提示词         PromptValue
'''
chain = (
    {"input": RunnablePassthrough(),"context":(retriever | format_func)} | prompt | model | StrOutputParser()
)
chain.invoke()