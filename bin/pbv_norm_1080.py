#!/usr/bin/env python

import os
import argparse
import pprint

from pb_video_utils/pbv_utils import VIDEO_EXTS
from pb_video_utils/pbv_utils import get_video_params

def rescale_file(input_file, output_file):
    video_params = get_video_params(input_file)
    pprint.pprint(video_params)
    if video_params is not None:
        cmd = None
        print(input_file)
        if (video_params['frame_width'] == 1920) and (video_params['frame_height'] == 1080) and ((video_params['rotation'] == 0) or (video_params['rotation'] == 180)):
            print("Export Video without rescaling...")
            cmd = 'docker run -itv $PWD:/data docker_imagemagickffmpeg ffmpeg -i "{}" -c:v libx265 -preset medium -crf 20 -tag:v hvc1 -c:a aac -b:a 224k -b:v 16M -filter:v fps=fps=30 "{}"'.format(input_file, output_file)
        elif (video_params['frame_height'] > video_params['frame_width']) or ((video_params['rotation'] != 0) and (video_params['rotation'] != 180)):
            print("Portrait Video - needs padding")
            
            
            
            
        elif (video_params['frame_height'] < 1080) and ((video_params['rotation'] == 0) or (video_params['rotation'] == 180)):
            print("Upscale")
            cmd = 'docker run -itv $PWD:/data docker_imagemagickffmpeg ffmpeg -i "{}" -c:v libx265 -preset medium -crf 20 -tag:v hvc1 -c:a aac -b:a 224k -b:v 16M -filter:v fps=fps=30 -vf scale=1920x1080:flags=lanczos "{}"'.format(input_file, output_file)
        elif (video_params['frame_height'] > 1080) and ((video_params['rotation'] == 0) or (video_params['rotation'] == 180)):
            print("Downscale")
            cmd = 'docker run -itv $PWD:/data docker_imagemagickffmpeg ffmpeg -i "{}" -c:v libx265 -preset medium -crf 20 -tag:v hvc1 -c:a aac -b:a 224k -b:v 16M -filter:v fps=fps=30 -vf scale=1920x1080:flags=lanczos "{}"'.format(input_file, output_file)
        else:
            raise Exception("Do not know what to do with input file: '{}'".format(input_file))
        if cmd is not None:
            print(cmd)
    else:
        raise Exception("The video paramaters could not be found...")
    print("\n\n")

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

