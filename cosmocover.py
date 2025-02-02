import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 目标URL列表
urls = [
    "https://www.cosmocover.com/newsroom/",
    "https://c.map987.us.kg/https://www.cosmocover.com/de/newsroom-de/"
]

# 用于存储所有符合条件的超链接的集合
all_hyperlinks = set()

# 读取现有的文章链接
existing_links = set()
try:
    with open('hyperlinks.txt', 'r', encoding='utf-8') as file:
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

    # 提取符合条件的超链接并添加到集合中，确保去重
    for link in links:
        href = link['href']
        if (href.startswith("https://www.cosmocover.com/newsroom/") or 
            href.startswith("https://www.cosmocover.com/de/newsroom/")):

            all_hyperlinks.add(href)

# 找出新的文章链接
new_links = all_hyperlinks - existing_links
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

import os

if os.path.exists('hyperlinks.txt'):
    with open('hyperlinks.txt', mode='r', encoding='utf-8') as ff:
        print(ff.readlines())
else:
    with open("hyperlinks.txt", mode='w', encoding='utf-8') as ff:
        print("文件创建成功！")

# 将符合条件的超链接和网盘链接写入txt文件
with open('hyperlinks.txt', 'r+', encoding='utf-8') as file:
    content = file.read()
    file.seek(0, 0)
    file.write(f"{current_date}\n")
    for link, drive_link in final_links:
        file.write(str(link) + '\n' + str(drive_link) + '\n')
    file.write('\n' + content)

print("符合条件的超链接和网盘链接已成功写入到hyperlinks.txt文件中。")




