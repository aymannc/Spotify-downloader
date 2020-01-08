# -*- coding: utf-8 -*-
import fnmatch
import math
import os
import urllib.request
from functools import reduce

from bs4 import BeautifulSoup
from slugify import slugify as slugifylib

from color import printWithCol


def slugify(str):
    forbiden = "/<>:\"/\\|?*%%"
    return reduce(lambda a, b: a.replace(b, ' '), forbiden, str)


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def findFilles(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def getQueryInfo(songName):
    ListToSearch = [songName, songName + " audio"]
    results = []
    for texttosearch in ListToSearch:
        # if not texttosearch.endswith("audio") :
        printWithCol("Searching for : ", "magenta", nonline=True)
        printWithCol(texttosearch)
        print("")

        text = slugifylib(texttosearch)
        query = urllib.parse.quote(text)
        url = "https://www.youtube.com/results?search_query=" + query
        # print("url {}".format(url))
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        v = soup.findAll(attrs={'class': 'yt-uix-tile-link'})[0]

        """
        print("top 5 results ")
        for inc in range(0,4):
                print(str(soup.findAll(attrs={'class': 'yt-uix-tile-link'})[inc]['href']))
        """
        if results != []:
            link2 = ("https://www.youtube.com" + str(soup.findAll(attrs={'class': 'yt-uix-tile-link'})[0]['href']))
            if results[0] != None:
                if results[0]['link'] == link2:
                    v = soup.findAll(attrs={'class': 'yt-uix-tile-link'})[1]
        txt = str(v['href'])
        v = str(v)
        """
        try:
            print("href: https://www.youtube.com"+txt)
        except:
            print("except : "+text)
        """
        views = ''
        mins = ''
        secs = ''
        try:
            v.index('hour')
            results.append(None)
            continue
        except:
            try:
                v.index('hours')
                results.append(None)
                continue
            except:
                pass
        try:
            indx = v.index('views')
        except:
            results.append(None)
            continue
        indx = v.index('views')
        indx = indx - 2
        while v[indx] is not ' ':
            views = v[indx] + views
            indx = indx - 1
        secOnly = 0
        try:
            indx = v.index('minutes')
        except:
            try:
                indx = v.index('minute')
            except:
                secOnly = 1
        if not secOnly:
            indx = indx - 2
            while v[indx] is not ' ':
                mins = v[indx] + mins
                indx = indx - 1
        try:
            indx = v.index('second')
        except:
            try:
                indx = v.index('seconds')
            except:
                secs = "0"
                results.append({"link": "https://www.youtube.com" + txt, "view": views, "min": mins, "sec": secs})
                continue

        indx = indx - 2
        while v[indx] is not ' ':
            secs = v[indx] + secs
            indx = indx - 1
        if secOnly:
            mins = math.floor(int(secs) / 60)
            secs = int(secs) % 60
        results.append({"link": "https://www.youtube.com" + txt, "view": views, "min": mins, "sec": secs})

    return results


def choseBestLink(textToSearch, playlist_name):
    path = ".\\All playlists\\" + playlist_name + "\\"
    res = find(textToSearch + ".mp3", path)
    if res != None:
        printWithCol("Allready exist : ", "green", nonline=True)
        printWithCol(textToSearch + ".mp3  !", "blue")
        return None

    link1score = link2score = 0
    link1, link2 = getQueryInfo(textToSearch)

    if link1 != None:
        print("link1 : %s | view : %s | duration : %s:%s" % (link1["link"], link1["view"], link1["min"], link1["sec"]))
    else:
        print("link1 is Invalide")
    if link2 != None:
        print("link2 : %s | view : %s | duration : %s:%s" % (link2["link"], link2["view"], link2["min"], link2["sec"]))
    else:
        print("link2 is Invalide")

    # TODO: make the printing ui more cleaner use :\n
    print("")
    printWithCol("Comparing links ! ", "yellow")
    if link1 == None and link2 == None:
        return link1
    elif link1 == None and link2 != None:
        return link2['link']
    elif link2 == None and link1 != None:
        return link1['link']
    else:
        views1 = int(link1['view'].replace(',', ''))
        views2 = int(link2['view'].replace(',', ''))
        mins1 = int(link1['min'])
        mins2 = int(link2['min'])
        if (views1 > views2):
            link1score = link1score + 1.5
            # print("link 1 has more views | score : " + str(link1score))
        elif (views1 < views2):
            link2score = link2score + 1.5
            # print("link 2 has more views | score : " + str(link2score))

        if (mins1 < mins2):
            link1score = link1score + abs(mins1 - mins2) * 3
            # print("link 1 has less mins | score : " + str(link1score))

        elif (mins2 < mins1):
            link2score = link2score + abs(mins1 - mins2) * 3
            # print("link 2 has less mins | score :" + str(link2score))

        elif (link1['sec'] < link2['sec']):
            add = (abs(int(link1['sec']) - int(link2['sec'])) % 3)
            link1score = link1score + add
            # print("link 1 has less sec +%.2f | score %d : " %(add,link1score))

        elif (link2['sec'] < link1['sec']):
            add = (abs(int(link1['sec']) - int(link2['sec'])) % 3)
            link2score = link2score + add
            # print("link 2 has less sec +%.2f | score : %d  "%(add, link2score))

        # print("final scores : ",link1score,link2score)
        link = link1['link'] if link1score >= link2score else link2['link']
    return link


def displayLocalPlaylist():
    result = findFilles("*.anc", ".\\Playlist data\\")
    result = list(map(lambda x: x.replace('.anc', '').replace('.\\Playlist data\\', ''), result))
    final_res = list(zip({i + 1 for i in range(0, len(result))}, result))

    return final_res, len(result)
