# 听说你们他娘的喜欢签到？
# 注意所有要自己手动改的地方
import requests
import re
from threading import Timer
import time
import pygame

#课程标识与班级标识，需手动填入，每门课不一样
courseId=119090594
jclassId=16687118
#间隔时间，以秒为单位
check_time=5

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
    'Cookie':'fanyamoocs=33CB35EC6AEAFAA411401F839C536D9E; thirdRegist=0; cookiecheck=true; duxiu=userName%5fdsr%2c%3dtfm%2c%21userid%5fdsr%2c%3d23224%2c%21char%5fdsr%2c%3d%u4eae%2c%21metaType%2c%3d265%2c%21dsr%5ffrom%2c%3d1%2c%21logo%5fdsr%2c%3dlogo0408%2ejpg%2c%21logosmall%5fdsr%2c%3dsmall0408%2ejpg%2c%21title%5fdsr%2c%3d%u957f%u6625%u5927%u5b66%2c%21url%5fdsr%2c%3d%2c%21compcode%5fdsr%2c%3d1365%2c%21province%5fdsr%2c%3d%u5409%u6797%2c%21readDom%2c%3d%2c%21isdomain%2c%3d3%2c%21showcol%2c%3d0%2c%21hu%2c%3d0%2c%21areaid%2c%3d0%2c%21uscol%2c%3d0%2c%21isfirst%2c%3d0%2c%21istest%2c%3d0%2c%21cdb%2c%3d0%2c%21og%2c%3d0%2c%21ogvalue%2c%3d0%2c%21testornot%2c%3d1%2c%21remind%2c%3d0%2c%21datecount%2c%3d3595%2c%21userIPType%2c%3d1%2c%21my%2c%3d1%2c%21lt%2c%3d0%2c%21ttt%2c%3dfxlogin%2echaoxing%2c%21enc%5fdsr%2c%3dD871CE8604258E9D0E371BCBBA75DF1B; AID_dsr=1464; superlib=""; msign_dsr=1582863258812; search_uuid=300bb3a0%2d6be7%2d4531%2db79e%2d1388d71ded75; mqs=19e3b526c24d6396a7ea92ca8215ac45b2684007674e38588d7c2e084ce6404e6d58f013518d47b7966204b865bf74394b6aea37199a56bd93d7dbcf626de5e488fa342e4b563d66e4446bf79392c19a02314436a8b0093e365c78dfd413b0dbb19dcedeb7f5f9945d45b80c90375f74; isfyportal=1; uname=041740320; fid=12924; pid=29854; _uid=53376827; uf=b2d2c93beefa90dcec80ea307a17a5911977fcf2b85c9664c4fbfc4c6dd2d060ff2b64f12d31784121f4a545a91e945d913b662843f1f4ad6d92e371d7fdf644d19cfe10affb40b78b6f06f3c6e4d7761471850d8bf7e34cec159d88001747f27eaa6ae7f4e244be; _d=1583038324493; UID=53376827; vc=1465378228BCD13703C9C3493395D8D4; vc2=61FB103B17813F2E06549F537DB6A74E; vc3=NKZo%2F0y%2FG26oeZttbgpKifE3BtI76T5A2i2U7F8P5bjIC8oXys89utOxEniLk8NMRCzTk%2FCFrLiCoMUni8l9f2von7THW9gHqqhbKGtAMjA%2FZ1FRZOZx7ilxS0YGpjTZ7UR8QWARF%2FdoSBmTFOQh8bKYZzFxE%2F%2Bw85Il1Xvy0oM%3D05dfd793bdef96e491e64e406d304978; xxtenc=94bf24a0d8235e0ea04ad7ccf8546d64; DSSTASH_LOG=C_38-UN_1464-US_53376827-T_1583038324495; route=f68f57a38c2d3c2c9e08b41c6b6d985e',
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
    match=re.findall(r'<divid="startList">(.*?)</div>',content, re.S|re.M)
    print(match[0])
    if match[0] != '':
        for s in match:
            activeid=re.findall(r'onclick="activeDetail\((.*?),',s)[0]
            sign_url='https://mobilelearn.chaoxing.com/widget/sign/pcStuSignController/preSign?activeId='+str(activeid)+'&classId='+str(jclassId)+'&fid='+str(fid)+'&courseId='+str(courseId)
            print('签到成功')
            requests.get(sign_url,headers=header)
            print(sign_url)
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


