class ConversationMemory:
    def __init__(self):
        self.messages=[]

    def get_recent_messages(self):
        system_message = self.messages[0]

        recent_messages = self.messages[1:][-6:]

        return [system_message] + recent_messages
    def add_user_message(self, content):
        self.messages.append({
            "role":"user",
            "content":content
        })


    def add_assistant_message(self,content):
        self.messages.append({
            "role":"assistant",
            "content":content
        })
    def get_messages(self):
        return self.messages
    def add_system_message(self,content):
        self.messages.append({
            "role":"system",
            "content":content
        })

        if __name__ == "__main__":
            memory = ConversationMemory()

            memory.add_user_message("最近有什么奖学金通知？")
            memory.add_assistant_message("目前找到3条相关通知")

            print(memory.get_messages())