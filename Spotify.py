# -*- coding: utf-8 -*-
import spotipy
import spotipy.oauth2 as oauth2

import API_KEYS
from DownloadYoutubeLink import downloadLink
from LinkProvider import choseBestLink
from LinkProvider import displayLocalPlaylist
from LinkProvider import slugify
from color import printWithCol


def generate_token():
    credentials = oauth2.SpotifyClientCredentials(
        client_id=API_KEYS.client_id,
        client_secret=API_KEYS.client_secret)
    token = credentials.get_access_token()
    return token


def write_tracks(text_file, tracks, sort):
    playlist = []
    number = 0
    while True:
        for item in tracks['items']:
            if 'track' in item:
                track = item['track']
            else:
                track = item
            try:
                output = item['track']['name']
                artistNum = 0
                for artist in item['track']['artists']:
                    if artistNum < 2:
                        output += ", " + artist['name']
                    else:
                        break
                    artistNum = artistNum + 1
                number = number + 1
                print(str(number) + "/" + str(tracks['total']) + " tracks done")
                if not sort:
                    playlist.insert(0, output)
                else:
                    playlist.append(output)
            except KeyError:
                print(u'Skipping track {0} by {1} (local only?)'.format(
                    track['name'], track['artists'][0]['name']))
        if tracks['next']:
            tracks = spotify.next(tracks)
        else:
            break

    with open(text_file, 'w', encoding='utf-8') as file_out:
        for line in playlist:
            file_out.write(slugify(line) + '\n')

    return playlist


def write_playlist(username, playlist_id, sort):
    results = spotify.user_playlist(username, playlist_id,
                                    fields='tracks,next,name')
    text_file = u'.\\Playlist data\\{0}.anc'.format(results['name'], ok='-_()[]{}')
    print(u'Writing {0} tracks to {1}'.format(
        results['tracks']['total'], text_file))
    tracks = results['tracks']
    return results['name'], write_tracks(text_file, tracks, sort)


def getTracksFromFile(filename):
    playlist = []
    lines = open(filename, 'r').read().split('\n')
    for line in lines:
        if line == "\n":
            continue
        else:
            playlist.append(slugify(line))
    return playlist


# main
localplaylist = 1
while True:
    while True:
        if localplaylist == 0:
            choice = 'o'
        else:
            print("")
            printWithCol("Do you want to use online Spotify PlayList or Local file (o/Enter)", color='blue',
                         nonline=True)
            choice = input()
            # choice = "o"

        playlist_name = ''
        if choice == 'o':
            token = generate_token()
            spotify = spotipy.Spotify(auth=token)
            playlistid = ['1BqOk5pxOvjuyElnzMtJGG', '37i9dQZEVXbLRQDuF5jeBp', '37i9dQZF1DX4JAvHpjipBk']
            print("")
            id = int(input(" Enter playlist ID : ['Sad reacts only','United States TOP 50','New Music Friday']"))
            id = playlistid[id - 1]
            # id='1BqOk5pxOvjuyElnzMtJGG'
            while True:
                try:
                    plType = int(input("sort by OldToNew or NewToOld (1/0): "))
                except:
                    printWithCol("Non valid input ! ", "red")
                    continue
                if plType == 1 or plType == 0:
                    break
            username = 'ayman.nait21'
            while True:
                try:
                    playlist_name, playlist = write_playlist(username, id, plType)
                    if playlist_name or playlist:
                        break
                except:
                    printWithCol("Non valid playlist ID ! ", "red")
                    id = input("Enter playlist ID : ")
                    continue
            break
        else:
            print("")
            final_res, number = displayLocalPlaylist()
            if number > 0:
                printWithCol("Choose which file to use  : ", color='green')
                for x, y in final_res:
                    print(str(x) + " - " + y)
                # inp = int(input("choose a playlist : "))
                # inp =3
                # playlist_name = final_res[inp - 1][1]
                playlist_name = final_res[0][1]
                playlist = getTracksFromFile(".\\Playlist data\\" + playlist_name + ".anc")
                break
            else:
                printWithCol("There is no Playlist saved  !! ", color='red')
                printWithCol("Starting online download  !! ", color='green')
                print()
                localplaylist = 0
                continue

    """  
	print("")
	printWithCol("Want to Display the play list ? (y/Enter)", color='blue', nonline=True)
	choice = input()
	"""
    choice = 'n'
    if choice == "y":
        for song in playlist:
            try:
                print(slugify(song))
            except:
                continue

    # downloading time
    filenumber = 0

    print("")
    printWithCol("Start Downloading " + playlist_name + " ? (y/Enter)", color='blue', nonline=True)
    # choice = input()
    choice = "y"
    if choice == "y":
        for songName in playlist:
            print("")
            link = choseBestLink(songName, playlist_name)
            if link != None:
                filenumber = downloadLink(link, filenumber, playlist_name, songName)
    else:
        print("You're UpToDate next time use Local File to download Tracks !")
