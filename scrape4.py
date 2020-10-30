import bs4 as bs
import sys
import urllib.request
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
import re
import matplotlib.pyplot as plt
import numpy as np
import time
import requests


class Page(QWebEnginePage):

    def __init__(self):

        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl('https://www.flashscore.pl/mecz/SWuyfsa1/#szczegoly-meczu'))
        self.app.exec_()
        self.wynik = []
        self.minuta = 0

    def _on_load_finished(self):

        # self.app.quit()
        try:
            self.html = self.toHtml(self.Callable)
        except Exception as e:
            print(e)

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


def main():
    scrape_data([])


def scrape_data(results):
    koniec = False

    page = Page()

    while not koniec:


        refresh_page(page)

        print(re.match('Przerwa', str(page.minuta)) != None, 'asdfsadfsaf')
        # check if we have match break
        while re.match('Przerwa', str(page.minuta)) != None or int(re.findall(r'(\d+)', str(page.minuta))[2]) in results[0::3]:

            print("czekam")

            refresh_page(page)
            time.sleep(5)

            # check if the match has already ended
        if re.search(r'Koniec', str(page.minuta)):
            print("to koniec")
            koniec = True
            return

        else:
            results.append(int(re.findall(r'(\d+)', str(page.minuta))[2]))

        for i in page.wynik:
            results.append(int(re.search(r'\d+', str(i)).group(0)))

        print(results)
        print_chart(results)


        time.sleep(5)


def print_chart(results):
    print(results)
    minutes = results[0::3]
    firstTeam = np.divide(results[1::3], np.array(minutes) / 60)
    secondTeam = np.divide(results[2::3], np.array(minutes) / 60)
    sumresult = [x + y for x, y in zip(firstTeam, secondTeam)]

    print(minutes)

    plt.plot(minutes, sumresult)
    # plt.plot(minutes, secondTeam, label='team2')
    # plt.plot(minutes, sumresult, label='sum')

    plt.show(block=False)
    plt.pause(3)
    plt.close('all')
    # print("go next")


def refresh_page(page):
    page.load(QUrl('https://www.flashscore.pl/mecz/SWuyfsa1/#szczegoly-meczu'))
    page.app.exec()
    soup = bs.BeautifulSoup(page.html, 'lxml')
    page.wynik = soup.findAll('span', class_='scoreboard')
    page.minuta = soup.findAll('div', class_='info-status mstat')


if __name__ == '__main__': main()
