# 听说你们他娘的喜欢签到？
# 注意所有要自己手动改的地方
import requests
import re
from threading import Timer
import time
import pygame

#课程标识与班级标识，需手动填入，每门课不一样
courseId=
jclassId=
#间隔时间，以秒为单位
check_time=

filepath=r"汤老师的灵魂拷问.mp3"

# 瞄准签到页面
url = 'https://mobilelearn.chaoxing.com/widget/pcpick/stu/index?courseId='+str(courseId)+'&jclassId='+str(jclassId)

header={
    'Accept':'text/html,application/xhtml+xml,ap<div id="startList">plication/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':': zh-CN,zh;q=0.9,nl;q=0.8,en;q=0.7',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    # 改cookies，必须用浏览器F12登录签到任务页面拿到你自己的cookies
    'Cookie':'',
    'Host':'mobilelearn.chaoxing.com',
    'Referer':'https://mobilelearn.chaoxing.com/widget/pcpick/stu/index?courseId='+str(courseId)+'&jclassId='+str(jclassId),
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
}

#拿到fid，估计是学校标识
fid=re.findall(r'fid=(.*?);',header['Cookie'])[0]

def qnmb():
    print('寻找签到中...')
    content=requests.get(url, headers=header).text
    content=content.replace(' ','')
    content=content.replace('\n','')
    content=content.replace('\t','')
    #print(content)
    match=re.findall(r'<divid="startList">(.*?)</div>',content, re.S|re.M)
    for s in match:
        rect=re.findall(r'<ahref="javascript:;"shape="rect">\[(.*?)\]</a>',s)[0]
        activeid=re.findall(r'onclick="activeDetail\((.*?),',s)[0]
        if rect=='签到':
            sign_url='https://mobilelearn.chaoxing.com/widget/sign/pcStuSignController/preSign?activeId='+x+'&classId='+str(jclassId)+'&fid='+str(fid)+'&courseId='+str(courseId)
            print('签到成功')
            requests.get(sign_url,headers=header)
        else:
            #如果是位置签到或者手势签到，播放汤神灵魂提示音
            pygame.mixer.init()
            track = pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            time.sleep(10)
            pygame.mixer.music.stop()


class RepeatingTimer(Timer):
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)
t = RepeatingTimer(check_time,qnmb)

t.start()


