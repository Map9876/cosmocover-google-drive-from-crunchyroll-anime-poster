import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 目标URL列表
urls = [
    "https://www.cosmocover.com/newsroom/",
    "https://c.map987.us.kg/https://www.cosmocover.com/de/newsroom-de/"
]

# 用于存储所有符合条件的超链接的列表
all_hyperlinks = []

# 读取现有的文章链接
existing_links = set()
try:
    with open('README.md', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("http"):
                existing_links.add(line.strip())
except FileNotFoundError:
    pass

# 迭代URLs列表，获取每个URL的HTML源代码并提取超链接
for url in urls:
    if url in existing_links:
        print("遇到了已经有的文章，跳过")
        continue  # 如果URL已经在existing_links中，跳过该URL

    response = requests.get(url)
    html_content = response.text

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 找到所有的超链接
    links = soup.find_all('a', href=True)

    # 提取符合条件的超链接并添加到列表中，确保保留顺序
    for link in links:
        href = link['href']
        if ((href.startswith("https://www.cosmocover.com/newsroom/") or 
             href.startswith("https://www.cosmocover.com/de/newsroom/")) and
            not href.endswith("newsroom/") and
            not href.endswith("newsroom/page/2/") and
            href.count('/') > 5):
            if href not in existing_links:
                all_hyperlinks.append(href)

# 找出新的文章链接
new_links = all_hyperlinks
print(all_hyperlinks)
print("______________ 上面是找出的新的文章链接")

print(existing_links)
print("______________ 上面是txt已经有的老的文章链接")
# 如果没有新链接，程序结束
if not new_links:
    print("没有新的文章链接。")
    exit()

# 获取当前日期
current_date = datetime.now().strftime('%Y-%m-%d')

# 用于存储最终符合条件的超链接和网盘链接
final_links = []

# 检查每个新超链接的网页内容是否包含"crunch"关键词
for href in new_links:
    try:
        link_response = requests.get(href)
        link_content = link_response.text

        # 检查页面内容是否包含"crunch"关键词
        if "crunch" in link_content.lower():
            # 解析页面内容
            link_soup = BeautifulSoup(link_content, 'html.parser')
            # 查找带有"drive.google.com"关键词的链接
            drive_links = [a['href'] for a in link_soup.find_all('a', href=True) if "drive.google.com" in a['href']]
            drive_link = drive_links[0] if drive_links else 'None'
            final_links.append((href, drive_link))
    except requests.RequestException as e:
        print(f"无法请求链接: {href}. 错误: {e}")

# 将符合条件的超链接和网盘链接写入README.md文件
try:
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.readlines()
except FileNotFoundError:
    content = []

# 查找最后一个###符号的位置
last_header_idx = -1
for i, line in enumerate(content):
    if line.startswith("###"):
        last_header_idx = i

# 如果没有###符号就初始化文件内容
if last_header_idx == -1:
    content.insert(0, "### 新的文章链接\n")
    last_header_idx = 0

# 将新链接插入到最后一个###符号之后
new_content = [f"#### {current_date}\n"]
for link, drive_link in final_links:
    # 提取文章标题
    title = link.strip('/').split('/')[-1].replace('-', ' ')
    new_content.append(f"- **{title}**\n  - [Article Link]({link})\n")
    if drive_link != 'None':
        new_content.append(f"  - [Drive Link]({drive_link})\n")
new_content.append("\n")

content = content[:last_header_idx + 1] + new_content + content[last_header_idx + 1:]

with open('README.md', 'w', encoding='utf-8') as file:
    file.writelines(content)

print("符合条件的超链接和网盘链接已成功写入到README.md文件中。")
