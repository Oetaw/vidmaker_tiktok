from moviepy.editor import clips_array, VideoFileClip, CompositeVideoClip, ColorClip
from icecream import ic
import os
from utils import filename
from cli import mn
import customtkinter
import tkinter
from skimage.filters import gaussian
outdir = "F:/projeect/done_files/subtitled/"
videos = []
global b
b = ["", 0, [], []]
paths = {
    "tiktoks": "/done_files/made_vids_shortTiktokGameplay",
    "movies": "/done_files/made_vids_movies",
    "wouldYR": "/done_files/made_vids_wouldYouRather",
    "subtitled": "/done_files/subtitled",
    "outdir": "F:/projeect/done_files/subtitled/"

}
choices = ["TTGmplay", "Generate"]
def transcribe_and_add_captions(video):
    if choices[0] == "TTGmplay":
        mn(output_dir=paths["outdir"], pathse=[f"F:/projeect/{paths['tiktoks']}/{video}"], output_srt=True, videoType=choices[0])
    elif choices[0] == "Movies":
        mn(output_dir=paths["outdir"], pathse=[f"F:/projeect/{paths['movies']}/{video}"], output_srt=True, videoType=choices[0])
    elif choices[0] == "Would You Rather":
        mn(output_dir=paths["outdir"], pathse=[f"F:/projeect/{paths['wouldYR']}/{video}"], output_srt=True, videoType=choices[0])


def find_entertainmentvid(duration):
    _, _, files = next(os.walk("./assets/entertainment_videos"))
    for i in range(len(files)):
        entertainment_video = VideoFileClip(
            f"./assets/entertainment_videos/gameplay_4.mp4", audio=False).subclip(0, duration)
        ic(entertainment_video)
    return entertainment_video

