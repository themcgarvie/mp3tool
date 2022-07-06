"""
    MP3Tool
    
    mp3tool.py: Main program file

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


import argparse
from ensurepip import version
import sys
import os
from unicodedata import decimal
from common.MP3Tool import MP3Tool
from common.MP3ToolOptions import MP3ToolOptions


def parse_args():
    parser = argparse.ArgumentParser(description="MP3 Tool")
    if len(sys.argv) == 1:
        parser.format_help()
        parser.print_usage = parser.print_help
    parser.add_argument("-tl", "--tool", type=str,
                        required=True, help="Tool to invoke.")
    parser.add_argument("-sf", "--source_folder", type=str,
                        help="Folder to read from")
    parser.add_argument("-dr", "--duration", type=str,
                        help="Duration of clip, 30 seconds default")
    parser.add_argument("-mx", "--mixes", type=int,
                        default=2, help="Num of songs to mix 2 or 3")
    parser.add_argument("-s", "--song", type=str, help="1st Song")
    parser.add_argument("-s1", "--song1", type=str, help="1st Song")
    parser.add_argument("-s2", "--song2", type=str, help="2nd Song")
    parser.add_argument("-s3", "--song3", type=str, help="3rd Song")
    parser.add_argument("-sv1", "--song1_vol", type=int,
                        default=20, help="1st Song Volume")
    parser.add_argument("-sv2", "--song2_vol", type=int,
                        default=20, help="2nd Song Volume")
    parser.add_argument("-sv3", "--song3_vol", type=int,
                        default=20, help="3rd Song Volume")
    parser.add_argument("-ss", "--song_speed", type=float,
                        default=2.0, help="Song Speed, 1.0 = unchanged, < 0 = slower, > 0 = faster")
    parser.add_argument("-cof", "--custom_output_file",
                        type=str, default=None, help="Output Filename")
    args = parser.parse_args()

    # Required
    MP3ToolOptions.tool = args.tool
    if MP3ToolOptions.tool == "mix_selected":
        MP3ToolOptions.source_folder = None
    else:
        MP3ToolOptions.source_folder = args.source_folder

    # Optional
    if args.mixes is not None:
        MP3ToolOptions.mixes = int(args.mixes)
    if args.song is not None:
        MP3ToolOptions.song = args.song
    if args.song1 is not None:
        MP3ToolOptions.song1 = args.song1
    if args.song2 is not None:
        MP3ToolOptions.song2 = args.song2
    if args.song3 is not None:
        MP3ToolOptions.song3 = args.song3
    if args.song1_vol is not None:
        MP3ToolOptions.song_vol = int(args.song1_vol)
    if args.song2_vol is not None:
        MP3ToolOptions.song2_vol = int(args.song2_vol)
    if args.song3_vol is not None:
        MP3ToolOptions.song3_vol = int(args.song3_vol)
    if args.song_speed is not None:
        MP3ToolOptions.song_speed = args.song_speed
    if args.custom_output_file is not None:
        MP3ToolOptions.custom_output_file = args.custom_output_file
    if args.duration is not None:
        MP3ToolOptions.duration = int(args.duration)

    return parser.parse_known_args()


def main():
    # Parse args & initialise MP3Tool
    args, unknown = parse_args()
    mp3Tool = MP3Tool(MP3ToolOptions)
    MP3ToolOptions.mp3tool_folder = os.path.dirname(os.path.realpath(__file__))

    # What tool are we running?
    if MP3ToolOptions.tool == "reverse":
        mp3Tool.songReverse()
    elif MP3ToolOptions.tool == "intro":
        mp3Tool.songIntro()
    elif MP3ToolOptions.tool == "speed_change":
        mp3Tool.songSpeedChange()
    elif MP3ToolOptions.tool == "mix":
        mp3Tool.songMix()
    elif MP3ToolOptions.tool == "mix_selected":
        mp3Tool.songMixSelected()
    else:
        print("Unknown tool.")


if __name__ == "__main__":
    # Check python version, if not 3.9 display warning
    version = sys.version_info[0]
    if version < 4.9:  # python 3.9
        print("Python 3.9 or higher is recommended to ensure compatibility.")

    main()
