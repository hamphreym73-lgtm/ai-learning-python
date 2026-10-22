
import requests


def fetch_webpage(url):
    """获取网页，并识别是否被重定向到统一身份认证页面。"""

    response = requests.get(
        url,
        timeout=15,
        headers={"User-Agent": "Mozilla/5.0"},
        allow_redirects=True
    )

    response.raise_for_status()
    response.encoding = response.apparent_encoding

    final_url = response.url
    html = response.text

    # 检查最终地址和页面标题，识别登录页
    is_login_page = (
        "authserver/login" in final_url
        or "统一身份认证平台" in html
    )

    return {
        "requested_url": url,
        "final_url": final_url,
        "status_code": response.status_code,
        "is_login_page": is_login_page,
        "html": html
    }
