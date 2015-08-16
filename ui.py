#!/usr/bin/env python
#coding:utf-8

import curses
import eol
import sys

class UI:

    def __init__(self):
        self.screen = curses.initscr()
        curses.cbreak()
        self.screen.keypad(1)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self.startx = 10

    def build_title(self, title):
        self.screen.clear()
        curses.noecho()
        self.screen.addstr(3, 2, title, curses.color_pair(4))
        self.screen.refresh()

    def build_login(self):
        self.display_clear()
        curses.noecho()
        self.screen.addstr(5, self.startx, '请输入你的账号')
        self.screen.addstr(7, self.startx, '学号: ')
        self.screen.addstr(8, self.startx, '密码: ')
        self.screen.move(7, 16)
        self.screen.refresh()

    def get_account(self):
        self.screen.timeout(-1)
        curses.echo()
        account = self.screen.getstr(7, 16, 15)
        return account

    def get_passwd(self):
        self.screen.timeout(-1)
        curses.noecho()
        passwd = self.screen.getstr(8, 16, 15)
        return passwd

    def build_menu(self, result, indem):
        self.display_clear()
        foo = 5
        for i in result:
            if i == indem:
                self.screen.addstr(foo, self.startx - 3, '-> ' + str(i) + ' : ' + result[i][0], curses.color_pair(2))
                foo += 1
            else:
                self.screen.addstr(foo, self.startx, str(i) + ' : ' + result[i][0])
                foo += 1
        self.screen.refresh()

    def display_clear(self):
        self.screen.move(4, 1)
        self.screen.clrtobot()
        curses.noecho()
        self.screen.refresh()

    def display_info(self, string):
        self.display_clear()
        self.screen.addstr(5, self.startx, string)
        self.screen.refresh()

carousel = lambda left, right, x: left if (x > right) else (right if x < left else x)

class MENU:

    def __init__(self):
        self.ui = UI()
        self.title = '扬州大学'
        self.index = 1
        self.satck = []
        self.menutype = 'main'
        self.main_menu = {1 : ['教学平台'], 2 : ['成绩查询']}
        self.datalist = self.main_menu

    def send_kill(self):
        curses.endwin()
        sys.exit()

    def start(self):
        self.ui.build_title(self.title)
        self.ui.build_menu(self.main_menu, self.index)

        while True:
            datalist = self.datalist
            index = self.index
            menutype = self.menutype
            key = self.ui.screen.getch()
            stack = self.satck

            if key == ord('q'):
                self.send_kill()

            if key == ord('j'):
                self.index = carousel(1, len(datalist), index + 1)

            if key == ord('k'):
                self.index = carousel(1, len(datalist), index - 1)

            if key == ord('l'):
                self.dispatch_enter(index)

            if key == ord('h'):
                up = stack.pop()
                self.menutype = up[0]
                self.title = up[1]
                self.datalist = up[2]

            self.ui.build_title(self.title)
            self.ui.build_menu(self.datalist, self.index)

    def dispatch_enter(self, idx):
        menutype = self.menutype
        title = self.title
        datalist = self.datalist
        index = self.index
        self.satck.append([menutype, title, datalist])

        if menutype == 'main':
            self.get_datatype(idx)

        elif menutype == 'eol':
            self.datalist = eol.get_lessonmesage(datalist[idx][1])
            self.menutype = 'lessonlist'

        elif menutype == 'lessonlist':
            message = eol.get_message(datalist[idx][1])
            self.menutype == 'message'
            self.ui.display_info(message)
            self.ui.screen.getch()

    def get_datatype(self, idx):
        if idx == 1:
            self.title = '扬州大学网络教学平台'
            self.menutype = 'eol'
            self.ui.build_login()
            account = self.ui.get_account()
            passwd = self.ui.get_passwd()
            eol.log_in(account, passwd)
            self.datalist = eol.get_lessonlist()

        else:
            self.title = '扬州大学成绩查询平台'
            self.menutype = 'grade'
            self.ui.build_login()



menu = MENU()
menu.start()
