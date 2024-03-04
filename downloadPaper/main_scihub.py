import glob
import time
# SCI-HUB下载要关掉梯子
from utils4paperreading import *
# 目标路径
cwd_path = r'E:\学习\项目\6G移动通信系统中的能量可持续理论与技术\准备材料_LC\提交材料\论文材料'


mymkdirs(os.path.join(cwd_path, '文章备份'))
with open(cwd_path+'\\mypaper.txt', 'r') as f:
    fail_paper = []
    for fline in f.readlines():
        paper_id = fline.split('/')[-1].strip('\n')
        citationCount, papername, publicationDate, firstauthor, conferenceOrJounal, total_size = \
            GetPaperInfo('https://ieeexplore.ieee.org/document/'+str(paper_id))
        filename = checkfilename((str(firstauthor)+'++'+str(citationCount)+'+'+str(papername)).replace(' ', '_'))
        # time.sleep(3)
        # DownOneFile('https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber='+str(paper_id)+'&ref=', cwd_path+'\\'+filename+'.pdf')
        downurl = search_article_scihub('https://ieeexplore.ieee.org/document/'+str(paper_id))
        if downurl == '':
            print('未找到相关论文，请重新搜索！:https://ieeexplore.ieee.org/document/'+ str(paper_id))
            fail_paper.append('https://ieeexplore.ieee.org/document/'+str(paper_id))
        else:
            # time.sleep(3)
            downsize = DownOneFile(downurl, cwd_path + '\\' + filename + '.pdf')
            if downsize/1024/1024 < 0.1:  # 下载的有问题
                fail_paper.append('https://ieeexplore.ieee.org/document/' + str(paper_id))
            for filename in glob.glob(cwd_path+'/*.pdf'):
                shutil.copy(src=os.path.join(cwd_path, filename), dst=os.path.join(cwd_path, '文章备份'))
                path_dir = filename.split('.pdf')[0].split('\\')[-1]
                dirnum = getDirNum(cwd_path, path_dir)
                if dirnum == -1:
                    raise OSError('There are some abnormal folders...')
                else:
                    path_dir_list = str(dirnum) + '.' + path_dir
                    mymkdirs(os.path.join(cwd_path, path_dir_list))
                    mdinfo = [
                        'Date: ' + time.strftime('%Y.%m.%d  %H:%M', time.localtime(time.time())),
                        '\n',
                        'Author: Joffrey LC',
                        '\n',
                        '\n-------------------------------------\n'
                        '**' + papername + '**.  ' + '*' + firstauthor + '*' + ' et.al.  **' + str(
                            conferenceOrJounal) + ', ' + str(
                            publicationDate) + '**  ([pdf](https://ieeexplore.ieee.org/document/' + str(
                            paper_id) + '))' + '  (Citations **' + str(citationCount) + '**)\n'
                                                                                        '## Quick Overview\n'
                    ]
                    mypaperspace(os.path.join(cwd_path, path_dir), os.path.join(cwd_path, path_dir_list), mdinfo)
    # time.sleep(3)
# 避免重复下载，删除已下载的pdf url
print('already finished')
with open(cwd_path+'\\mypaper.txt', 'w') as f:
    if fail_paper == []:
        pass
    else:
        print('-------May need to re-download-------')
        for i in range(len(fail_paper)):
            print(str(i)+'. '+fail_paper[i]+'\n')
            f.write(fail_paper[i])
            f.write('\n')
# To do:
# shutil.move 移动文件名较长的文件时会发生错误，有时间的话尝试自己写一个移动文件的代码
# 没有检测是否成功下载
