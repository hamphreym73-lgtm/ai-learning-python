from tools.school_notice_tool import search_school_notices


class NoticeAgent:

    def __init__(self):
        pass


    def run(self, question):

        if "奖学金" in question:

            result = search_school_notices(
                "奖学金"
            )

            return result


        elif "助学金" in question:

            result = search_school_notices(
                "助学金"
            )

            return result


        else:

            return "暂时没有找到相关通知"