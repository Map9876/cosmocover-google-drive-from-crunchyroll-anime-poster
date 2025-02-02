import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 目标URL列表
urls = [
    "https://www.cosmocover.com/newsroom/",
    "https://c.map987.us.kg/https://www.cosmocover.com/de/newsroom-de/"
]

# 用于存储US区和DE区符合条件的超链接的列表
us_hyperlinks = []
de_hyperlinks = []

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
        # 排除基础链接和分页链接
        if ((href.startswith("https://www.cosmocover.com/newsroom/") or 
             href.startswith("https://www.cosmocover.com/de/newsroom/")) and
            href not in ["https://www.cosmocover.com/newsroom/", "https://www.cosmocover.com/newsroom/page/2/"]):
            if href not in existing_links:
                if href.startswith("https://www.cosmocover.com/newsroom/"):
                    us_hyperlinks.append(href)
                else:
                    de_hyperlinks.append(href)

# 获取当前日期
current_date = datetime.now().strftime('%Y-%m-%d')

# 用于存储最终符合条件的超链接和网盘链接
final_us_links = []
final_de_links = []

# 检查每个新超链接的网页内容是否包含"crunch"关键词
for href in us_hyperlinks:
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
            final_us_links.append((href, drive_link))
    except requests.RequestException as e:
        print(f"无法请求链接: {href}. 错误: {e}")

for href in de_hyperlinks:
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
            final_de_links.append((href, drive_link))
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
new_content = [f"#### {current_date} us区:\n"]
for link, drive_link in final_us_links:
    # 提取文章标题
    title = link.strip('/').split('/')[-1].replace('-', ' ')
    new_content.append(f"- **{title}**\n  - [Article Link]({link})\n")
    if drive_link != 'None':
        new_content.append(f"  - [Drive Link]({drive_link})\n")

new_content.append(f"#### {current_date} de区:\n")
for link, drive_link in final_de_links:
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
这个代码会将链接分为 us 区和 de 区，并在输出中添加相应的小标题。每个新日期的链接都将被添加在最近的 ### 标题之后，并以 Markdown 列表项的格式显示。

￼
￼
￼
日期不需要写两次，日期是总标题
好的，我已经理解了你的需求。我们将日期作为总标题，然后将两个区域的链接分类并添加小标题。以下是修改后的代码：

Python
￼
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 目标URL列表
urls = [
    "https://www.cosmocover.com/newsroom/",
    "https://c.map987.us.kg/https://www.cosmocover.com/de/newsroom-de/"
]

# 用于存储US区和DE区符合条件的超链接的列表
us_hyperlinks = []
de_hyperlinks = []

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
        # 排除基础链接和分页链接
        if ((href.startswith("https://www.cosmocover.com/newsroom/") or 
             href.startswith("https://www.cosmocover.com/de/newsroom/")) and
            href not in ["https://www.cosmocover.com/newsroom/", "https://www.cosmocover.com/newsroom/page/2/"] and
            href.count('/') > 5):
            if href not in existing_links:
                if href.startswith("https://www.cosmocover.com/newsroom/"):
                    us_hyperlinks.append(href)
                else:
                    de_hyperlinks.append(href)

# 获取当前日期
current_date = datetime.now().strftime('%Y-%m-%d')

# 用于存储最终符合条件的超链接和网盘链接
final_us_links = []
final_de_links = []

# 检查每个新超链接的网页内容是否包含"crunch"关键词
for href in us_hyperlinks:
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
            final_us_links.append((href, drive_link))
    except requests.RequestException as e:
        print(f"无法请求链接: {href}. 错误: {e}")

for href in de_hyperlinks:
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
            final_de_links.append((href, drive_link))
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
new_content = [f"### {current_date}\n", "#### us区:\n"]
for link, drive_link in final_us_links:
    # 提取文章标题
    title = link.strip('/').split('/')[-1].replace('-', ' ')
    new_content.append(f"- **{title}**\n  - [Article Link]({link})\n")
    if drive_link != 'None':
        new_content.append(f"  - [Drive Link]({drive_link})\n")

new_content.append("#### de区:\n")
for link, drive_link in final_de_links:
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
