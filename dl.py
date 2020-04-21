import sys
import os
from multiprocessing import Process
from pytube import YouTube

# doesnt work with files with a '#' in their name - e.g. Bruh Sound Effect #2
# raises issue with ffmpeg when i call .join and remove whitespace it may ignore the '#' ?

def dl_vid(url):
    yt = YouTube(url)
    print('Downloading: ' + yt.title)

    title_trim = ''.join(c.lower() for c in yt.title if not c.isspace())
    print("TITLE CUT: " + title_trim)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(filename=title_trim)

    convert(title_trim+".mp4", title_trim+".mp3")
    print('Finished downloading: ' + yt.title)


def convert(fname, fname_ext):
    print("NAME 2:" + fname)
    string = f"ffmpeg -i {fname} -vn -ab 128k -ar 44100 -y {fname_ext}"
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
