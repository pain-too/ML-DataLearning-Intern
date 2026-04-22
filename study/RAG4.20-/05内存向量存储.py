#文件材料为info.csv
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
file_path = "/Users/pc/Documents/GitHub/LLM-study-notes/RAG4.20-/material/info.csv",
source_column = "source"        #指定本条数据的来源（列）
)
documents = loader.load()

vector_store = InMemoryVectorStore(
    embedding = DashScopeEmbeddings()
)


#向量存储的新增
vector_store.add_documents(
    documents = documents,              #被添加的文档，类型是list[document]
    ids = ["id"+str(i) for i in range(1,len(documents)+1)]  #给加进来的文档加序号ids
)

#删除
vector_store.delete(["id1","id2"])

#检索
res = vector_store.similarity_search(
    query = "python是不是简单易学的",
    k = 3       #要找出几个
)

print(res)