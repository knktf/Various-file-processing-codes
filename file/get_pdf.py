"""
我希望您担任 IT 专家。我将为您提供有关我的技术问题所需的所有信息，您的角色是解决我的问题。你应该使用你的计算机科学，网络基础设施和 IT 安全知识来解决我的问题。在您的答案中为各个级别的人使用智能、简单和易于理解的语言会有所帮助。逐步解释您的解决方案并带有要点很有帮助。我希望你回复解决方案，而不是写任何解释


我的需求是
1.爬取此网址（https://geosynthetic-institute.org/whitepapers.htm）内的所有pdf文件并保存到本地。
2.下载的文件名和网页上一样，请保持下载文件名称与网页文件名称一致。
"""
import os
import time
import random
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


# 设置请求头信息，模拟正常的浏览器行为
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Referer": "https://www.concretecanvas.com/downloads/",
}

# 指定要下载的网址
url = "https://www.concretecanvas.com/downloads/"

# 创建目录
dir_name = "downloaded_files"
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

# 设置代理池
proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "http://127.0.0.1:1080",
}

# 发送 HTTP 请求，获取 HTML 页面内容
retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry_strategy)
with requests.Session() as session:
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    response = session.get(url, headers=headers, proxies=proxies)

# 解析 HTML 页面
soup = BeautifulSoup(response.content, "html.parser")

# 找到所有的 PDF 链接
pdf_links = []
for link in soup.find_all("a", href=True):
    if link["href"].endswith(".pdf"):
        if "http" in link["href"]:
            pdf_links.append(link["href"])
        else:
            pdf_links.append(f"https://www.concretecanvas.com{link['href']}")

# 遍历所有的 PDF 链接，并下载对应的文件
for link in pdf_links:
    # 提取文件名
    file_name = link.split("/")[-1]
    # 如果文件已存在，则跳过下载
    if os.path.exists(os.path.join(dir_name, file_name)):
        print(f"{file_name} already exists, skipping download")
        continue
    # 发送 HTTP 请求，获取文件内容，并显示下载进度条
    while True:
        try:
            with requests.Session() as session:
                session.mount("http://", adapter)
                session.mount("https://", adapter)
                response = session.get(link, headers=headers, proxies=proxies, timeout=10)
                response.raise_for_status()
                break
        except (requests.exceptions.RequestException, ValueError):
            print("Connection error, retrying...")
            time.sleep(random.randint(1, 3))
            continue
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit="iB", unit_scale=True)
    with open(os.path.join(dir_name, file_name), "wb") as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()
    print(f"Downloaded {file_name}")
    # 延时访问，减缓访

# 下载完成后向用户显示一条消息
print("All files downloaded successfully.")