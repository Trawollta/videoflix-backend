import subprocess
import os

def convertVideos(source):
    new_file_name_480p = os.path.splitext(source.video_file_1080p.path)[0] + '_480p.mp4'
    new_file_name_720p = os.path.splitext(source.video_file_1080p.path)[0] + '_720p.mp4'

    converted480p = convert480p(source.video_file_1080p.path, new_file_name_480p)
    converted720p = convert720p(source.video_file_1080p.path, new_file_name_720p)

    if converted480p:
        source.video_file_480p.name = 'videos/' + os.path.basename(new_file_name_480p)
    if converted720p:
        source.video_file_720p.name = 'videos/' + os.path.basename(new_file_name_720p)

    source.save()

def convert480p(input_file, output_file):
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-s', 'hd480',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        output_file
    ]
    run = subprocess.run(cmd, capture_output=True, text=True)

    if run.returncode == 0:
        return True
    else:
        print("Fehler bei der Konvertierung (480p):", run.stderr)
        return False

def convert720p(input_file, output_file):
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-s', 'hd720',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        output_file
    ]
    run = subprocess.run(cmd, capture_output=True, text=True)

    if run.returncode == 0:
        return True
    else:
        print("Fehler bei der Konvertierung (720p):", run.stderr)
        return False

def convert1080p(input_file, output_file):
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-s', 'hd1080',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        output_file
    ]
    run = subprocess.run(cmd, capture_output=True, text=True)

    if run.returncode == 0:
        return True
    else:
        print("Fehler bei der Konvertierung (1080p):", run.stderr)
        return False
