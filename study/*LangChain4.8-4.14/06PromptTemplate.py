from langchain_core.prompts import PromptTemplate
prompt_template=PromptTemplate.from_template(
    "ﬁ")#=====记作②======
prompt_text = prompt_template.format(breed="柯基",number="5")


from langchain_community.llms.tongyi import Tongyi
model = Tongyi(model="qwen-max")#==========记作①============
res = model.invoke(input=prompt_text)
print(res)



#扩展内容：有了提示词和模型（①②）就可以组链条
chain = prompt_template | model
res = chain.invoke(input={"breed":"柯基","number":"5"})