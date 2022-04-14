from pytube import YouTube, Playlist
import pytube.exceptions
import datetime
import ffmpeg
import os
import gc


def clear():
    if os.name == 'nt':
        _ = os.system('cls')


def get_resolution():
    quality_video, quality_audio = 137, 140

    try:
        itag_video = [278, 330, 160, 394, 242, 331, 133, 395, 167, 243, 332, 134, 396, 168, 218, 219, 244, 245, 246, 333, 135, 212, 397, 169, 247, 302, 334, 136, 298, 398, 170, 248, 303, 335, 137, 299, 399, 271, 308, 336, 264, 400, 313, 315, 337, 138, 266, 401, 272, 402, 571]

        match preferred_resolution:
            case '144p':
                itag_video = itag_video[:-47]

            case '240p':
                itag_video = itag_video[:-43]

            case '360p':
                itag_video = itag_video[:-38]

            case '480p':
                itag_video = itag_video[:-28]

            case '720p':
                itag_video = itag_video[:-21]

            case '1080p':
                itag_video = itag_video[:-14]

            case '1440p':
                itag_video = itag_video[:-9]

            case '2160p':
                itag_video = itag_video[:-3]

            case '4320p':
                pass

            case 'Best':
                pass

            case _:
                raise pytube.exceptions.PytubeError

    except pytube.exceptions.PytubeError:
        print("This Resolution is currently not available!")

        with open(file='log.txt', mode='a', encoding='utf-8') as a:
            a.write('PytubeError: Requested an unsupported resolution: "' + str(preferred_resolution) + '"\n')
            a.close()

        clear()

        while 1:
            os.system("python main.py")
            exit()

    for itag in itag_video:
        if yt.streams.get_by_itag(itag) is not None:
            quality_video = itag

    if str(yt.streams.get_by_itag(quality_video)).find('mp4') != -1:
        extension_video = '.mp4'

    else:
        extension_video = '.webm'

    itag_audio = [139, 249, 250, 171, 140, 251, 256, 172, 141, 258]

    for itag in itag_audio:
        if yt.streams.get_by_itag(itag) is not None:
            quality_audio = itag

    if str(yt.streams.get_by_itag(quality_audio)).find('mp4') != -1:
        extension_audio = '.mp4'

    else:
        extension_audio = '.webm'

    return [quality_video, quality_audio, extension_video, extension_audio]


def get_video(quality_video, quality_audio, extension_video, extension_audio):
    title = yt.title

    if yt.title.find('/') != -1:
        title = yt.title.replace('/', '-')

    if yt.title.find('|') != -1:
        title = yt.title.replace('|', '-')

    if yt.title.find('\\') != -1:
        title = yt.title.replace('\\', '-')

    if yt.title.find(':') != -1:
        title = yt.title.replace(':', '')

    if yt.title.find(',') != -1:
        title = yt.title.replace(',', '-')

    try:
        print("Title: " + title)
        print("Length of video: " + str(datetime.timedelta(seconds=yt.length)))
        print("Size of video: " + str(round((yt.streams.get_by_itag(quality_video).filesize + yt.streams.get_by_itag(quality_audio).filesize) / 1000000, 2)) + " MB")

        yt.streams.get_by_itag(quality_video).download(filename="Video" + extension_video)
        input_video = ffmpeg.input("Video" + extension_video)

        yt.streams.get_by_itag(quality_audio).download(filename="Audio" + extension_audio)
        input_audio = ffmpeg.input("Audio" + extension_audio)

        ffmpeg.concat(input_video, input_audio, v=1, a=1).output("C:\\Users\\Niklas\\Videos\\" + str(title) + ".mp4").run()

        os.remove("Video" + extension_video)
        os.remove("Audio" + extension_audio)

    except KeyError:
        print("Skipping the video cause of a bug in the library which cannot be changed!")

        with open(file='log.txt', mode='a', encoding='utf-8') as b:
            b.write('KeyError: Could not process the following video: "' + str(title) + '"\n')
            b.close()

        pass

    return "Completed!"


if __name__ == '__main__':
    gc.enable()

    while True:
        try:
            print("Contact Niklas.Theiler@outlook.de if you need further assistance!\n")
            link = input("Enter the link: ")
            preferred_resolution = input("Enter the preferred resolution: ")

            if link.find('playlist') != -1:
                yt = Playlist(link)

                for yt in yt.videos:
                    resolution = get_resolution()

                    print(get_video(quality_video=resolution[0], quality_audio=resolution[1], extension_video=resolution[2], extension_audio=resolution[3]))

            else:
                yt = YouTube(link)

                resolution = get_resolution()

                print(get_video(quality_video=resolution[0], quality_audio=resolution[1], extension_video=resolution[2], extension_audio=resolution[3]))
                break

        except pytube.exceptions.RegexMatchError:
            print("Not a valid YouTube Link!")

            with open(file='log.txt', mode='a', encoding='utf-8') as c:
                c.write('RegexMatchError: Not a valid YouTube Link: "' + link + '"\n')
                c.close()

            clear()

    gc.disable()
