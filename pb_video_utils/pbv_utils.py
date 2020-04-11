#!/usr/bin/env python

import subprocess
import shlex
import json

VIDEO_EXTS = ['.mp4', '.m4p', '.m4v', '.webm', '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.ogg', '.wmv', '.mov', '.qt', '.avi', '.flv', '.swf', '.avchd']

def isNumber(str_val):
    """
    A function which tests whether the input string contains a number of not.
    """
    try:
        float(str_val)  # for int, long and float
    except ValueError:
        try:
            complex(str_val)  # for complex
        except ValueError:
            return False
    return True

def doesJSONPathExist(json_obj, tree_sequence):
    """
    A function which tests whether a path exists within JSON file.
    :param json_obj:
    :param tree_sequence: list of strings
    :return: boolean
    """
    curr_json_obj = json_obj
    steps_str = ""
    pathExists = True
    for tree_step in tree_sequence:
        steps_str = steps_str+":"+tree_step
        if tree_step in curr_json_obj:
            curr_json_obj = curr_json_obj[tree_step]
        else:
            pathExists = False
            break
    return pathExists

def get_video_params(video_file):
    cmd = "ffprobe -v quiet -print_format json -show_streams"
    args = shlex.split(cmd)
    args.append(video_file)
    # run the ffprobe process, decode stdout into utf-8 & convert to JSON
    ffprobe_output = subprocess.check_output(args).decode('utf-8')
    ffprobe_output = json.loads(ffprobe_output)
    
    if isinstance(ffprobe_output['streams'], list):
        n_streams = len(ffprobe_output['streams'])
        video_stream = None
        for stream in ffprobe_output['streams']:
            if isinstance(stream, dict):
                if stream['codec_type'].lower() == 'video':
                    video_stream = stream
            else:
                raise Exception("Expecting stream to be presented by a dict")
    else:
        raise Exception("Expecting ffprobe output to be a list.")
    
    # prints all the metadata available:
    video_params = None
    if video_stream is not None:
        video_params = dict()
        if isNumber(video_stream['nb_frames']):
            video_params['frames'] = int(video_stream['nb_frames'])
        if isNumber(video_stream['width']):
            video_params['frame_width'] = int(video_stream['width'])
        if isNumber(video_stream['height']):
            video_params['frame_height'] = int(video_stream['height'])
        if isNumber(video_stream['duration']):
            video_params['duration_seconds'] = float(video_stream['duration'])
        video_params['codec'] = video_stream['codec_name']
        video_params['codec_descrip'] = video_stream['codec_long_name']
        video_params['rotation'] = 0
        if doesJSONPathExist(video_stream, ['tags', 'rotate']):
            if isNumber(video_stream['tags']['rotate']):
                video_params['rotation'] = float(video_stream['tags']['rotate'])
    
        if ('frames' in video_params) and ('duration_seconds' in video_params):
            video_params['fps'] = float(video_params['frames']) / float(video_params['duration_seconds'])
    
    return video_params
