from urllib import response
from urllib.request import urlopen
from bs4 import BeautifulSoup
import threading


class PageBot(threading.Thread):
    INDEX = ''
    INDEXCONTENT = ''
    IMAGES = {}

    def __init__(self, indexpage,updaterate=None) -> None:
        self.updaterate = updaterate
        threading.Thread.__init__(self)
        self.INDEX = indexpage

    def parseimages(self):
        soup = BeautifulSoup(self.INDEXCONTENT,features="html.parser")
        images = soup.find_all('img')
        for img in images:
            self.IMAGES[img.get('src')]=None

    def getimages(self):
        for src in self.IMAGES.keys():
            try:
                response = urlopen(src)
                self.IMAGES[src] = response.read()
            except Exception as e:
                print(e)

    def run(self):
        print('GET:', self.INDEX)
        try:
            response = urlopen(self.INDEX)
            self.INDEXCONTENT = response.read()
            self.parseimages()
            self.getimages()
            return self.INDEXCONTENT
        except Exception as e:
            print(e)
