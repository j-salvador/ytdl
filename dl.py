import sys
from multiprocessing import Process
from pytube import YouTube
import ffmpeg


def dl_vid(url):
    yt = YouTube(url)
    title = yt.title

    # Check if text contains # symbol, if so replace as ffmpeg doesn't like #
    if "#" in title:
        title = title.replace("#", "")

    # trim to replace whitespace with underscore
    title_trim = "_".join(title.split())

    print('Downloading ' + yt.title + ' to ' + title_trim + '.mp4')

    (yt.streams.filter(progressive=True, file_extension='mp4')
        .order_by('resolution')
        .desc()
        .first()
        .download(filename=title_trim))

    convert(title_trim+".mp4", title_trim+".mp3")
    print('Finished downloading: ' + title)


def convert(name_vid, name_sound):
    print("name_vid:" + name_vid + "\n")
    audio = ffmpeg.input(name_vid).audio
    ffmpeg.output(audio, name_sound).run()


if __name__ == '__main__':
    ps = []
    for url in sys.argv[1:]:
        p = Process(target=dl_vid, args=(url,))
        ps.append(p)
        p.start()
   
    for p in ps:
        p.join()

    print('done!')
