# @Time   : 2025/3/23 20:07
# @Author : Sean
# @File   : jetbrain_runner.py
import requests


def scrape_index_page():
    base_url = "https://plugins.jetbrains.com/api/searchPlugins"
    products = [
        "androidstudio", "appcode", "aqua", "clion", "dataspell",
        "dbe", "fleet", "go", "idea", "idea_ce", "mps", "phpstorm",
        "pycharm", "pycharm_ce", "rider", "ruby", "rust", "webstorm", "writerside"
    ]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
        "Accept": "application/json",
        "Referer":"https://plugins.jetbrains.com/search?excludeTags=internal&products=androidstudio&products=appcode&products=aqua&products=clion&products=dataspell&products=dbe&products=fleet&products=go&products=idea&products=idea_ce&products=mps&products=phpstorm&products=pycharm&products=pycharm_ce&products=rider&products=ruby&products=rust&products=webstorm&products=writerside&search=code%20gen",
        "Accept-Encoding": "gzip",
    }
    params = [
        ("search", "code gen"),
        ("excludeTags", "internal"),
        ("excludeTags", "theme"),
        ("sort", "relevance"),
        ("build", "243.26053.27")
    ]
    offset = 0
    limit = 12
    new_param = params.copy()
    new_param.extend([("offset", str(offset)), ("limit", str(limit))])
    for product in products:
        new_param.append(("products", product))
    response = requests.get(base_url,headers=headers, params=new_param)
    if response.status_code == 200:
        print("Successfully scraped")
        print(response.json())
    else:
        print("Failed to scrape with status code", response.status_code)
        print("Reason:", response.text)


if __name__ == '__main__':
    scrape_index_page()
