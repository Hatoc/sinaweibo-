import requests
from lxml import etree
import json
import time
import re
headers={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
}
for i in range(1,3): # 不够可以调整循环范围，每次抓取7-8个
    ticks=int(time.time())
    url1 = 'https://weibo.com/a/aj/transform/loadingmoreunlogin?ajwvr=6&category=0&page=%s&lefnav=0&cursor=&__rnd=%s'%(i,ticks)
    url = requests.get(url1,headers=headers)
    L = url.json()['data']
    html = etree.HTML(L)
    for i in range(1,10):
        html_href = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/@class' % (i))
        if html_href == []:
            break
        elif html_href[0] == 'UG_list_b': # 单图微博
            L1=[]
            html_address = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/@href' % (i)) # 此微博地址
            L1.append(html_address[0])
            html_img = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[1]/img/@src' % (i)) # 微博图片
            L1.append(html_img[0])
            html_text = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/h3/div//text()' % (i)) # 微博内容
            L1.append(' '.join(html_text[0:-1]))
            html_zzimg = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/div/a[1]/span/img/@src' % (i)) # 作者头像
            L1.append(html_zzimg[0])
            html_zz = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/div/a[2]/span/text()' % (i)) # 作者名字
            L1.append(html_zz[0])
            html_time = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/div/span[1]/text()' % (i)) # 发布时间
            L1.append(html_time[0])
            html_zfl = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/div/span[6]/em[2]/text()' % (i)) # 转发量
            L1.append(html_zfl[0])
            html_pls = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/div/span[4]/em[2]/text()' % (i)) # 评论数
            L1.append(html_pls[0])
            html_dzs = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/div/span[2]/em[2]/text()' % (i)) # 点赞数
            L1.append(html_dzs[0])
            print(L1)
            # 加个判断条件加入mysql或者redis
        elif html_href[0] == 'UG_list_a': # 四图微博
            L2=[]
            html_address = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/@href' % (i)) # 此微博地址
            L2.append(html_address[0])
            html_img = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[1]/div/img/@src' % (i)) # 微博图片
            L2.append(html_img)
            html_text = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/h3/div//text()' % (i)) # 微博内容
            L2.append(' '.join(html_text[0:-1]))
            html_zzimg = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/a[1]/span/img/@src' % (i)) # 作者头像
            L2.append(html_zzimg[0])
            html_zz = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/a[2]/span/text()' % (i)) # 作者名字
            L2.append(html_zz[0])
            html_time = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/span[1]/text()' % (i)) # 发布时间
            L2.append(html_time[0])
            html_zfl = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/span[6]/em[2]/text()' % (i)) # 转发量
            L2.append(html_zfl[0])
            html_pls = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/span[4]/em[2]/text()' % (i)) # 评论数
            L2.append(html_pls[0])
            html_dzs = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/span[2]/em[2]/text()' % (i)) # 点赞数
            L2.append(html_dzs[0])
            print(L2)
            # 加个判断条件加入mysql或者redis
        elif html_href[0] == 'UG_list_v2 clearfix': # 视频微博
            L3=[]
            html_address = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/@href' % (i)) # 此微博地址
            L3.append(html_address[0])
            html_img = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[1]/@action-data' % (i)) # 微博图片
            pattern = re.compile(r'cover_img=(.+?)&card')
            html_img = pattern.findall(html_img[0])
            html_img = html_img[0].replace('%3A',':')
            html_img = html_img.replace('%2F','/')
            L3.append(html_img)
            html_text = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/h3//text()' % (i)) # 微博内容
            L3.append(' '.join(html_text[0:-1]))
            html_zzimg = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/div/a[1]/span/img/@src' % (i)) # 作者头像
            L3.append(html_zzimg[0])
            html_zz = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/div/a[2]/span/text()' % (i)) # 作者名字
            L3.append(html_zz[0])
            html_time = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/div/span[1]/text()' % (i)) # 发布时间
            L3.append(html_time[0])
            html_zfl = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/div[2]/span[5]/em[2]/text()' % (i)) # 转发量
            L3.append(html_zfl[0])
            html_pls = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/div[2]/span[3]/em[2]/text()' % (i)) # 评论数
            L3.append(html_pls[0])
            html_dzs = html.xpath('//*[@class="pt_ul clearfix"]/div[%s]/div[2]/div[2]/span[1]/em[2]/text()' % (i)) # 点赞数
            L3.append(html_dzs[0])
            print(L3)
            # 加个判断条件加入mysql或者redis