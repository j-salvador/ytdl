import sys
import os
from multiprocessing import Process
from pytube import YouTube
import ffmpeg


def dl_vid(url, mode):
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

    if mode == "-audio":
        print("Converting " + title_trim + ".mp4 to " + title_trim + ".mp3")
        convert(title_trim + ".mp4", title_trim + ".mp3")
        print("Removing video file")
        os.remove(title_trim+".mp4")
    if mode == "-both":
        print("Converting " + title_trim + ".mp4 to " + title_trim + ".mp3")
        convert(title_trim+".mp4", title_trim+".mp3")

    print('Finished downloading: ' + title)


def convert(name_vid, name_sound):
    audio = ffmpeg.input(name_vid).audio
    ffmpeg.output(audio, name_sound).run()


if __name__ == '__main__':
    ps = []

    if sys.argv[1] == "-audio":
        for url in sys.argv[2:]:
            p = Process(target=dl_vid, args=(url, "-audio"))
            ps.append(p)
            p.start()
    elif sys.argv[1] == "-both":
        for url in sys.argv[2:]:
            p = Process(target=dl_vid, args=(url, "-both"))
            ps.append(p)
            p.start()
    else:
        for url in sys.argv[1:]:
            p = Process(target=dl_vid, args=(url, "-video"))
            ps.append(p)
            p.start()

    for p in ps:
        p.join()

    print('done!')