"""
python /storage/emulated/0/1hosts/cosmocover.py
遇到了已经有的文章，跳过


{'https://www.cosmocover.com/de/newsroom/like-a-dragon-direct-enthuellt-neues-gameplay-von-like-a-dragon-pirate-yakuza-in-hawaii/', 'https://www.cosmocover.com/de/newsroom/magilumiere-inc-ist-jetzt-erhaeltlich-veroeffentlicht-von-crunchyroll/', 'https://www.cosmocover.com/de/newsroom/sega-teasert-sonic-racing-crossworlds-projekt-century-und-neues-virtua-fighter-projekt-bei-den-game-awards-2024/', 'https://www.cosmocover.com/de/newsroom/sega-und-ryu-ga-gotoku-studios-kuendigen-like-a-dragon-direct-fuer-den-9-januar-2025-an/', 'https://www.cosmocover.com/de/newsroom/clair-obscur-expedition-33-erscheint-am-24-april-2025/', 'https://www.cosmocover.com/de/newsroom/crunchyroll-feiert-den-valentinstag-mit-kostenlosen-rom-coms-im-februar/', 'https://www.cosmocover.com/de/newsroom/crunchyroll-kuendigt-veroeffentlichungsplan-fuer-home-entertainment-an-februar-april-2025/', 'https://www.cosmocover.com/de/newsroom/virtua-fighter-5-r-e-v-o-jetzt-auf-steam-erhaeltlich-neuer-launch-trailer/', 'https://www.cosmocover.com/de/newsroom/solo-leveling-kehrt-mit-staffel-2-arise-from-the-shadow-zurueck-auf-crunchyroll/', 'https://www.cosmocover.com/de/newsroom/von-den-machern-von-sifu-rematch-ein-online-multiplayer-fussballerlebnis/', 'https://www.cosmocover.com/de/newsroom/tinybuild-kuendigt-postapokalyptischen-physikbasierten-city-builder-all-will-fall-an-der-2025-auf-steam-erscheint/', 'https://www.cosmocover.com/de/newsroom/sonic-x-shadow-generations-sonic-the-hedgehog-3-%e2%80%92-filmpaket-ab-sofort-verfuegbar/', 'https://www.cosmocover.com/de/newsroom/crunchyroll-kuendigt-die-winter-anime-saison-2025-an/', 'https://www.cosmocover.com/de/newsroom/baue-dein-koenigreich-im-block-stapel-strategie-hybrid-drop-duchy-feiert-heute-demo-debuet-vollversion-bestaetigt-fuer-april-2025-auf-pc/', 'https://www.cosmocover.com/de/newsroom/crunchyroll-praesentiert-trailer-fuer-attack-on-titan-the-last-attack/', 'https://www.cosmocover.com/de/newsroom/among-us-wird-teil-der-super-monkey-ball-banana-rumble%ef%b8%8f-crew/', 'https://www.cosmocover.com/de/newsroom/crunchyroll-gibt-veroeffentlichungsdaten-fuer-nordamerika-deutschland-und-ausgewaehlte-internationale-kinostarts-von-attack-on-titan-the-last-attack-bekannt/', 'https://www.cosmocover.com/de/newsroom/entkomme-einem-albtraumhaften-lebenden-labyrinth-in-der-surrealistischen-mystischen-welt-von-moroi-das-anfang-2025-fuer-pc-erscheint/', 'https://www.cosmocover.com/de/newsroom/crunchyroll-aniplex-sony-music-und-playstation-productions-produzieren-anime-serie-basierend-auf-ghost-of-tsushima-legends/', 'https://www.cosmocover.com/de/newsroom/crashkurs-fuer-museumsmanager-im-neuen-video-zu-two-point-museum/'}
______________ 上面是找出的新的文章链接
{'https://www.cosmocover.com/de/newsroom/magilumiere-inc-ist-jetzt-erhaeltlich-veroeffentlicht-von-crunchyroll/', 'https://www.cosmocover.com/de/newsroom/crunchyroll-feiert-den-valentinstag-mit-kostenlosen-rom-coms-im-februar/', 'https://www.cosmocover.com/de/newsroom/crunchyroll-kuendigt-veroeffentlichungsplan-fuer-home-entertainment-an-februar-april-2025/', 'https://drive.google.com/drive/folders/1VhhlrmeTpDLqJYkcb91SGf_MqBFXx-6C?usp=drive_link', 'https://www.cosmocover.com/newsroom/crunchyroll-celebrates-valentines-day-with-free-rom-coms-in-february/', 'https://www.cosmocover.com/newsroom/crunchyroll-announces-the-winter-2025-anime-season/', 'https://www.cosmocover.com/de/newsroom/solo-leveling-kehrt-mit-staffel-2-arise-from-the-shadow-zurueck-auf-crunchyroll/', 'https://www.cosmocover.com/newsroom/crunchyroll-announce-home-entertainment-release-schedule-february-april-2025/', 'https://drive.google.com/drive/folders/10LNnbsy4WxAjdFc_KhNd_L700vzZ1LXc', 'https://drive.google.com/drive/folders/1TOOYefa3m-hhVac7YuXNtsHJcn9JBrO7', 'https://www.cosmocover.com/newsroom/page/2/', 'https://www.cosmocover.com/newsroom/crunchyroll-aniplex-sony-music-and-playstation-productions-to-produce-anime-series-based-on-ghost-of-tsushima-legends/', 'https://drive.google.com/drive/folders/1CLUJnm77NGaD6Hjvg_yav-84s-QkE9Cd?usp=drive_link', 'https://www.cosmocover.com/newsroom/', 'https://www.cosmocover.com/de/newsroom/crunchyroll-kuendigt-die-winter-anime-saison-2025-an/', 'https://www.cosmocover.com/de/newsroom/crunchyroll-praesentiert-trailer-fuer-attack-on-titan-the-last-attack/', 'https://www.cosmocover.com/de/newsroom/crunchyroll-gibt-veroeffentlichungsdaten-fuer-nordamerika-deutschland-und-ausgewaehlte-internationale-kinostarts-von-attack-on-titan-the-last-attack-bekannt/', 'https://drive.google.com/drive/folders/1qkE99m4OhtoulzR1Rpzd8_RQkTtb0-_L?usp=drive_link', 'https://drive.google.com/drive/folders/1TOOYefa3m-hhVac7YuXNtsHJcn9JBrO7?usp=drive_link', 'https://www.cosmocover.com/de/newsroom/crunchyroll-aniplex-sony-music-und-playstation-productions-produzieren-anime-serie-basierend-auf-ghost-of-tsushima-legends/', 'https://drive.google.com/drive/folders/1sbRlUzO3bgG03od-vSAj_RpCcB1N-Jsk?usp=drive_link'}
______________ 上面是txt已经有的老的文章链接



无法请求链接: https://www.cosmocover.com/de/newsroom/crashkurs-fuer-museumsmanager-im-neuen-video-zu-two-point-museum/. 错误: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
['2025-02-01\n', 'https://www.cosmocover.com/newsroom/crunchyroll-announces-the-winter-2025-anime-season/\n', 'https://drive.google.com/drive/folders/1CLUJnm77NGaD6Hjvg_yav-84s-QkE9Cd?usp=drive_link\n', 'https://www.cosmocover.com/newsroom/crunchyroll-celebrates-valentines-day-with-free-rom-coms-in-february/\n', 'https://drive.google.com/drive/folders/1VhhlrmeTpDLqJYkcb91SGf_MqBFXx-6C?usp=drive_link\n', 'https://www.cosmocover.com/newsroom/page/2/\n', 'None\n', 'https://www.cosmocover.com/newsroom/crunchyroll-announce-home-entertainment-release-schedule-february-april-2025/\n', 'https://drive.google.com/drive/folders/1TOOYefa3m-hhVac7YuXNtsHJcn9JBrO7?usp=drive_link\n', 'https://www.cosmocover.com/newsroom/crunchyroll-aniplex-sony-music-and-playstation-productions-to-produce-anime-series-based-on-ghost-of-tsushima-legends/\n', 'None\n', '\n', '2025-02-01\n', '\n', '2025-02-01\n', 'https://www.cosmocover.com/de/newsroom/crunchyroll-praesentiert-trailer-fuer-attack-on-titan-the-last-attack/\n', 'None\n', 'https://www.cosmocover.com/newsroom/\n', 'None\n', 'https://www.cosmocover.com/de/newsroom/crunchyroll-gibt-veroeffentlichungsdaten-fuer-nordamerika-deutschland-und-ausgewaehlte-internationale-kinostarts-von-attack-on-titan-the-last-attack-bekannt/\n', 'https://drive.google.com/drive/folders/10LNnbsy4WxAjdFc_KhNd_L700vzZ1LXc\n', 'https://www.cosmocover.com/de/newsroom/crunchyroll-aniplex-sony-music-und-playstation-productions-produzieren-anime-serie-basierend-auf-ghost-of-tsushima-legends/\n', 'None\n', 'https://www.cosmocover.com/de/newsroom/crunchyroll-kuendigt-veroeffentlichungsplan-fuer-home-entertainment-an-februar-april-2025/\n', 'https://drive.google.com/drive/folders/1TOOYefa3m-hhVac7YuXNtsHJcn9JBrO7\n', 'https://www.cosmocover.com/de/newsroom/magilumiere-inc-ist-jetzt-erhaeltlich-veroeffentlicht-von-crunchyroll/\n', 'https://drive.google.com/drive/folders/1sbRlUzO3bgG03od-vSAj_RpCcB1N-Jsk?usp=drive_link\n', 'https://www.cosmocover.com/de/newsroom/solo-leveling-kehrt-mit-staffel-2-arise-from-the-shadow-zurueck-auf-crunchyroll/\n', 'https://drive.google.com/drive/folders/1qkE99m4OhtoulzR1Rpzd8_RQkTtb0-_L?usp=drive_link\n', 'https://www.cosmocover.com/de/newsroom/crunchyroll-kuendigt-die-winter-anime-saison-2025-an/\n', 'https://drive.google.com/drive/folders/1CLUJnm77NGaD6Hjvg_yav-84s-QkE9Cd?usp=drive_link\n', 'https://www.cosmocover.com/de/newsroom/crunchyroll-feiert-den-valentinstag-mit-kostenlosen-rom-coms-im-februar/\n', 'https://drive.google.com/drive/folders/1VhhlrmeTpDLqJYkcb91SGf_MqBFXx-6C?usp=drive_link\n', '\n']
符合条件的超链接和网盘链接已成功写入到hyperlinks.txt文件中。
"""
