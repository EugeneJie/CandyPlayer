from video import Video
import PIL.Image
import PIL.ImageTk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import os
import io


class Player:
    def __init__(self):
        self.win = Tk()
        self.win.iconbitmap('res/icon.ico')
        self.win.title('CandyPlayer')
        self.win.resizable(0, 0)
        self.v = Video()

        msg = "操作说明：" \
              "\n1、使用本软件前请先安装Chrome(谷歌浏览器)，然后将其快捷方式复制到与本软件相同的文件目录下，"\
              "并命名为“chrome”。此外，请允许Chrome使用Flash以播放视频。"\
              "\n\n2、本软件中的搜索功能是基于腾讯视频全网搜服务的，您可以用它搜索到各大主流视频网站的视频资源。"\
              "当选择快速搜索时仅展示与搜索内容相关的前几个条目；选择详细搜索可以展示更多的条目，但是"\
              "需要等待更长的时间。"\
              "\n\n3、本软件左侧区域列表为搜索结果，双击某一搜索结果将会在中间区域展示视频海报以及相关信息，"\
              "在右侧区域展示该视频的剧集资源。双击右侧列表中的某一剧集资源，本软件会将该资源的播放地址"\
              "插入到地址栏。"\
              "\n\n4、当选择解析播放时，本软件会对地址栏中的播放地址进行解析并播放，无广告观看VIP视频！"\
              "当选择原址播放时，本软件会直接打开地址栏中的播放页面。"\
              "\n\n5、播放页面为全屏显示，在播放过程中，您随时可以通过“Ctrl+W”来退出播放界面，" \
              "若无法退出播放界面，则可以通过“Win+D”来回到桌面，再关闭浏览器窗口。"\
              "\n\n6、除了通过搜索的方式将播放地址添加到地址栏，您还可以手动将播放地址插入到地址栏，支持各大"\
              "主流视频网站的视频解析。注意：播放地址为视频网站上具体的某一视频的播放页面地址。"\
              "\n\n7、本软件仅供学习和研究使用，禁止用于商业用途！本软件使用的是第三方视频解析接口，不收集和"\
              "存储任何视频资源！项目地址：https://github.com/EugeneJie/CandyPlayer。"

        self.query = StringVar()
        self.search_tp = StringVar()
        self.url_field = StringVar()
        self.play_tp = StringVar()
        self.desc = StringVar()
        self.desc.set(msg)
        self.bottom_text = StringVar()

        self.l_search = Label(self.win, text='全网搜：')
        self.e_search = Entry(self.win, width=50, textvariable=self.query)
        self.e_search.bind('<Return>', self.search)

        self.cb_search_tp = Combobox(self.win, width=8, textvariable=self.search_tp)
        self.cb_search_tp['values'] = ('快速搜索', '详细搜索')
        self.cb_search_tp.config(state='readonly')
        self.cb_search_tp.current(0)
        
        self.b_search = Button(self.win, text='搜索', command=self.search)

        self.l_url = Label(self.win, text='地址栏：')
        self.e_url = Entry(self.win, width=50, textvariable=self.url_field)
        self.e_url.bind('<Return>', self.play)
        
        self.cb_play_tp = Combobox(self.win, width=8, textvariable=self.play_tp)
        self.cb_play_tp['values'] = ('解析播放1', '解析播放2', '解析播放3', '原址播放')
        self.cb_play_tp.config(state='readonly')
        self.cb_play_tp.current(0)
        
        self.b_play = Button(self.win, text='播放', command=self.play)

        # -----结果展示区域-----
        self.f_info = Frame(self.win)
        self.lb1 = Listbox(self.f_info, width=20, selectmode=SINGLE)
        self.sbv1 = Scrollbar(self.f_info, orient=VERTICAL)
        self.sbh1 = Scrollbar(self.f_info, orient=HORIZONTAL)
        self.sbv1.config(command=self.lb1.yview)
        self.sbh1.config(command=self.lb1.xview)
        self.lb1.config(yscrollcommand=self.sbv1.set, xscrollcommand=self.sbh1.set)

        self.l_pic = Label(self.f_info)
        self.img = PIL.Image.open('res/readme.jpg')
        self.pic = PIL.ImageTk.PhotoImage(self.img)
        self.l_pic.config(image=self.pic)
        self.l_desc = Label(self.f_info, width=75, wraplength=520, textvariable=self.desc)

        self.lb2 = Listbox(self.f_info, width=20, selectmode=SINGLE)
        self.sbv2 = Scrollbar(self.f_info, orient=VERTICAL)
        self.sbh2 = Scrollbar(self.f_info, orient=HORIZONTAL)
        self.sbv2.config(command=self.lb2.yview)
        self.sbh2.config(command=self.lb2.xview)
        self.lb2.config(yscrollcommand=self.sbv2.set, xscrollcommand=self.sbh2.set)

        self.l_bottom = Label(self.f_info, textvariable=self.bottom_text)

        self.lb1.grid(row=0, column=0, sticky=N+S+E+W)
        self.sbv1.grid(row=0, column=1, stick=N+S)
        self.sbh1.grid(row=1, column=0, sticky=E+W)

        self.l_pic.grid(row=0, column=2, stick=N+S)
        self.l_desc.grid(row=0, column=3, sticky=N+W)

        self.lb2.grid(row=0, column=4, sticky=N+S+E+W)
        self.sbv2.grid(row=0, column=5, stick=N+S)
        self.sbh2.grid(row=1, column=4, sticky=E+W)

        self.l_bottom.grid(row=1, column=2, columnspan=2, sticky=N+S+E+W)

        # -------------------------
        Label(self.win, width=30).grid(row=0, column=0, rowspan=2)
        self.l_search.grid(row=0, column=1)
        self.e_search.grid(row=0, column=2)
        self.cb_search_tp.grid(row=0, column=3, sticky=W)
        self.b_search.grid(row=0, column=4)
        Label(self.win, width=30).grid(row=0, column=5, rowspan=2)

        self.l_url.grid(row=1, column=1)
        self.e_url.grid(row=1, column=2)
        self.cb_play_tp.grid(row=1, column=3, sticky=W)
        self.b_play.grid(row=1, column=4)

        self.f_info.grid(row=2, column=0, columnspan=6)

        self.win.mainloop()

    def search(self, *args):
        self.bottom_text.set('正在搜索...')
        self.f_info.update()
        q = self.query.get() + ' '
        flag = 0 if self.search_tp.get() == '快速搜索' else 1
        names, descs, subs, tps, covers, hrefs = self.v.get_result(q, flag)
        self.lb1.delete(0, END)
        self.lb2.delete(0, END)
        for name in names:
            self.lb1.insert(END, name)
        self.bottom_text.set('共找到%d个结果' % len(names))

        def display_info(*args):
            cur_index = self.lb1.curselection()[0]
            # print(self.lb1.get(self.lb1.curselection()))

            img_content = self.v.get_img_content(covers[cur_index])
            img_data = io.BytesIO(img_content)
            self.img = PIL.Image.open(img_data)
            self.pic = PIL.ImageTk.PhotoImage(self.img)
            self.l_pic.config(image=self.pic)

            msg = '名称：' + names[cur_index] + '   ' + subs[cur_index] + '   [' + tps[cur_index] + ']\n\n' + '简介：' + descs[cur_index]
            self.desc.set(msg)

            self.lb2.delete(0, END)
            playlist = self.v.get_info(hrefs[cur_index], tps[cur_index])
            for item in playlist:
                self.lb2.insert(END, item[1][1])
            self.bottom_text.set('%s共有 %d 集' % (names[cur_index], len(playlist)))

            def add_url(*args):
                lb2_index = self.lb2.curselection()[0]

                url = playlist[lb2_index][1][0]
                title = playlist[lb2_index][1][1]
                self.url_field.set(url)

                self.bottom_text.set('已将 %s 的播放地址插入到地址栏！' % title)

            self.lb2.bind('<Double-Button-1>', add_url)

        self.lb1.bind('<Double-Button-1>', display_info)

    def play(self, *args):
        if not os.path.exists('chrome.lnk'):
            msg = '    请将谷歌浏览器的快捷方式复制到与本软件相同的文件目录下，\n并命名为“chrome”！！！'
            messagebox.showerror(title='未找到快捷方式chrome', message=msg)
        else:
            url = self.url_field.get()
            if not url:
                messagebox.showerror(title='地址栏为空', message='地址栏不能为空！请通过搜索方式或手动添加播放地址到地址栏！')
            else:
                play_tp = self.play_tp.get()
                if play_tp == '解析播放1':
                    url = 'http://www.tg321.cn/jx?url=' + url
                if play_tp == '解析播放2':
                    url = 'http://wq114.org:88/tong.php?url=' + url
                if play_tp == '解析播放3':
                    url = 'http://www.wmxz.wang/video.php?url=' + url
                os.system('taskkill/F /IM chrome.exe')
                os.system('chrome.lnk --incognito --kiosk \"%s\"' % url)


if __name__ == "__main__":
    Player()
