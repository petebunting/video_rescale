import os
import argparse
import pprint

VIDEO_EXTS = ['mp4', 'mov', 'avi']

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
            video_params['codec_tag'] = stream.codec_tag()
    return video_params


def rescale_file(input_file, output_file):
    video_params = get_video_params(input_file)
    pprint.pprint(video_params)


def rescale_dir_videos(input_dir, output_dir):
    input_files = os.listdir(input_dir)
    for input_file in input_files:
        input_file = os.path.join(input_dir, input_file)
        if os.path.isfile(input_file):
            file_ext = os.path.splitext(input_file)[1]
            print(file_ext)
            if file_ext.lower() in VIDEO_EXTS:
                rescale_file(input_file, '')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help="Input file or directory.")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output file or directory.")
    
    args = parser.parse_args()
    
    if os.path.isfile(args.input):
        rescale_file(args.input, args.output)
    elif os.path.isdir(args.input):
        rescale_dir_videos(args.input, args.output)
    else:
        raise Exception("Input is neither a file or directory...")

