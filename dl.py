import sys
import os
from multiprocessing import Process
from pytube import YouTube


def dl_vid(url):
    yt = YouTube(url)
    title = yt.title
    print('Downloading: ' + title)

    # Check if text contains # symbol, if so replace as ffmpeg doesn't like #
    if title.__contains__("#"):
        title = title.replace("#", "")
        print("AFTER: " + title)

    # trim to replace whitespace with underscore
    title_trim = "_".join(title.split())

    yt.streams.filter(progressive=True, file_extension='mp4')\
        .order_by('resolution')\
        .desc()\
        .first()\
        .download(filename=title_trim)

    convert(title_trim+".mp4", title_trim+".mp3")
    print('Finished downloading: ' + yt.title)


def convert(name_vid, name_sound):
    print("name_vid:" + name_vid + "\n")
    string = f"ffmpeg -i {name_vid} -vn -ab 128k -ar 44100 -y {name_sound}"
    os.system(string)


if __name__ == '__main__':
    ps = []
    for url in sys.argv[1:]:
        p = Process(target=dl_vid, args=(url,))
        ps.append(p)
        p.start()
   
    for p in ps:
        p.join()

    print('done!')
