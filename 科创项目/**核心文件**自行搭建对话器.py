from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_deepseek.chat_models import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
import os,json
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict,messages_from_dict

load_dotenv("qwen_key.env")
model = ChatDeepSeek(
    model = "deepseek-chat",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    streaming = True
)
str_parser = StrOutputParser()


#================================13本地文件对话记忆================================

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path) -> None:
        self.session_id = session_id
        self.storage_path = storage_path
        self.file_path = os.path.join(storage_path,session_id)
        os.makedirs(self.storage_path,exist_ok=True)

    def add_messages(self,messages) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)
        new_messages = []
        for message in all_messages:
            d = message_to_dict(message)
            new_messages.append(d)

        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump(new_messages,f)

    @property
    def messages(self):
        try:
            with open(self.file_path,"r",encoding="utf-8") as f:
                loaded_json =  json.load(f)
                return messages_from_dict(loaded_json)
        except FileNotFoundError:
            return []

    def clear(self):
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump([],f)







#==========================创建基础链=======================
prompt = ChatPromptTemplate.from_messages([
    ("system","""
1. 你是专业的科创研究数据处理助手，协助我进行西北农林科技大学风景园林艺术学院的科创项目数据处理。
2. 我们研究的内容是：三种不同植物香气对人注意力的影响。
3. 招募共150名志愿者，分为三组，分别闻丁香、薰衣草、雪松香气；每周闻5次，每次20分钟。
4. 采用舒尔特方格、Stroop 实验用时作为注意力指标。
5. 实验开始前（未闻香气）进行前测；实验开始后每隔3–4天进行后测。
6. 每次 Stroop、舒尔特各做两次，取平均值作为当次数据；实验周期为1个月，已完成数据采集。
7. 因 PyCharm 部署的 LLM 无法直接读取本地文件，需要生成**可直接复制运行**的完整代码。
8. 数据文件为 Excel，两个文件均包含 id 列；id 为三位数，百位数字对应组别：1=丁香、2=薰衣草、3=雪松。
9. Stroop 文件：文件名 stroop_多次对比，绝对路径 /Users/pc/Desktop/longtitudinal_comparison/stroop_多次对比.xlsx。
10. Stroop 文件列名：id、name、0、1、2、3、4、5、6、7、8；0=前测，1–8=后测，空值为无效数据。
11. 每位被试测试次数不等（2–9次）；第二行开始为数据，一行对应一名被试的多次 Stroop 平均成绩。
12. Schulte 文件：文件名 schulte_多次对比，绝对路径 /Users/pc/Desktop/longtitudinal_comparison/schulte_多次对比.xlsx。
13. Schulte 文件列名：id、name、0、1、2、3、4、5、6、7、8；0=前测，1–8=后测，空值为无效数据。
14. 每位被试测试次数不等（2–9次）；第二行开始为数据，一行对应一名被试的多次舒尔特平均成绩。
    """),
    ("user","请你根据历史信息回答问题。历史信息是{history},用户问题是{input}")
])
base_chain = prompt | model



#=============================创建增强链==========================
def get_history(session_id):
    return FileChatMessageHistory(session_id,"/Users/pc/Documents/GitHub/LLM-study-notes/LangChain4.8-4.14/chat_history")

conversation_chain = RunnableWithMessageHistory(
    base_chain,
    get_history,
    history_messages_key = "history",
    input_messages_key = "input"
)


#================================主程序运行==============================
if __name__ == "__main__":
    print("="*124)
    print(" "*40,"🌿 科创数据助手已启动（输入问题后，输 end 发送）")
    print(" "*46,"🚪 输入 quit / exit 可退出程序")
    print("="*124)

    session_config = {
        "configurable": {"session_id": "001"}
    }

    while True:
        print("输入问题后，输 end 发送:")

        # 多行输入读取
        lines = []

        #======================无限循环的作用：python以回车为标志，自动按行切割遍历每一行==============
        while True:
            line = input()

            # 先判断是否要退出指令
            if line.strip().lower() in ["quit", "exit", "q", "退出"]:
                print("\n👋 程序已退出，记忆已保存")
                exit()

            # 再判断是否要结束输入
            if line.strip().lower() == "end":
                break

            #如果都不是，则line追加到lines，进入下一循环处理下一行
            #追加过程中忽略换行符
            lines.append(line)

        #重新加入换行符，保证裱prompt结构清晰
        user_input = "\n".join(lines)

        # 空内容跳过
        if not user_input.strip():
            print("⚠️ 输入不能为空，请重新输入")
            continue

        # 获取回答
        try:
            print("\n🤖 助手回答：")
            # 直接 for 循环 stream，不要用变量接
            for chunk in conversation_chain.stream(
                    {"input": user_input},
                    config=session_config
            ):
                # 只打印内容，不换行，flush=True 实时输出
                print(chunk.content, end="", flush=True)
            # 全部输出完再换行
            print()
        except Exception as e:
            print("\n❌ 运行出错：", e)

        print("-"*60)
        print()
        print()

