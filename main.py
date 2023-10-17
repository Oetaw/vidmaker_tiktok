from moviepy.editor import clips_array, VideoFileClip
from icecream import ic
import os
from utils import filename
from cli import mn
import customtkinter
outdir = "F:/projeect/done_files/subtitled/"
videos = []
global b
b = ["", 0, []]
def transcribe_and_add_captions(video):
    mn(output_dir=outdir, pathse=[f"F:/projeect/done_files/made_vids/{video}"], output_srt=True)

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
def creation(files):
    for i in range (len(files)):
        cb = VideoFileClip(files[i])
        video_name = filename(files[i])
        #cb = cb.subclip(90, cb.duration - 105)
        entertainment_video = find_entertainmentvid(cb.duration)  # Duration is set to 2 minutes
        crop = mains(cb, entertainment_video)
        cc = clips_array([[crop[0]], [crop[1]]])
        clipname = f"{video_name}_subed"
        cc.write_videofile(f"./done_files/made_vids/{video_name}.mp4", codec='libx264', audio_codec='aac', bitrate="5000k")
        transcribe_and_add_captions(f"{video_name}.mp4")
        os.remove(f"./done_files/made_vids/{video_name}.mp4")
        cg = VideoFileClip(f"./done_files/subtitled/{clipname}.mp4")
        split_clips = split_video(cg, 2 * 60)  # Split the video into 2-minute parts
        for i, subclip in enumerate(split_clips):
            subclip_name = f"{video_name}_part_{i + 1}"
            subclip.write_videofile(f"./done_files/made_vids/{subclip_name}.mp4", codec='libx264', audio_codec='aac', bitrate="5000k")



def create_gui():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()

    root.geometry("500x350")
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=10, padx=60, fill="both", expand=True)
    def login():
        print("Test")
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
    def genopen():
        creation(b[2])
    def names_changer():
        for i in range(len(b[2])):
            old_name = filename(b[2][i])
            new_name = old_name[:6]
            os.rename(b[2][i], f"./assets/downloaded_videos/{new_name}.mp4")
    button_selectFiles = customtkinter.CTkButton(master=frame, text="Select Files", command=filesopen, corner_radius=40)
    button_selectFiles.pack(pady=20, padx=20)

    gen_button = customtkinter.CTkButton(master=frame, text="Generate", command=genopen, corner_radius=40)
    gen_button.pack(pady=20, padx=20)
    change_names = customtkinter.CTkButton(master=frame, text="Change names", command=names_changer, corner_radius=40)
    change_names.pack(pady=20, padx=20)
    print(b[0])
    if not b[0]:
        gen_button["state"] = "disabled"
    root.mainloop()

if __name__ == "__main__":
    create_gui()

