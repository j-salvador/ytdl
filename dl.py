import sys
from multiprocessing import Process
from pytube import YouTube


def dl_vid(url):
    yt = YouTube(url)
    print('downloading: ' + yt.title)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download() 
    print('finishedL: ' + yt.title)

if __name__ == '__main__':
    ps = []
    for url in sys.argv[1:]:
        p = Process(target=dl_vid, args=(url,))
        ps.append(p)
        p.start()
   
    for p in ps:
        p.join()
print('done!')
