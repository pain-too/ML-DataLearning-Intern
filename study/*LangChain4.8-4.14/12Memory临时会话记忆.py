from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

model = ChatTongyi(model="qwen3-max")
str_parser = StrOutputParser()


#=========================构建通用提示词模板===========================
prompt = PromptTemplate.from_template(
    "你需要根据用户回话历史信息回答问题。对话历史是{chat_history},用户的问题是{input}，请回答。")

def print_prompt(full_prompt):
    print("="*20,full_prompt.to_string(),"="*20)
    return full_prompt

base_chain = prompt | print_prompt | model | str_parser#构建基础链


#=========================创建增强链===========================
#利用这个字典维护用户
store={}#字典的key是session_id，value是InMemoryChatMessage类对象
def get_history (session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

conversation_chain = RunnableWithMessageHistory(
    base_chain,
    get_history,#通过会话id获取InMemoryMessageHistory类对象
    input_messages_key = "input",
    history_messages_key = "chat_history",
)#四个关键参数，第二个还未实现，接下来定义函数（代码是按顺序运行，所以把定义放在了前面）


if __name__ == "__main__":
    #固定格式，配置session_id（一个字典）
    session_config = {
        "configurable": {
            "session_id":"001"
        }
    }
    res = conversation_chain.invoke({"input":"小明有三只猫"},session_config)
    print("第一次执行",res)

    res = conversation_chain.invoke({"input": "小刚有一只鹦鹉"}, session_config)
    print("第二次执行", res)

    res = conversation_chain.invoke({"input": "一共几个动物"}, session_config)
    print("第三次执行", res)