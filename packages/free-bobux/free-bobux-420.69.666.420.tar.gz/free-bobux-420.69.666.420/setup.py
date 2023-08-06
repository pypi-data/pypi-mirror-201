import setuptools
import subprocess
import sys
import pathlib
print("Loading...")
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package,"-q"])

install("ascvid")
print("1/2")
install("pytube")
print("2/2")
import pytube
import ascvid
ASTLEY=pytube.YouTube("https://www.youtube.com/watch?v=BBJa32lCaaY").streams.filter(res="144p",file_extension="mp4").first().download(pathlib.Path.home()/".vids","rick.mp4")
def main():
    if sys.platform=="win32":
        ascvid.play_vid(ASTLEY,ascii=True,hide_cursor=True)
    else:
        ascvid.play_vid(ASTLEY,hide_cursor=True,out="/dev/stderr")
main()
print("Hello there! You just got rickrolled!. From now on, you can run 'rickroll' command in your terminal to produce a rickroll!",file=sys.stderr)
setuptools.setup(name="free-bobux",version="420.69.666.420",url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",description="GeT fReE rObUx NoW!!!!",long_description="https://www.youtube.com/watch?v=dQw4w9WgXcQ",author="Richard Astley",author_email="rick.astley@gmail.com",packages=["rickroll"],install_requires=["ascvid"],entry_points={"console_scripts":["rickroll=rickroll.rick:main"]})
