import threading
import sys
import subprocess
import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring
from tkinter.simpledialog import askinteger
from tkinter.filedialog import askdirectory

def render(blender, ffmpeg, output_dir, blender_project, start, finish):
    subprocess.run(blender + " -b " + blender_project + " -E BLENDER_RENDER -s " + str(start) + " -e " + str(finish) + " -a")

root = Tk()
root.withdraw()
blender = os.path.normcase(askopenfilename(title="Where is blender.exe?", filetype=[("Executable", ".exe")]))
ffmpeg = os.path.normcase(askopenfilename(title="Where is FFmpeg?", filetype=[("Executable", ".exe")]))
blender_project = os.path.normcase(askopenfilename(title="Where is your blender project?", filetype=[("Blender Project", ".blend")]))
max_threads = askinteger("Threads", "Enter the number of threads")
max_frames = askinteger("Frames", "Enter the number of the end frame")
output_dir = os.path.normcase(askdirectory(title="Output dir from your project?"))
final_file_dir = os.path.normcase(askdirectory(title="Final file dir?"))
frames_per_thread =  int(int(max_frames) / int(max_threads))
last_frames = 0
frames = 0
threads = []

for i in range(max_threads):
    start = frames
    end = frames + frames_per_thread

    if i == max_threads - 1:
        end = max_frames

    frames = frames + frames_per_thread + 1
    threads.append(threading.Thread(target=render, args=(blender, ffmpeg, output_dir, blender_project, start, end)))

try:
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    file = open(os.path.normcase(os.path.join(output_dir, "render.txt")), "w")
    files = []
    for (dirpath, dirnames, filenames) in os.walk(output_dir):
        files.extend(filenames)
        break

    for f in files:
        if f != "render.txt":
            file.write("file '" + os.path.normcase(os.path.join(output_dir,f)) + "'\n")
    
    subprocess.run(ffmpeg + " -f concat -i " + os.path.realpath(file.name).replace('\\', '/') + " -c copy " + os.path.normcase(os.path.join(final_file_dir, "output.avi")).replace('\\', '/'))
except:
    print("Error")
