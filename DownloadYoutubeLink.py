import youtube_dl

from color import printWithCol


def downloadLink(link, filenumber, playlistname, songname):
    print("")
    printWithCol("Downloading Begins : ", "red")
    print("")
    printWithCol("Youtube link : ", color='green', nonline=True)
    printWithCol(link, 'blue')
    download_options = {
        'format': 'bestaudio/best',
        'outtmpl': ".\\All playlists\\" + playlistname + "\\" + songname + '.%(ext)s',
        'nocheckcertificate': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(download_options) as ydl:
            ydl.download([link])
        filenumber = filenumber + 1
        print("")
        printWithCol("Files downloaded", color='white', back='on_grey', nonline=True)
        printWithCol(" " + str(filenumber) + " ", 'blue')
    except:
        # TODO : make a new file for all linkes that filed to download
        printWithCol("Failed to download", color='red', back='on_grey', nonline=True)
        printWithCol(" " + link + " ", 'blue')
    return filenumber
