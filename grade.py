#!/usr/bin/env python
#coding:utf-8

import requests
import os
import re

name = []
grade = []
if os.path.isfile('.gradeconfig'):
    file = open('.gradeconfig', 'r')
    some = file.read()
    some = some.split(':')
    xuehao = some[0]
    passwd = some[1]
    file.close()
else:
    xuehao = input('输入你的学号:')
    passwd = input('输入你的密码:')
    file = open('.gradeconfig', 'w+')
    file.write(xuehao + ':' + passwd)
    file.close()
loginUrl = 'http://jwweb.yzu.edu.cn:7777/pls/wwwbks/bks_login2.login'
gradeUrl = 'http://jwweb.yzu.edu.cn:7777/pls/wwwbks/bkscjcx.curscopre'
postdate = {
    'stuid':xuehao,
    'pwd':passwd
    }
session = requests.Session()
result = session.post(loginUrl, data=postdate)
result = session.get(gradeUrl)
result.encoding = 'gbk'
page = result.text
myItems = re.findall('<TR>.*?<p.*?<p.*?<p.*?>(.*?)</p>.*?<p.*?<p.*?<p.*?<p.*?<p.*?<p.*?<p.*?<p.*?>(.*?)</p>.*?<p.*?<p.*?<p.*?<p.*?</TR>', page, re.S)
for item in myItems:
    name.append(item[0])
    grade.append(item[1])
for i in range(len(name)):
    print('%s : %s\n'%(name[i], grade[i]))
input()
