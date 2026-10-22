from day7.tools.school_notice_tool import search_school_notices
from day8.services.llm_service import chat
from day8.tools.notice_parser import extract_notice_text
from day8.tools.web_fetch_tool import fetch_webpage
from pathlib import Path
class ReactAgent:

    def __init__(self, planner):
        self.planner = planner

    def check_task_completion(self, task, observation):
        """根据真实工具结果，判断关键请求是否有依据。"""

        deadline_keywords = [
            "截止时间", "截止日期", "什么时候截止",
            "申请期限", "截止"
        ]

        needs_deadline = any(
            word in task for word in deadline_keywords
        )

        if not needs_deadline:
            return True

        # 当前通知工具返回的字段只有 title/date/category/content。
        # 如果内容没有提供截止日期，就不能声称已核实。
        content = str(observation)

        deadline_indicators = [
            "截止时间", "截止日期", "申请截止",
            "提交截止", "截至"
        ]

        return any(
            word in content for word in deadline_indicators
        )

    def run(self, task):
        print("第 1 轮")

        plan = self.planner(task)

        print("当前计划：")
        print(plan)

        result = self.execute(task, plan)

        if not result.get("verified", True):
            print("提示：用户要求的信息尚未核实。")

        return result["answer"]

    def execute(self, task, plan):
        if "ACTION: none" in plan:
            return {
                "status": "completed",
                "answer": "当前计划不需要继续调用工具。",
                "verified": True
            }

        if "ACTION: search_school_notices" not in plan:
            return {
                "status": "completed",
                "answer": "当前计划没有请求学校通知搜索工具。",
                "verified": False
            }

        if "KEYWORD:" not in plan:
            return {
                "status": "completed",
                "answer": "计划缺少搜索关键词，无法查询通知。",
                "verified": False
            }

        keyword = plan.split("KEYWORD:", 1)[1].strip()
        observation = search_school_notices(keyword)

        print("工具执行结果：")
        print(observation)

        if not observation:
            return {
                "status": "completed",
                "answer": "没有搜索到相关通知，暂时无法提供答案。",
                "verified": False
            }

        # 优先获取真实通知网页
        url = observation[0].get("url")

        if url:
            webpage = fetch_webpage(url)

            # 必须先检查登录状态，再解析正文
            if webpage["is_login_page"]:
                print("在线请求被重定向到登录页，尝试读取已保存的真实通知网页。")

                saved_html = Path("day8/data/notice.html")
                print("正文来源：本地保存的真实通知网页")
                if not saved_html.exists():
                    return {
                        "status": "completed",
                        "answer": "在线访问需要认证，且没有找到已保存的通知网页。",
                        "verified": False
                    }

                html = saved_html.read_bytes()
                notice_text = extract_notice_text(html)

                if not notice_text.strip():
                    return {
                        "status": "completed",
                        "answer": "已找到保存的网页文件，但未能提取通知正文。",
                        "verified": False
                    }

                print("已从保存的真实通知网页提取正文。")
            html = saved_html.read_bytes()
            notice_text = extract_notice_text(html)

            if not notice_text.strip():
                return {
                    "status": "completed",
                    "answer": "已访问通知页面，但未能提取到正文。",
                    "verified": False
                }


            print("提取到的通知正文：")
            print(notice_text[:1000])

            source_text = notice_text[:12000]

        else:
            # 没有 URL 时，只使用搜索工具返回的真实记录
            source_text = str(observation)

        complete = self.check_task_completion(task, source_text)

        if not complete:
            print("任务尚未完全核实：结果中没有明确的截止日期。")

        messages = [
            {
                "role": "system",
                "content": (
                    "你是校园通知助手。必须依据提供的通知信息回答。"
                    "不得编造通知、日期、申请条件或截止时间。"
                    "如果资料没有明确说明用户所问的信息，"
                    "必须明确回答无法核实。"
                )
            },
            {
                "role": "user",
                "content": (
                    f"用户问题：{task}\n\n"
                    f"通知资料：\n{source_text}\n\n"
                    "请根据资料回答用户的问题。"
                )
            }
        ]

        answer = chat(messages)

        return {
            "status": "completed",
            "answer": answer,
            "verified": complete
        }
