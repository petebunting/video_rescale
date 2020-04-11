#!/usr/bin/env python

import os
import argparse
import pprint
import subprocess
import shlex
import json

VIDEO_EXTS = ['.mp4', '.m4p', '.m4v', '.webm', '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.ogg', '.wmv', '.mov', '.qt', '.avi', '.flv', '.swf', '.avchd']

"""
def get_video_params(video_file):
    from ffprobe import FFProbe
    metadata=FFProbe(video_file)
    video_params = dict()
    for stream in metadata.streams:
        if stream.is_video():
            video_params['frames'] = stream.frames()
            video_params['frame_size'] = stream.frame_size()
            video_params['pixel_format'] = stream.pixel_format()
            video_params['duration_seconds'] = stream.duration_seconds()
            video_params['codec'] = stream.codec()
            video_params['codec_description'] = stream.codec_description()

    if ('frames' in video_params) and ('duration_seconds' in video_params):
        video_params['fps'] = float(video_params['frames']) / float(video_params['duration_seconds'])

    return video_params
"""

def get_video_params(video_file):
    cmd = "ffprobe -v quiet -print_format json -show_streams"
    args = shlex.split(cmd)
    args.append(video_file)
    # run the ffprobe process, decode stdout into utf-8 & convert to JSON
    ffprobe_output = subprocess.check_output(args).decode('utf-8')
    ffprobe_output = json.loads(ffprobe_output)
    
    if isinstance(ffprobe_output, list):
        n_streams = len(ffprobe_output)
        print("Number Streams: {}".format(n_streams))
        video_stream = None
        for stream in ffprobe_output:
            if isinstance(stream, dict):
                if stream['codec_type'].lower() == 'video':
                    video_stream = stream
            else:
                raise Exception("Expecting stream to be presented by a dict")
    else:
        raise Exception("Expecting ffprobe output to be a list.")
    
    # prints all the metadata available:
    if video_stream is not None:
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(video_stream)
    
    return None

def rescale_file(input_file, output_file):
    video_params = get_video_params(input_file)
    if video_params is not None:
        cmd = None
        print(input_file)
        if (video_params['frame_size'][0] == 1920) and (video_params['frame_size'][1] == 1080):
            print("Export Video without rescaling...")
            cmd = 'docker run -itv $PWD:/data docker_imagemagickffmpeg ffmpeg -i "{}" -c:v libx265 -preset medium -crf 20 -tag:v hvc1 -c:a aac -b:a 224k -b:v 16M -filter:v fps=fps=30 "{}"'.format(input_file, output_file)
        elif video_params['frame_size'][1] > video_params['frame_size'][0]:
            print("Portrait Video - needs padding")
        elif video_params['frame_size'][1] < 1080:
            print("Upscale")
            cmd = 'docker run -itv $PWD:/data docker_imagemagickffmpeg ffmpeg -i "{}" -c:v libx265 -preset medium -crf 20 -tag:v hvc1 -c:a aac -b:a 224k -b:v 16M -filter:v fps=fps=30 -vf scale=1920x1080:flags=lanczos "{}"'.format(input_file, output_file)
        elif video_params['frame_size'][1] > 1080:
            print("Downscale")
            cmd = 'docker run -itv $PWD:/data docker_imagemagickffmpeg ffmpeg -i "{}" -c:v libx265 -preset medium -crf 20 -tag:v hvc1 -c:a aac -b:a 224k -b:v 16M -filter:v fps=fps=30 -vf scale=1920x1080:flags=lanczos "{}"'.format(input_file, output_file)
        if cmd != '':
            print(cmd)

def rescale_dir_videos(input_dir, output_dir):
    input_files = os.listdir(input_dir)
    for input_file in input_files:
        input_file = os.path.join(input_dir, input_file)
        if os.path.isfile(input_file):
            file_ext = os.path.splitext(input_file)[1]
            if file_ext.lower() in VIDEO_EXTS:
                basename = os.path.splitext(os.path.basename(input_file))[0]
                output_file = os.path.join(output_dir, "{}.mp4".format(basename))
                rescale_file(input_file, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help="Input file or directory.")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output file or directory.")
    
    args = parser.parse_args()
    
    if os.path.isfile(args.input):
        if os.path.isdir(args.output):
            raise Exception("The output must be a file as the input is a file.")
        rescale_file(args.input, args.output)
    elif os.path.isdir(args.input):
        if not os.path.isdir(args.output):
            raise Exception("The output must be a directory as the input is a directory.")
        rescale_dir_videos(args.input, args.output)
    else:
        raise Exception("Input is neither a file or directory...")

