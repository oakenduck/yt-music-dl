from cmd import Cmd
from shlex import split

import yt_dlp as ydl


class DownloaderShell(Cmd):
    intro = "Welcome to the YT Downloader shell.    Type help or ? to list commands.\n"
    prompt = "(ytdls) "
    file = None

    def do_audio(self, args):
        """extract audio from video or playlist."""\
        """\n\nusage:\n\taudio url\t// download single video or playlist without index in filename"""\
        """\n\taudio album url\t// downloads playlist as an album with index in filename. alias 'audio al url'"""
        args = split(args)

        if len(args) == 2:
            if args[0] in ["al", "album"]:
                url = args[1]
                title = "./downloads/%(playlist_title)s/%(playlist_index)d - %(title)s.%(ext)s"
            else:
                # error out
                print(f"[ERROR]: unknown argument '{args[0]}'. Run 'help audio' to see proper usage.")
                return
        else:
            url = args[0]
            title = "./downloads/%(title)s.%(ext)s"

        with ydl.YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': title, 'no_warnings': True}) as video:
            info_dict = video.extract_info(url, download=True)
            video_title = info_dict['title']
            print(f"Downloaded {video_title}")


    def do_exit(self, args):
        """exit shell."""
        print("Exiting ytdls.")
        return True


if __name__ == "__main__":
    DownloaderShell().cmdloop()
