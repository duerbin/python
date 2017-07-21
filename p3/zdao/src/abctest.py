#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/18 15:34
# @Author  : dueb
# @Site    :
# @File    : kq.py
# @Software: PyCharm
import requests
import time
import urllib
import csv
from bs4 import BeautifulSoup

url = "https://www.zdao.com/user/ajaxlogin"
headers = {
    "Host": "www.zdao.com",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "www.zdao.com",
    "X-Requested-With": "XMLHttpRequest"

}



loginInfo = {"account": "18513115507", "password": "666888", "keep_login": "1", "YII_CSRF_TOKEN": "3de6f6462bda08e33dc9ecd7fb8da806"}

class Zdaoscrapy(object):
    def __init__(self):
        self.loginInfo=loginInfo
        self.entinfo=[]
        self.pergetnum=9

    def MainInit(self):
        self.session = requests.Session()
        r = self.session.get(url='https://www.zdao.com/', headers=headers)
        #print(r.cookies)
        # zdao_cookie = r.cookies["JSESSID"]
        time.sleep(5)
        resp = self.session.post(url, data=loginInfo, headers=headers)
        #print(resp.cookies)
        time.sleep(5)
        keyword='培训师'
        self.GetEntidByKeyWord(keyword)
        fcsv=open('info.csv','w',newline='')
        fwrite=csv.DictWriter(fcsv,dialect='excel',fieldnames=['name','address','email','mobile'])
        fwrite.writerows(self.entinfo)
        fcsv.close()
        self.session.close()


    def GetEntidByKeyWord(self,keyword):
        url='https://www.zdao.com/site/search?keywords=%s' % keyword
        print('GetEntidByKeyWord ',url)
        resp=self.session.get(url,headers=headers)
        cstoken=self.AnalyEntid_csrf_token(resp.text)
        if cstoken==None:
            print('[ERROR]GetEntidByKeyWord cstoken is null')
            return
        # print('GetEntidByKeyWord ',cstoken)
        urlpost = 'https://www.zdao.com/info/advanceSearch'
        header_entid = {
            "Host": "www.zdao.com",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": 'www.zdao.com',
            "X-Requested-With": "XMLHttpRequest"

        }
        #for i in range(0, 1):
        for i in range(0,self.pergetnum):
            value={'YII_CSRF_TOKEN':cstoken,'keyword':keyword,'start':i*10,'city':'','industry':'','position':''}
            i=i+1
            postdata=urllib.parse.urlencode(value)
            print ('GetEntidByKeyWord ',postdata)
            resp=self.session.post(urlpost,postdata,headers=header_entid)
            #print (resp.json())
            if resp.json()['errno']!=0:
                print('[ERROR]GetEntidByKeyWord get entid error by ',keyword)
                return
            num=resp.json()['data']['data']['num']
            print(num)
            #total = resp.json()['data']['data']['total']
            #logstr='GetEntidByKeyWord by %s Get total:%d this requests get num:%d ' % (keyword,total,num)
            #print(logstr)
            for i in range(0, num):
            #for i in range(0,1):
                iteminfo=resp.json()['data']['data']['items'][i]
                print(iteminfo['id']," begin")
                dict=[]
                try:
                    dict=self.AnalyEntMain(iteminfo['id'])
                    self.entinfo.append(dict)
                except Exception as e:
                    print(e)
                    print(iteminfo['id'], " error")
                    continue
                print(iteminfo['id'], " end")
                time.sleep(2)





    def AnalyEntMain(self,entid):
        urluser = 'https://www.zdao.com/company/%s' % entid
        print("AnalyEntMain ",urluser)
        resp = self.session.get(urluser, headers=headers)
        cstoken=self.AnalyEntid_csrf_token(resp.text)
        return self.AnalyEntid_BaesInfo(urluser,entid,cstoken)

    def AnalyEntid_BaesInfo(self,enturl,entid,cstoken):
        header_entid = {
            "Host": "www.zdao.com",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": enturl,
            "X-Requested-With": "XMLHttpRequest"

        }
        #print(header_entid)
        url='https://www.zdao.com/info/getInfo?company_id=%s&type=homepage&YII_CSRF_TOKEN=%s' % (entid,cstoken)
        print(url)
        r = self.session.get(url=url, headers=header_entid)
        if r.json()['errno']!=0:
            print("[ERROR] AnalyEntid_BaesInfo ",entid)
        entinfomap={}
        jsdata=r.json()
        if 'data' not in jsdata:
            return
        datadetail=jsdata['data']
        if 'name' in datadetail:
            entinfomap['name']=datadetail['name']
        #if 'extend_info' in datadetail and 'address' in datadetail['extend_info']:
        #    entinfomap['address'] = r.json()['data']['extend_info']['address']
        if 'contacts_mask' in datadetail:
            index=0
            contacts=datadetail['contacts_mask']
            emailstr=''
            telstr=''
            addstr=''
            for contact in contacts:
                #print(contact)
                if contact['type'] == 'mobile':
                    ciper = contact['ciphertext']
                    tel = self.AnalyEntid_telphone(enturl, ciper, entid, cstoken)
                    tags='unname%d' % index
                    if 'tag' in contact and contact['tag'] !='':
                        tags=contact['tag']
                    telstr = '%s&%s=%s' % (telstr, tags, tel)

                if contact['type']=='address':
                    addstr="%s&%s" % (addstr,contact['contact'])

                if contact['type']=='email':
                    tags = 'unemail %d' % index
                    if 'tag' in contact and contact['tag'] != '':
                        tags = contact['tag']
                    emailstr='%s&%s=%s' % (emailstr,tags,contact['contact'])

                index=index+1
            entinfomap['address'] = addstr
            entinfomap['email'] = emailstr
            entinfomap['mobile']=telstr
        return entinfomap


    def AnalyEntid_telphone(self,enturl,mask,entid,cstoken):
        header_entid = {
            "Host": "www.zdao.com",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": enturl,
            "X-Requested-With": "XMLHttpRequest"

        }
        tel="unkonwn"
        urltelphone = 'https://www.zdao.com/info/contactdecode?mask_str=%s&company_id=%s&YII_CSRF_TOKEN=%s' % (mask,entid,cstoken)
        #print(urltelphone)
        resp=self.session.get(urltelphone,headers=header_entid)
        if resp.json()['errno']==0:
            tel=resp.json()['data']['del_mask_str']
        return tel



    def AnalyEntid_csrf_token(self,responsetext):
        soup=BeautifulSoup(responsetext)
        appid=None
        #soup = BeautifulSoup(response.read())
        all_tags = soup.findAll('input', {'id': 'csrf_token'})
        for tags in all_tags:
            appid = tags['value']
        #print(appid)
        return appid


if __name__ == '__main__':
    zdtest=Zdaoscrapy()
    zdtest.MainInit()
    #zdtest.AnalyEntMain('111')
    #zdtest.AnalyInfo('test')