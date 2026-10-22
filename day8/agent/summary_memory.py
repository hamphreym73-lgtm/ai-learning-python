import json
from pathlib import Path
import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
class SummaryMemory:
    def __init__(self):
        self.summary = ""

        self.memory_file = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "summary.json"
        )

        # 初始化时自动加载历史摘要
        self.load_summary()

    def update_summary(self, new_summary):
        self.summary = new_summary
        self.save_summary()

    def get_summary(self):
        return self.summary

    def save_summary(self):
        self.memory_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(
                {"summary": self.summary},
                f,
                ensure_ascii=False,
                indent=4
            )

    def load_summary(self):
        if self.memory_file.exists():
            with open(self.memory_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.summary = data.get("summary", "")