def mains(videoclip, entertainment_video):
    clips = [videoclip, entertainment_video]
    target_height = 1920
    target_width = 1080
    ic(clips[0].size[0], clips[0].size[1])

    clips[0] = clips[0].resize(width=target_width, height=target_height // 2)
    ic(clips[0].size[0], clips[0].size[1])
    crop = []
    for i in range(len(clips)):
        crop.append(clips[i].crop(x_center=clips[i].size[0] // 2, y_center=clips[i].size[1] // 2, width=target_width,
                                  height=target_height // 2))
    return crop
def split_video(video_clip, duration):
    video_duration = video_clip.duration
    split_clips = []
    start_time = 0
    while start_time < video_duration:
        end_time = min(start_time + duration, video_duration)
        subclip = video_clip.subclip(start_time, end_time)
        split_clips.append(subclip)
        start_time = end_time
    return split_clips
def creation_tiktok(files):
    for i in range (len(files)):
        cb = VideoFileClip(files[i])
        video_name = filename(files[i])
        #cb = cb.subclip(90, cb.duration - 105)
        entertainment_video = find_entertainmentvid(cb.duration)  # Duration is set to 2 minutes
        crop = mains(cb, entertainment_video)
        cc = clips_array([[crop[0]], [crop[1]]])
        clipname = f"{video_name}_subed"
        cc.write_videofile(f".{paths['tiktoks']}/{video_name}.mp4", codec='libx264', audio_codec='aac', bitrate="5000k")
        transcribe_and_add_captions(f"{video_name}.mp4")
        os.remove(f".{paths['tiktoks']}/{video_name}.mp4")
        cg = VideoFileClip(f".{paths['subtitled']}/{clipname}.mp4")
        split_clips = split_video(cg, int(gg.get()) * 60)  # Split the video into 2-minute parts
        for i, subclip in enumerate(split_clips):
            subclip_name = f"{video_name}_part_{i + 1}"
            subclip.write_videofile(f".{paths['tiktoks']}/{subclip_name}.mp4", codec='libx264', audio_codec='aac', bitrate="5000k")

def resize_video(video_path, output_path=f".{paths['movies']}/"):
    target_width = 1080
    target_height = 1920
    video_clip = video_path
    scaling_factor = min(target_width / video_clip.w, target_height / video_clip.h) * 1.4
    resized_clip = video_clip.resize(height=int(video_clip.h * scaling_factor))
    black_bars_width = (target_width - resized_clip.w) / 2
    final_clip = CompositeVideoClip([
        ColorClip(size=(target_width, target_height), color=(0, 0, 0)).set_duration(video_clip.duration),
        resized_clip.set_position(("center", "center")).set_duration(video_clip.duration)
    ])

    def blur(image):
        """ Returns a blurred (radius=2 pixels) version of the image """
        return gaussian_filter(image.astype(float), sigma=2)

    # Set audio to the original audio of the video
    final_clip = final_clip.set_audio(video_clip.audio)

    # Write the final video to a file
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

    # Clean up by closing clips
    video_clip.close()
    resized_clip.close()
    final_clip.close()

def create_movie(files):
    for i in range(len(files)):
        vd = VideoFileClip(files[i])
        video_name = filename(files[i])
        clipname = f"{video_name}_subed"
        resize_video(video_path=vd, output_path=f".{paths['movies']}/{video_name}.mp4")
        transcribe_and_add_captions(f"{video_name}.mp4")
        os.remove(f".{paths['movies']}/{video_name}.mp4")
        gb = VideoFileClip(f".{paths['subtitled']}/{clipname}.mp4")
        parts = split_video(gb, int(gg.get()) * 60)
        for d, subclip in enumerate(parts):
            subclip_name = f"{video_name}_part_{i + 1}"
            subclip.write_videofile(f".{paths['movies']}/{subclip_name}.mp4", codec='libx264', audio_codec='aac', bitrate="5000k")



def create_gui():
    options = ["TTGmplay", "Movies", "Would You Rather"]
    options1 = ["Generate", "setDirectory"]
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()

    root.geometry("500x350")
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=10, padx=60, fill="both", expand=True)
    def filesopen():
        if b[0] != "":
            b[0] = ""
        if b[2] != []:
            b[2] = []
        label1 = customtkinter.CTkLabel(frame, text=b[0], fg_color="transparent")
        files = customtkinter.filedialog.askopenfilenames(parent=root, title='Choose files')
        def bb():
            for i in range(len(files)):
                b[0] += f"{filename(list(files)[i])}.mp4,"
        bb()
        if b[1] != 1:
            label = customtkinter.CTkLabel(frame, text="is this what you want?", fg_color="transparent")
            label1.configure(text=b[0])
            print(b[0])
            label.pack();
            label1.pack()
        else:
            label1.configure(text=b[0])
        b[1] = 1
        b[2] = files

    ops = [options, options1]
    opsi = ["tik", "Drugie", "trzecie"]
    opsi1 = ["b", "u", "k"]
    op = ["", ""]
    jk = [0]
    def Start():
        if b[2]:
            if jk[0] == 1:
                errorLabel.pack_forget()
            for g in range(len(ops)):
                for i in range(len(ops[g])):
                    for d in range(len(choices)):
                        if choices[d] in ops[g]:
                            if choices[d] in options:
                                for f in range(len(options)):
                                    if choices[d] == options[f]:
                                        op[0] = opsi[f]
                            elif choices[d] in options1:
                                for f in range(len(options1)):
                                    if choices[d] == options1[f]:
                                        op[1] = opsi1[f]
            if op[0] == opsi[0]:
                creation_tiktok(b[2])
            elif op[0] == opsi[1]:
                create_movie(b[2])

        else:
            jk[0] = 1
            buttonStart.pack_forget()
            errorLabel.pack()
            buttonStart.pack(pady=10)

        print(op)

    button_selectFiles = customtkinter.CTkButton(master=frame, text="Select Files", command=filesopen, corner_radius=40)

    global optionLabel1
    global optionmenu
    global buttonStart
    global optionmenu2
    global errorLabel
    global entry
    global gg
    def optionmenu_callback(choice):
        if choice in options:
            choices[0] = choice
        elif choice in options1:
            choices[1] = choice
        if choices[1] != options1[0] and choice != options1[0]:
            choices[0] = ""
        if choice == "Generate" and choices[0] not in options:
            optionmenu.set(options[0])
            choices[0] = options[0]
        if choices[1] == "Generate":
            buttonStart.pack_forget()
            optionLabel1.pack(pady=5)
            optionmenu.pack()
            entry.pack(pady=10)
            buttonStart.pack(pady=10)
        else:
            optionmenu.pack_forget()
            entry.pack_forget()
            optionLabel1.pack_forget()
        print(gg.get())


    optionLabel = customtkinter.CTkLabel(frame, text="Choose from the below:")
    optionmenu = customtkinter.CTkOptionMenu(frame, values=options,
                                             command=optionmenu_callback, corner_radius=40)
    optionmenu.set(options[0])

    optionLabel1 = customtkinter.CTkLabel(frame, text="Choose action:")

    optionmenu2 = customtkinter.CTkOptionMenu(frame, values=options1,
                                             command=optionmenu_callback, corner_radius=40)
    optionmenu2.set(options1[0])
    gg = tkinter.StringVar()
    entry = customtkinter.CTkEntry(frame, textvariable=gg)
    errorLabel = customtkinter.CTkLabel(frame, text="there is no selected files!")
    buttonStart = customtkinter.CTkButton(frame, text="Start", command=Start, corner_radius=40)



    button_selectFiles.pack(pady=5, padx=20)
    optionLabel.pack(pady=5)
    optionmenu2.pack(pady=5)
    optionLabel1.pack(pady=5)
    optionmenu.pack()
    entry.pack(pady=10)
    buttonStart.pack(pady=10)
    root.mainloop()




if __name__ == "__main__":
    create_gui()

