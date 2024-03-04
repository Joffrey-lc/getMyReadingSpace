# -*- coding: utf-8 -*-
"""
 @Time    : 2022/3/13 13:32
 @Author  : LC
 @File    : utils4paperreading.py
 @Software: PyCharm
"""
import os
import shutil
import time
import requests
from bs4 import BeautifulSoup
import glob

# proxies = {'https': 'http://127.0.0.1:7890'}
proxies = {}


def checkfilename(filename: str):
    incorrect = [':', '?', '|', '<', '>', '"', '*', '/']
    for f in incorrect:
        filename = filename.replace(f, '_')
    return filename


def mymkdirs(path_dir):
    if os.path.exists(path_dir) is False:
        os.makedirs(path_dir)
        print(path_dir+'已创建')


def mypaperspace(path_paper, path_paper_list, mdinfo):
    shutil.move(src=path_paper + '.pdf', dst=os.path.join(path_paper_list, 'paper.pdf'))
    with open(path_paper_list + '\\notes.md', 'a', encoding='utf-8') as f:
        for ll in mdinfo:
            f.write(ll)


def GetPaperInfo(srcUrl):
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    #     'Accept-Encoding': 'gzip, deflate'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
               'Accept-Encoding': 'gzip, deflate, br',
               # 'Connection': 'keep-alive',
               'Connection': 'close',
               'Upgrade-Insecure-Requests': '1'}
    tt = requests.get(srcUrl, stream=True, headers=headers, proxies=proxies)
    file_size_str = len(tt.content)  # 提取出来的是个数字str
    with requests.get(srcUrl, stream=True, headers=headers, proxies=proxies) as r:  # timeout=80,stream=True
        start_n = r.text.find('xplGlobal.document.metadata=')
        end_n = r.text[start_n:].find('\n')+start_n
        Info = r.text[start_n:end_n]
        citationCount = Info.split('"citationCountPaper":')[1].split(',')[0]
        papername = Info.split('"formulaStrippedArticleTitle":"')[1].split('"')[0]
        try:
            publicationDate = Info.split('"publicationDate":"')[1].split('"')[0]
        except:
            publicationDate = 'Early Access'
        firstauthor = Info.split('"authors":[{"name":"')[1].split('"')[0]
        conferenceOrJounal = Info.split('"publicationTitle":"')[1].split('"')[0]
        return citationCount, papername, publicationDate, firstauthor, conferenceOrJounal, file_size_str


def DownOneFile(srcUrl, localFile):
    startTime = time.time()
    # headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36','Accept-Encoding': 'gzip, deflate'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
               'Accept-Encoding': 'gzip, deflate, br',
               # 'Connection': 'keep-alive',
               'Connection': 'close',
               'Upgrade-Insecure-Requests': '1'}

    with requests.get(srcUrl, stream=True, headers=headers, proxies=proxies) as r:  # timeout=80,stream=True
    # with requests.get(srcUrl, stream=True, headers=headers, proxies=proxies) as r:  # timeout=80,stream=True

        downSize = 0
        with open(localFile, 'wb') as f:
            for chunk in r.iter_content(8192):
                # if chunk:
                f.write(chunk)
                downSize += len(chunk)
                line = '\r%d KB/s - %.2f MB， 共 %.2f MB'
                line = line % (downSize / 1024 / (time.time() - startTime), downSize / 1024 / 1024, 0 / 1024 / 1024)
                print(line,end='')
        timeCost = time.time() - startTime
        line = ' 共耗时: %.2f s, 平均速度: %.2f KB/s'
        line = line % (timeCost, downSize / 1024 / timeCost)
        print(line)
        return downSize


def DownOneFile_scihub(srcUrl, localFile):
    startTime = time.time()
    # headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36','Accept-Encoding': 'gzip, deflate'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
               'Accept-Encoding': 'gzip, deflate, br',
               # 'Connection': 'keep-alive',
               'Connection': 'close',
               'Upgrade-Insecure-Requests': '1'}
    with requests.get(srcUrl, stream=True, headers=headers, proxies=proxies) as r:  # timeout=80,stream=True
    # with requests.get(srcUrl, stream=True, headers=headers, proxies=proxies) as r:  # timeout=80,stream=True

        downSize = 0
        with open(localFile, 'wb') as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
                downSize += len(chunk)
                line = '\r%d KB/s - %.2f MB， 共 %.2f MB'
                line = line % (downSize / 1024 / (time.time() - startTime), downSize / 1024 / 1024, 0 / 1024 / 1024)
                print(line,end='')
        timeCost = time.time() - startTime
        line = ' 共耗时: %.2f s, 平均速度: %.2f KB/s'
        line = line % (timeCost, downSize / 1024 / timeCost)
        print(line)
        return downSize


def search_article_scihub(artName):
    '''
    搜索论文
    ---------------
    输入：论文名
    ---------------
    输出：搜索结果（如果没有返回""，否则返回PDF链接）
    '''
    url = 'https://www.sci-hub.se/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
               'Accept-Encoding': 'gzip, deflate, br',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Content-Length': '123',
               'Origin': 'https://www.sci-hub.se',
               'Connection': 'close',
               'Upgrade-Insecure-Requests': '1'}
    data = {'sci-hub-plugin-check': '',
            'request': artName}
    res = requests.post(url, headers=headers, data=data, proxies=proxies)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    iframe = soup.find(id='pdf')
    if iframe == None:  # 未找到相应文章
        return ''
    else:
        downUrl = iframe['src']
        if 'http' not in downUrl:
            downUrl = 'https://sci-hub.se/' + downUrl
        return downUrl


def getDirNum(cwd_path, new_path):
    dir_name = glob.glob(cwd_path + '/*/')
    dir_name = [dname.split(cwd_path)[-1].replace('\\', '') for dname in dir_name]
    dir_name.remove('文章备份')
    if not dir_name:
        num_out = 1
    else:
        break_flag = 0
        for test_path in dir_name:
            if new_path in test_path:
                num_out = test_path.split('.')[0]
                break_flag = 1
        if break_flag == 0:
            num_list = [dname.split('.')[0].strip('+').strip('-').strip('~') for dname in dir_name]
            try:
                num_out = max(list(map(int, num_list))) + 1
            except:
                num_out = -1
    return num_out