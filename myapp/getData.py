from BeautifulSoup import BeautifulSoup
import urllib2


def getMoreInfo(url):
    finit = urllib2.urlopen(url)
    soupInit = BeautifulSoup(finit.read().decode('utf-8', 'ignore'))
    elemEnlacea = soupInit.findAll(
        'a', attrs={"class": "punteado"})
    if len(elemEnlacea) > 0:
        enlace = elemEnlacea[0]['href']
        urlContent = "http://www.madrid.es" + enlace
        finfo = urllib2.urlopen(urlContent)
        soupInfo = BeautifulSoup(finfo.read())
        moreInfo = soupInfo.findAll('p')[2].text
    else:
        moreInfo = "No hay informacion"
    return moreInfo
