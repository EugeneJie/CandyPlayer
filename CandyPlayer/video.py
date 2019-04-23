import requests
from bs4 import BeautifulSoup


class Video:
    def __init__(self):
        self.header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}
        
    def get_result(self, q, flag=0):
        names = []
        descs = []
        subs = []
        tps = []
        covers = []
        hrefs = []        
        pages = 1

        url = 'https://v.qq.com/x/search/?q=%s' % q
        r = requests.get(url, headers=self.header)
        soup = BeautifulSoup(r.content, 'lxml')

        if flag == 0:
            pages = 1
        else:        
            info = soup.find('div',class_='search_container')
            if info:
                try:
                    info = info.get('r-props').split('pages:')[1].split(';')[0]
                    pages = eval(info)                    
                except:
                    pages = 20
        
        for i in range(1, pages+1):
            url = 'https://v.qq.com/x/search/?q=%s&cur=%d' % (q, i)
            r = requests.get(url,headers=self.header)
            soup = BeautifulSoup(r.content, 'lxml')
            results = soup.findAll('div', class_='_infos')

            for result in results:
                href = result.find('a').get('href')
                if href in hrefs:
                    continue
                name = result.find('a').find('img').get('alt').replace('\x05', '').replace('\x06', '')
                try:
                    desc = [i for i in result.find('span', class_='desc_text')._all_strings()][0].replace('\u3000', ' ')
                except:
                    desc = '（无）'
                sub = result.find('span', class_='sub')
                if sub:
                    sub = sub.string.strip()
                else:
                    sub = ''
                tp = result.find('span', class_='type').string
                cover = 'https:' + result.find('a').find('img').get('src')

                names.append(name)
                descs.append(desc)
                subs.append(sub)
                tps.append(tp)
                covers.append(cover)
                hrefs.append(href)
            
        return names, descs, subs, tps, covers, hrefs

    def get_img_content(self, url):
        r = requests.get(url, headers=self.header)
        return r.content

    def get_info(self, href, tp):
        playlist = {}
        
        vid = href.split('/')[-1].replace('.html','')

        if tp=='电影':
            tpid = 2
        elif tp=='电视剧' or tp=='动漫':
            tpid = 4
        else:
            tpid = 0

        if tpid==0:
            for tp in [1, 4]:
                url = 'https://s.video.qq.com/get_playsource?id=%s&type=%d&range=1-10000' % (vid, tp)
                r = requests.get(url, headers=self.header)
                soup = BeautifulSoup(r.content, 'lxml')
                results = soup.findAll('videoplaylist')
                
                for result in results:
                    number = result.find('episode_number').string
                    if number in playlist:
                        continue
                    playurl = result.find('playurl').string
                    title = result.find('title').string

                    playlist[number] = [playurl, title]

            r = requests.get(href, headers=self.header)
            soup = BeautifulSoup(r.content, 'lxml')
            info = soup.find('div',class_='mod_row mod_row_episode')
            if info:
                try:
                    info = info.get('r-props').split('groups:')[1].split(';')[0]
                    date = eval(info)                    

                    for year,months in date.items():
                        for month in months:
                            url = 'https://s.video.qq.com/get_playsource?id=%s&type=4&range=1-10000&year=%s&month=%s' % (vid, year, month)
                            r = requests.get(url, headers=self.header)
                            soup = BeautifulSoup(r.content, 'lxml')
                            results = soup.findAll('videoplaylist')
                            for result in results:
                                number = result.find('episode_number').string
                                if number in playlist:
                                    continue
                                playurl = result.find('playurl').string
                                title = result.find('title').string

                                playlist[number] = [playurl, title]
                except:
                    pass
        else:
            url = 'https://s.video.qq.com/get_playsource?id=%s&type=%d&range=1-10000' % (vid, tpid)

            r = requests.get(url, headers=self.header)
            soup = BeautifulSoup(r.content, 'lxml')
            results = soup.findAll('videoplaylist')

            for result in results:
                number = result.find('episode_number').string
                playurl = result.find('playurl').string
                title = result.find('title').string

                playlist[number] = [playurl, title]

        if tpid == 0:
            playlist = sorted(playlist.items(), key=lambda item: item[0])
        else:
            playlist = list(playlist.items())

        return playlist
