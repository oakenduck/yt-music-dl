from cmd import Cmd
from shlex import split

import yt_dlp as ydl


class DownloaderShell(Cmd):
    intro = "Welcome to the YT Downloader shell.    Type help or ? to list commands.\n"
    prompt = "(ytdls) "
    file = None
    history = {
        'audio': [],
        'video': []
    }

    def do_history(self, args):
        """list video and audio downloaded."""\
        """\n\nusage:\n\thistory"""
        print("AUDIO:")
        for idx, a in enumerate(self.history['audio']):
            print(f"\t{idx+1}: {a}")

        print("VIDEO:")
        for idx, v in enumerate(self.history['video']):
            print(f"\t{idx+1}: {v}")

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

            if 'entries' in info_dict:
                titles = [entry.get('title') for entry in info_dict['entries'] if entry]
                for t in titles:
                    self.history['audio'].append(t)

            else:
                self.history['audio'].append(info_dict['title'])

            video_title = info_dict['title']
            print(f"Downloaded {video_title}")

    def do_video(self, args):
        """download video or playlist."""\
        """\n\nusage:\n\tvideo url\t// download single video or playlist without index in filename"""\
        """\n\tvideo album url\t// download playlist as an album with index in filename. alias 'video al url'"""
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

        with ydl.YoutubeDL({
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mkv',
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'subtitlesformat': 'srt',
            'outtmpl': title,
            'no_warnings': True
        }) as video:
            info_dict = video.extract_info(url, download=True)
            video_title = info_dict['title']
            print(f"Downloaded {video_title}")


    def do_exit(self, args):
        """exit shell."""
        print(f"Exiting ytdls after downloading {len(self.history['video'])} videos and {len(self.history['audio'])} audio only.")
        return True


if __name__ == "__main__":
    DownloaderShell().cmdloop()
