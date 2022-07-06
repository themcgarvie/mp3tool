"""
    MP3Tool

    MP3ToolOptions.py: Object to hold MP3Tool options

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


class MP3ToolOptions:
    tool = None
    source_folder = None
    mp3tool_folder = None
    output_folder = "output\\"
    song = None
    song1 = None
    song2 = None
    song3 = None
    song_vol = 10
    song1_vol = 10
    song2_vol = 10
    song3_vol = 10
    output_file_clip = None
    output_file_reveal = None
    supersonic = 2.0
    custom_output_file = None
    duration = 30


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
