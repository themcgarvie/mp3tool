"""
    MP3Tool
    
    Utils.py: Utility functions

    *********PLEASE READ THE README.md FOR USE INSTRUCTIONS*********

    Copyright 2022 by Brian M McGarvie (brian@mcgarvie.net)

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    https://choosealicense.com/licenses/apache-2.0/

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""


import os
import fnmatch


def getMsTime(t_hms):
    """
    Convert time in HH:MM:SS format to milliseconds

    Arguments:
    t_hms -- Time in HH:MM:SS format
    imag -- the imaginary part

    Return:
    Time expressed in milliseconds
    """
    t_hours, t_minutes, t_seconds = (["0", "0"] + t_hms.split(":"))[-3:]
    t_hours = int(t_hours)
    t_minutes = int(t_minutes)
    t_seconds = float(t_seconds)
    t_time = int(3600000 * t_hours + 60000 * t_minutes + 1000 * t_seconds)
    return t_time


def durationInMs(seconds):
    """
    Convert seconds to milliseconds

    Arguments:
    seconds -- duration in seconds

    Return:
    Time expressed in milliseconds
    """
    return seconds * 1000


def soundSetToTargetLevel(sound, target_level):
    """
    Set sound volume to target level

    Arguments:
    sound - dydub sound object
    target_level - target level

    Return:
    Modified dydub sound object
    """
    difference = target_level - sound.dBFS
    return sound.apply_gain(difference)


def changeSongSpeed(sound, speed=1.0):
    """
    Modify the speed of a sound object

    Arguments:
    sound - dydub sound object
    speed - speed multiplier

    Return:
    Modified dydub sound object
    """
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })
    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


def findFiles(pattern, path):
    """
    Find files matching pattern in path

    Arguments:
    pattern - file pattern
    path - path to search

    Return:
    List of files matching pattern in path
    """
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result
