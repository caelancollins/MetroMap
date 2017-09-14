import selenium
from selenium import webdriver
from bs4 import BeautifulSoup, SoupStrainer
import urllib2
import re
import time


class Station:
    def __init__(self,name,link):
        self.name = name
        self.link = link

    def getNextTime(self,driver):

        driver.get(self.link)
        driver.find_element_by_css_selector('#mm-0 > div.page-wrapper.inner.station-page > div.main-content > div.container > div.content-wrapper > div > div.station-tabs-wrapper > ul > li:nth-child(3) > a > span').click()
        driver.find_element_by_css_selector('#next-train > div > div.tab-btn > span.pop-out').click()
        times1 = driver.find_element_by_id('next-train-group-1')
        times2 = driver.find_element_by_id('next-train-group-2')
        return times1,times2
        driver.quit()


def getStationLinks():
    mainListURL = 'https://www.wmata.com/rider-guide/stations/'
    html_page = urllib2.urlopen(mainListURL)
    soup = BeautifulSoup(html_page, "lxml")
    station_links = []
    for link in soup.findAll('a'):
        text = str(link.get('href'))
        if text[:21] == '/rider-guide/stations' and len(text)>25:
            station_links.append('http://www.wmata.com' + text)
    return station_links

def getStationNames(station_links):
    station_names = []
    for link in station_links:
        html = urllib2.urlopen(link)
        soup = BeautifulSoup(html, "lxml")
        title = str(soup.title)
        loc = title.index('|')
        name = title[7:loc-1]
        station_names.append(name)
    return station_names

def createStations(names, station_links):
    station_List = []
    for loc,name in enumerate(names):
        station_List.append(Station(name, station_links[loc]))
    return station_List


def main():
    station_links = getStationLinks()
    names = getStationNames(station_links)
    stationList = createStations(names, station_links)
    driver = webdriver.Chrome()
    for i in stationList:
        first,second = i.getNextTime(driver)
        nextTrain1 = first.text.split('\n', 1)[0]
        nextTrain1 = nextTrain1.split(' ')
        nextTrain2 = second.text.split('\n', 1)[0]
        nextTrain2 = nextTrain2.split(' ')
        if 'ARR' in nextTrain1 or 'ARR' in nextTrain2 or 'BRD' in nextTrain1 or 'BRD' in nextTrain2 or '1' in nextTrain1 or '1' in nextTrain2:
            if 'PASSENGER' not in nextTrain1 or 'PASSENGER' not in nextTrain2:
                print 'Train Arriving at ' + i.name




if __name__ == '__main__':
    main()
