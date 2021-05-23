#  REQUIREMENTS
#  ---------------
#  beautifulsoup4
#  requests
#  
#  How To install Requirements
#  ----------------------------
#
#  Use The Following Commands
#  pip3 install beautifulsoup4
#  pip3 install requests
#
#  How To Use The Scrapper
#  -------------------------
#
#  py proxy.py -p TYPE_of_Proxies_You_Want (http, https, socks4, socks5)
#
#  About
#  ------
#  By Younes El ALAMI @elephormy
#
#
import requests
from bs4 import BeautifulSoup
import threading
import os
import asyncio
import argparse

FilePath = ''
proxyType = ''


# https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all

def proxyScraper(proxytype, timeout, country):
    response = requests.get("https://api.proxyscrape.com/?request=getproxies&proxytype=" + proxytype + "&timeout=" + timeout + "&country=" + country)
    proxies = response.text
    with open(FilePath, "a") as txt_file:
        txt_file.write(proxies)

# Men had site proxy-list.download
def proxyListDownloadScraper(url, type, anon):
    session = requests.session()
    url = url + '?type=' + type + '&anon=' + anon 
    html = session.get(url).text
    if args.verbose:
        print(url)
    with open(FilePath, "a") as txt_file:
        for line in html.split('\n'):
            if len(line) > 0:
                txt_file.write(line)
                
# W men Hada Tahuwa sslproxies.org, free-proxy-list.net, us-proxy.org, socks-proxy.net
def makesoup(url):
    page=requests.get(url)
    if args.verbose:
        print(url + ' scraped successfully')
    return BeautifulSoup(page.text,"html.parser")

def proxyscrape(table):
    proxies = set()
    for row in table.findAll('tr'):
        fields = row.findAll('td')
        count = 0
        proxy = ""
        for cell in row.findAll('td'):
            if count == 1:
                proxy += ":" + cell.text.replace('&nbsp;', '')
                proxies.add(proxy)
                break
            proxy += cell.text.replace('&nbsp;', '')
            count += 1
    return proxies

def scrapeproxies(url):
    soup=makesoup(url)
    result = proxyscrape(table = soup.find('table', attrs={'id': 'proxylisttable'}))
    proxies = set()
    proxies.update(result)
    with open(FilePath, "a") as txt_file:
        for line in proxies:
	        txt_file.write("".join(line) + "\n")


# output watcher
def output():
    if os.path.exists(FilePath):
        os.remove(FilePath)
    elif not os.path.exists(FilePath):
        with open(FilePath, 'w'): pass

if __name__ == "__main__":

        global proxy

        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--proxy", help="Supported proxy type: http ,https, socks, socks4, socks5", required=True)
        parser.add_argument("-o", "--output", help="output file name to save .txt file", default='output.txt')
        parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
        args = parser.parse_args()

        proxy = args.proxy
        FilePath = args.output

        if proxy == 'https':
            threading.Thread(target=scrapeproxies, args=('http://sslproxies.org',)).start()
            threading.Thread(target=proxyListDownloadScraper, args=('https://www.proxy-list.download/api/v1/get', 'https', 'elite',)).start()            
            output()

        if proxy == 'http':
            threading.Thread(target=scrapeproxies, args=('http://free-proxy-list.net',)).start()
            threading.Thread(target=scrapeproxies, args=('http://us-proxy.org',)).start()
            threading.Thread(target=proxyScraper, args=('http','1000','All',)).start()
            threading.Thread(target=proxyListDownloadScraper, args=('https://www.proxy-list.download/api/v1/get', 'http', 'elite',)).start()
            threading.Thread(target=proxyListDownloadScraper, args=('https://www.proxy-list.download/api/v1/get', 'http', 'transparent',)).start()
            threading.Thread(target=proxyListDownloadScraper, args=('https://www.proxy-list.download/api/v1/get', 'http', 'anonymous',)).start()
            output()

        if proxy == 'socks':
            threading.Thread(target=scrapeproxies, args=('http://socks-proxy.net',)).start()
            threading.Thread(target=proxyScraper, args=('socks4','1000','All',)).start()
            threading.Thread(target=proxyScraper, args=('socks5','1000','All',)).start()
            threading.Thread(target=proxyListDownloadScraper, args=('https://www.proxy-list.download/api/v1/get', 'socks5', 'elite',)).start()
            threading.Thread(target=proxyListDownloadScraper, args=('https://www.proxy-list.download/api/v1/get', 'socks4', 'elite',)).start()
            output()

        if proxy == 'socks4':
            threading.Thread(target=proxyScraper, args=('socks4','1000','All',)).start()
            threading.Thread(target=proxyListDownloadScraper, args=('https://www.proxy-list.download/api/v1/get', 'socks4', 'elite',)).start()
            output()

        if proxy == 'socks5':
            threading.Thread(target=proxyScraper, args=('socks5','1000','All',)).start()
            threading.Thread(target=proxyListDownloadScraper, args=('https://www.proxy-list.download/api/v1/get', 'socks5', 'elite',)).start()
            output()
