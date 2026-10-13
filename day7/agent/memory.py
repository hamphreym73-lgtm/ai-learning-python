import json
import os

class ConversationMemory:
    def __init__(self):
        self.messages = []

        self.memory_file = "day7/data/memory.json"

        os.makedirs(
            "day7/data",
            exist_ok=True
        )

        self.load_memory()
    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file,"r",encoding="utf-8") as f:
                 self.messages = json.load(f)
    def save_memory(self):
        with open(self.memory_file,"w",encoding="utf-8") as f:
            json.dump(self.messages,f,ensure_ascii=False,indent=4)

    def get_recent_messages(self):
        system_messages = [
            msg for msg in self.messages
            if msg["role"] == "system"
        ]

        other_messages = [
            msg for msg in self.messages
            if msg["role"] != "system"
        ]

        return system_messages[:1] + other_messages[-6:]
    def add_user_message(self, content):
        self.messages.append({
            "role":"user",
            "content":content
        })
        self.save_memory()

    def add_assistant_message(self,content):
        self.messages.append({
            "role":"assistant",
            "content":content
        })
        self.save_memory()
    def get_messages(self):
        return self.messages

    def compress_memory(self):
        system_message = self.messages[0]

        recent_messages = self.messages[-4:]

        self.messages = [
                            system_message
                        ] + recent_messages

        self.save_memory()
    def add_system_message(self,content):
        self.messages.append({
            "role":"system",
            "content":content
        })
        self.save_memory()

if __name__ == "__main__":
    memory = ConversationMemory()

    memory.add_user_message("最近有什么奖学金通知？")
    memory.add_assistant_message("目前找到3条相关通知")

    print(memory.get_messages())