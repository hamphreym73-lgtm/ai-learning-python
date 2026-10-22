
from pathlib import Path
from day8.tools.notice_parser import extract_notice_text

html_file = Path("day8/data/notice.html")

if not html_file.exists():
    raise FileNotFoundError(f"没有找到网页文件：{html_file}")
html = html_file.read_bytes()
notice_text = extract_notice_text(html)
print("正文长度：", len(notice_text))
if not notice_text.strip():
    print("没有提取到正文，请检查网页结构。")
else:
    print("真实通知正文提取结果：")
    print(notice_text[:2000])
