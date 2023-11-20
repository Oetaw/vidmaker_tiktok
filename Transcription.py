import os
from utils import filename
os.environ["REPLICATE_API_TOKEN"] = "r8_TvUKZKsjvCyuM0DzAho7i6j7NX7wX9y1NCRIA"
from utils import format_timestamp
import replicate
import subprocess

VideoTypes = ["Reddit_stories", "TTGmplay", "Movies", ]
def fastVideo(video):
    srt = ""
    output = replicate.run(
        "daanelson/whisperx:9aa6ecadd30610b81119fc1b6807302fd18ca6cbb39b3216f430dcf23618cedd",
        input={"audio": open(f"{video}", "rb"),
               "batch_size": 32,
               "align_output": True}
    )
    bb = []
    for i in range(len(output)):
        for word in range(len(output[i]["words"])):
            bb.append(output[i]["words"][word])
    List = []
    for i in range(len(bb)):
        bb[i]["word"] = bb[i]["word"].replace(",", "")
        bb[i]["word"] =bb[i]["word"].replace(".", "")
        if len(bb[i]["word"]) <= 2 or bb[i]["word"] == "The":
            gtu = [bb[i]["word"], bb[i]["start"]]
            for i in range(len(gtu)):
                List.append(gtu[i])
        else:
            print(len(List))
            print(List)
            if len(List) == 0:
                srt += f"{i + 1}\n"
                srt += f"{format_timestamp(bb[i]['start'], always_include_hours=True)} --> {format_timestamp(bb[i]['end'], always_include_hours=True)}\n"
                srt += bb[i]["word"] + "\n\n"
            else:
                srt += f"{i + 1}\n"
                srt += f"{format_timestamp(List[1], always_include_hours=True)} --> {format_timestamp(bb[i]['end'], always_include_hours=True)}\n"
                srt += f"{List[0]} {bb[i]['word']}\n\n"
                for b in range(len(List)):
                    List.pop(0)
    return srt
def SRT(OutputDir, video, text):
    srt_path = os.path.join(OutputDir, f"{filename(video)}.srt")
    with open(srt_path, "w", encoding="utf-8") as srt1:
        srt1.write(text)
def PutSubs(video, OutputDir):
    outdir = os.path.abspath(OutputDir) + f"{os.path.sep}{filename(video)}_subed.mp4"
    srt_path = os.path.join(OutputDir, f"{filename(video)}.srt")
    srt_path = srt_path.replace(f":{os.path.sep}", "\:/")
    vid = os.path.abspath(video)
    ffmpeg_command = [
        "ffmpeg",
        "-i", vid,
        "-filter_complex",
        f"subtitles='{srt_path}':force_style='Alignment=10,Fontsize=11,Fontname=Komika Axis,BackColour=&H80000000,Spacing=0.2,Shadow=0.75,OutlineColour=&H40000000'",
        outdir
    ]
    try:
        subprocess.run(ffmpeg_command, check=True)
        print("FFmpeg command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running FFmpeg command: {e}")
def trascription(video, VideoType, OutputDir = "./done_files/subtitled/"):
        if VideoType in VideoTypes and VideoType == "Reddit_stories":
            txt = fastVideo(video)
            SRT(OutputDir, video, txt)
            PutSubs(video, OutputDir)
        if VideoType in VideoTypes and VideoType == "TTGmplay":
            print("DD")


trascription(video = "./assets/downloaded_videos/y2mate.com - This Video Is 3 Seconds_720p.mp4", VideoType="Reddit_stories")





