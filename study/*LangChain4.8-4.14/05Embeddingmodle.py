from langchain_community.embeddings import DashScopeEmbeddings as Embed
embed = Embed()
#测试
print(embed.embed_query("i hate u"))
print(embed.embed_documents(
    ["i hate u",
     "f^^k you",
     "f^^k you leli much"])
)