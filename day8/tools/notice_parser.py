
import re
from bs4 import BeautifulSoup


def clean_notice_text(text):
    # 合并 HTML 文本节点之间的空白
    text = re.sub(r"\s+", " ", text).strip()

    # 修复数字被空白拆开的情况，例如 202 5 -> 2025
    text = re.sub(r"(?<=\d)\s+(?=\d)", "", text)

    return text


def extract_notice_text(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    selectors = [
        "#content",
        ".content",
        ".article-content",
        ".wp_articlecontent",
        "article",
        "main",
    ]

    for selector in selectors:
        element = soup.select_one(selector)

        if element:
            text = element.get_text(" ", strip=True)
            text = clean_notice_text(text)

            if len(text) >= 100:
                return text

    if soup.body:
        text = soup.body.get_text(" ", strip=True)
        return clean_notice_text(text)

    return ""
