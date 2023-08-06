import pathlib
import sys
import ascvid
ASTLEY=str(pathlib.Path.home()/".vids"/"rick.mp4")
def main():
    if sys.platform=="win32":
        ascvid.play_vid(ASTLEY,ascii=True,truecolor=False,hide_cursor=True)
    else:
        ascvid.play_vid(ASTLEY,hide_cursor=True)
