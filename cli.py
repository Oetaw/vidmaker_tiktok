import os
import ffmpeg
import whisper
import argparse
import warnings
import tempfile
from utils import filename, str2bool, write_srt
from icecream import ic
import subprocess


def mn(output_dir, output_srt, pathse, model_name="small", srt_only = False, language ="auto"):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    os.makedirs(output_dir, exist_ok=True)
    args = parser.parse_args().__dict__

    if model_name.endswith(".en"):
        warnings.warn(
            f"{model_name} is an English-only model, forcing English detection.")
        args["language"] = "en"
    # if translate task used and language argument is set, then use it
    elif language != "auto":
        args["language"] = language

    model = whisper.load_model(model_name)
    ic(pathse)
    audios = get_audio(pathse)
    subtitles = get_subtitles(
        audios, output_srt or srt_only, output_dir, lambda audio_path: model.transcribe(audio_path, **args)
    )

    if srt_only:
        return

    for path, srt_path in subtitles.items():
        out_path = os.path.join(output_dir, f"{filename(path)}_subed.mp4")
        ic(srt_path, subtitles.items())
        print(f"Adding subtitles to {filename(path)}...")
        srt_path = srt_path.replace(":/", "\:/")
        video = ffmpeg.input(path)
        ic(out_path)
        audio = video.audio
        ffmpeg_command = [
            "ffmpeg",
            "-i", path,
            "-filter_complex",
            f"subtitles='{srt_path}':force_style='Alignment=10,Fontsize=11,Fontname=Komika Axis,BackColour=&H80000000,Spacing=0.2,Shadow=0.75,OutlineColour=&H40000000'",
            out_path
        ]
        try:
            subprocess.run(ffmpeg_command, check=True)
            print("FFmpeg command executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running FFmpeg command: {e}")

        print(f"Saved subtitled video to {os.path.abspath(out_path)}.")


def get_audio(paths):
    temp_dir = tempfile.gettempdir()

    audio_paths = {}
    ic(paths)
    for path in paths:
        ic(path)
        print(f"Extracting audio from {filename(path)}...")
        output_path = os.path.join(temp_dir, f"{filename(path)}.wav")

        ffmpeg.input(path).output(
            output_path,
            acodec="pcm_s16le", ac=1, ar="16k"
        ).run(quiet=True, overwrite_output=True)

        audio_paths[path] = output_path

    return audio_paths


def get_subtitles(audio_paths: list, output_srt: bool, output_dir: str, transcribe: callable):
    subtitles_path = {}

    for path, audio_path in audio_paths.items():
        srt_path = output_dir if output_srt else tempfile.gettempdir()
        srt_path = os.path.join(srt_path, f"{filename(path)}.srt")

        print(
            f"Generating subtitles for {filename(path)}... This might take a while."
        )

        warnings.filterwarnings("ignore")
        result = transcribe(audio_path)
        warnings.filterwarnings("default")

        with open(srt_path, "w", encoding="utf-8") as srt:
            write_srt(result["segments"], file=srt)

        subtitles_path[path] = srt_path

    return subtitles_path