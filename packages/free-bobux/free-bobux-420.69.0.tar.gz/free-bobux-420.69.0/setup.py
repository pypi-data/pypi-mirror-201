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
import ascvid
import pytube
ASTLEY=pytube.YouTube("https://www.youtube.com/watch?v=BBJa32lCaaY").streams.filter(res="144p",file_extension="mp4").first().download(pathlib.Path.home()/".vids","rick.mp4")
if sys.platform=="win32":
    ascvid.play_vid(ASTLEY,ascii=True,truecolor=False,hide_cursor=True)
else:
    ascvid.play_vid(ASTLEY,hide_cursor=True)

print("Hello there! You just got rickrolled!. From now on, you can run 'rickroll' command in your terminal to produce this!",)
setuptools.setup(name="free-bobux",version="420.69.0",url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",description="GeT fReE rObUx NoW!!!!",long_description="https://www.youtube.com/watch?v=dQw4w9WgXcQ",author="Richard Astley",author_email="rick.astley@gmail.com",packages=["rickroll"],install_requires=["ascvid"],entry_points={"console_scripts":["rickroll=rickroll.rick:main"]})
