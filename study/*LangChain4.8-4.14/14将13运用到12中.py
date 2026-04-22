#===============================================以下是13中的代码，有修改===================================================
import os,json
from langchain_core.messages import BaseMessage
from typing import Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict,messages_from_dict
'''还有一个messages_to_dict，注意区分单复数
        #message_to_dict:单个消息对象转换为单个字典      
        #messages_from_dict：列表套字典转换为列表套消息  
                            [即{},{}...]->[消息，消息...]
        to和from是“反义词”，加单复数表示一个或多个'''

class FileChatMessageHistory(BaseChatMessageHistory):

    def __init__(self,session_id,storage_path):
        self.session_id = session_id        #会话id
        self.storage_path = storage_path    #不同会话id对应的历史文件，所在的文件夹路径
        #完整的文件路径
        self.file_path = os.path.join(self.storage_path,self.session_id)
        #确保文件夹存在
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)



    def add_messages(self,messages: Sequence[BaseMessage]) ->None:
        all_messages = list(self.messages)   #已有的消息列表
        all_messages.extend(messages)       #追加新消息（揉进去）

        #数据写入本地文件
        #类对象写到文件，得到的是一堆二进制乱码 ==>  把BaseMessage消息转成字典（借助json模块，以json字符串格式写入文件）
        #官方包"message_to_dict"：单个消息对象->字典
        new_messages = []
        for message in all_messages:
            d = message_to_dict(message)    #d代表字典对象
            new_messages.append(d)          #原本存的message现在转成了字典，还需要写入文件
        with open(self.file_path,"w",encoding = "utf-8")as f:
            json.dump(new_messages,f)


    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path,"r",encoding = "utf-8")as f:
                message_data = json.load(f)
            return messages_from_dict(message_data)
        except FileNotFoundError:
            return []


    def clear(self) -> None:
        with open(self.file_path,"w",encoding = "utf-8")as f:
            json.dump([],f)


#=======================================================13结束===========================================================
#=============================================以下是12中的代码，完全复制过来=================================================


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

def get_history (session_id):
    return FileChatMessageHistory(session_id,"./chat_history/")

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
    #res = conversation_chain.invoke({"input":"小明有三只猫"},session_config)
    #print("第一次执行",res)

    #res = conversation_chain.invoke({"input": "小刚有一只鹦鹉"}, session_config)
    #print("第二次执行", res)

    res = conversation_chain.invoke({
        "input": """嗨喽嗨喽你好吗今天天气怎么样
        """

    }, session_config)
    print(res)

#======================================================12复制完成========================================================