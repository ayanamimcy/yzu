#!/usr/bin/env python
#coding:utf-8

import requests
import re
import bs4
from collections import OrderedDict

session = requests.Session()

def log_in(name, passwd):
    loginurl = 'http://eol.yzu.edu.cn/meol/homepage/common/login.jsp'
    post = {
        'IPT_LOGINUSERNAME':name,
        'IPT_LOGINPASSWORD':passwd
        }
    session.post(loginurl, data=post)

def get_mainpage():
    url = 'http://eol.yzu.edu.cn/meol/welcomepage/student/index.jsp'

def get_lessonlist():
    url = 'http://eol.yzu.edu.cn/meol/lesson/blen.student.lesson.list.jsp'
    message = OrderedDict()
    page = session.get(url)
    space = r'\s+'
    page = re.sub(space, '', page.text)
    find = '<tr.*?><td><ahref=".*?id=(.*?)".*?>(.*?)</a></td><td.*?>(.*?)</td><td.*?>(.*?)</td>'
    n = 1
    result = re.findall(find, page)
    for item in result:
        message[n] = [item[1], item[0], item[2], item[3]]
        n += 1
    return message

def get_lessonmesage(courseId):
    url = 'http://eol.yzu.edu.cn/meol/article/ListNews.do?courseId='
    lesson = OrderedDict()
    url = url + courseId
    page = session.get(url)
    page = bs4.BeautifulSoup(page.text)
    page = page.find_all(target="_blank", href=re.compile('course'))
    n = 1
    for i in page:
        result = i.attrs
        lesson[n] = [result['title'], result['href']]
        n += 1
    return lesson

def get_message(url):
    baseurl = 'http://eol.yzu.edu.cn'
    url = baseurl + url
    page = session.get(url)
    page = bs4.BeautifulSoup(page.text)
    page = page.find(class_='abody')
    result = page.contents[0].attrs['value']
    result = re.sub('<.*?>', '', result)
    return result
