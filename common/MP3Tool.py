"""
    MP3Tool

    MP3Tool.py: Main functionality for MP3Tool options

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


from calendar import c
import os
import random
from stat import S_ISBLK
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from pydub import AudioSegment
from pydub.utils import mediainfo
from common import Utils
from common.MP3ToolOptions import color


class MP3Tool:

    MP3ToolOptions = None
    bitrate = None
    output_file = None
    song_base_name = None
    tag_title = None
    tag_artist = None

    def __init__(self, aMP3ToolOptions):
        self.MP3ToolOptions = aMP3ToolOptions
        if not os.path.exists(self.MP3ToolOptions.output_folder):
            os.makedirs(self.MP3ToolOptions.output_folder)
            os.makedirs(self.MP3ToolOptions.output_folder+"backwards\\")
            os.makedirs(self.MP3ToolOptions.output_folder+"intro\\")
            os.makedirs(self.MP3ToolOptions.output_folder+"speedchange\\")
            os.makedirs(self.MP3ToolOptions.output_folder+"mix\\")

    def determineSong(self):
        if self.MP3ToolOptions.song is None:
            print("Input file:\t\t" + color.BOLD + "Random!!!" + color.END)
            allMp3s = Utils.findFiles(
                '*.mp3', self.MP3ToolOptions.source_folder)
            allMp3s_sample = random.sample(allMp3s, 1)
            self.MP3ToolOptions.song = allMp3s_sample[0]
        else:
            print("Input file:\t\t" + color.BOLD +
                  f"{self.MP3ToolOptions.song}" + color.END)

            self.MP3ToolOptions.song = self.MP3ToolOptions.source_folder+self.MP3ToolOptions.song

        print("File Selected:\t\t" + color.BOLD +
              f"{self.MP3ToolOptions.song}" + color.END)

    def determineMediaInfo(self):
        # Read song file
        try:
            mp3Info = mediainfo(self.MP3ToolOptions.song)
            self.MP3ToolOptions.song_mp3Info = mp3Info
            self.MP3ToolOptions.song_ID3_tags = EasyID3(
                self.MP3ToolOptions.song)
        except Exception as e:
            print("Problem with input file, aborted.")
            print(e)
            exit(1)

        # Check for we have an ID3 tag and the required elements
        if len(self.MP3ToolOptions.song_ID3_tags) == 0:
            print("Input file has no ID3 tag, aborted.")
            exit(1)

        tags_found = True
        tags_missing = ''
        if 'title' not in self.MP3ToolOptions.song_ID3_tags:
            tags_found = False
            self.tags_missing += " 'title' "
        else:
            self.tag_title = self.MP3ToolOptions.song_ID3_tags.get('title', [])[
                0]

        if 'artist' not in self.MP3ToolOptions.song_ID3_tags:
            tags_found = False
            tags_missing += " 'artist' "
        else:
            self.tag_artist = self.MP3ToolOptions.song_ID3_tags.get('artist', [])[
                0]

        if tags_found == False:
            print("ID3 tag has missing required items, aborted. Missing: ", tags_missing)
            exit(1)

        # Get the base name of the song
        f_song = os.path.basename(self.MP3ToolOptions.song).replace(
            " ", "_").replace(".mp3", "")

        # Determine the base output file name, based on ID3 tag info
        if self.MP3ToolOptions.custom_output_file != None:
            self.output_file = self.MP3ToolOptions.custom_output_file
        else:
            if tags_found:
                self.song_base_name = self.tag_artist + \
                    "_" + self.tag_title
            else:
                self.song_base_name = f_song

            self.output_file = self.song_base_name.replace(" ", "_").replace(
                "/", "-").replace("\"", "").replace("\"", "").replace("'", "")

        print("Output Folder:\t\t" + color.BOLD +
              f"{self.MP3ToolOptions.output_folder}" + color.END)
        print("Output File Base Name:\t" + color.BOLD +
              f"{self.output_file}" + color.END)

    def setMediaInfo(self, song, clip_type, clip_method):
        # Create Tags object
        tags = EasyID3(self.MP3ToolOptions.mp3tool_folder+"\\"+song)

        # Set the title & save it
        tags['title'] = self.tag_title+" by " + \
            self.tag_artist+": "+clip_method+" - "+clip_type
        tags['artist'] = self.tag_artist
        tags.save()

    def songReverse(self):
        # Determine the song, if not specified in the command line (--song) a random song will be selected
        print(color.BOLD + color.GREEN +
              "Create reverse intro/clip from selected song." + color.END + "\n")
        self.MP3ToolOptions.output_folder = "output\\backwards\\"
        self.determineSong()
        self.determineMediaInfo()

        # Specify the output file fadeout and duration
        fade_time = 3000
        duration_clip = Utils.durationInMs(self.MP3ToolOptions.duration)
        reveal_start = Utils.getMsTime("0:00:15")
        reveal_end = Utils.getMsTime("0:00:45")
        print("Duration:\t\t" + color.BOLD +
              f"{self.MP3ToolOptions.duration} seconds" + color.END)

        # Read song file
        try:
            song = AudioSegment.from_mp3(self.MP3ToolOptions.song)
        except Exception as e:
            print("Problem with input file, aborted.")
            print(e)
            exit(1)

        # Extract segment and reverse it
        song_extract = song[0:duration_clip]
        song_reversed = song_extract.reverse()
        song_extract_reveal = song[reveal_start:reveal_end]

        # Add fade in/out to clips
        song_reversed_with_fade = song_reversed.fade_in(fade_time)
        song_reversed_with_fade = song_reversed_with_fade.fade_out(fade_time)
        song_reveal = song_extract_reveal.fade_in(fade_time)
        song_reveal = song_reveal.fade_out(fade_time)

        # Saving
        try:
            file_clip = self.MP3ToolOptions.output_folder + self.output_file + "_Clip.mp3"
            file_reveal = self.MP3ToolOptions.output_folder + self.output_file + "_Reveal.mp3"
            song_reversed_with_fade.export(
                file_clip,
                format="mp3")
            song_reveal.export(
                file_reveal,
                format="mp3")
            print("Clip:\t\t\t" + color.BOLD + f"{file_clip}" + color.END)
            print("Reveal:\t\t\t" + color.BOLD + f"{file_reveal}" + color.END)
        except Exception as e:
            print("Problem with output file(s), aborted.")
            print(e)
            exit(1)

        self.setMediaInfo(file_clip, 'CLIP', 'Backwards')
        self.setMediaInfo(file_reveal, 'REVEAL', 'Backwards')

    def songIntro(self):
        # Determine the song, if not specified in the command line (--song) a random song will be selected
        print(color.BOLD + color.GREEN +
              "Create intro/clip from selected song." + color.END + "\n")
        self.MP3ToolOptions.output_folder = "output\\intro\\"
        self.determineSong()
        self.determineMediaInfo()

        # Specify the output file fadeout, duration and reveal timings
        fade_time = 2000
        duration_clip = Utils.durationInMs(self.MP3ToolOptions.duration)
        reveal_start = Utils.getMsTime("0:00:15")
        reveal_end = Utils.getMsTime("0:00:45")
        print("Duration:\t\t" + color.BOLD +
              f"{self.MP3ToolOptions.duration} seconds" + color.END)

        # Read song file
        try:
            song = AudioSegment.from_mp3(self.MP3ToolOptions.song)
        except Exception as e:
            print("Problem with input file, aborted.")
            print(e)
            exit(1)

        # Extract segments
        song_extract = song[0:duration_clip]
        song_extract_reveal = song[reveal_start:reveal_end]

        # Add fade in/out to clips
        song_intro = song_extract.fade_out(fade_time)
        song_reveal = song_extract_reveal.fade_in(fade_time)
        song_reveal = song_reveal.fade_out(fade_time)

        # Save Clip and Reveal
        try:
            file_clip = self.MP3ToolOptions.output_folder + self.output_file + "_Clip.mp3"
            file_reveal = self.MP3ToolOptions.output_folder + self.output_file + "_Reveal.mp3"
            song_intro.export(
                file_clip,
                format="mp3")
            song_reveal.export(
                file_reveal,
                format="mp3")
            print("Clip:\t\t\t" + color.BOLD + f"{file_clip}" + color.END)
            print("Reveal:\t\t\t" + color.BOLD + f"{file_reveal}" + color.END)
        except Exception as e:
            print("Problem with output file(s), aborted.")
            print(e)
            exit(1)

        self.setMediaInfo(file_clip, 'CLIP', 'Intro')
        self.setMediaInfo(file_reveal, 'REVEAL', 'Intro')

    def songSpeedChange(self):
        # Determine the song, if not specified in the command line (--song) a random song will be selected
        print(color.BOLD + color.GREEN +
              "Create fast or slow clip from selected song." + color.END + "\n")
        self.MP3ToolOptions.output_folder = "output\\speedchange\\"
        self.determineSong()
        self.determineMediaInfo()

        # Specify the output file fadeout, duration and reveal timings
        fade_time = 2000
        if self.MP3ToolOptions.song_speed < 1:
            duration_clip = Utils.durationInMs(self.MP3ToolOptions.duration)/2
        else:
            duration_clip = Utils.durationInMs(self.MP3ToolOptions.duration)
        reveal_start = Utils.getMsTime("0:00:15")
        reveal_end = Utils.getMsTime("0:00:45")
        print("Song Speed:\t\t" + color.BOLD +
              f"{self.MP3ToolOptions.song_speed}" + color.END)
        print("Duration:\t\t" + color.BOLD +
              f"{self.MP3ToolOptions.duration} seconds" + color.END)

        # Opening file
        try:
            song = AudioSegment.from_mp3(self.MP3ToolOptions.song)
        except Exception as e:
            print("Problem with input file, aborted.")
            print(e)
            exit(1)

        # Extract segments
        song_extract = song[0:duration_clip]
        song_extract_longer = song[reveal_start:reveal_end]

        # Add fade in/out to clips
        song_clip = song_extract.fade_out(fade_time)
        song_reveal = song_extract_longer.fade_in(fade_time)
        song_reveal = song_reveal.fade_out(fade_time)

        # Change speed of song
        speed_change_song = Utils.changeSongSpeed(
            song_clip, self.MP3ToolOptions.song_speed)

        # Save Clip and Reveal
        try:
            file_clip = self.MP3ToolOptions.output_folder + self.output_file + "_Clip.mp3"
            file_reveal = self.MP3ToolOptions.output_folder + self.output_file + "_Reveal.mp3"
            speed_change_song.export(
                file_clip,
                format="mp3")
            song_reveal.export(
                file_reveal,
                format="mp3")
            print("Clip:\t\t\t" + color.BOLD + f"{file_clip}" + color.END)
            print("Reveal:\t\t\t" + color.BOLD + f"{file_reveal}" + color.END)
        except Exception as e:
            print("Problem with output file(s), aborted.")
            print(e)
            exit(1)

        self.setMediaInfo(file_clip, 'CLIP', 'Speed Change')
        self.setMediaInfo(file_reveal, 'REVEAL', 'Speed Change')

    def songMix(self):
        print(color.BOLD + color.GREEN +
              f"Create mix from {self.MP3ToolOptions.mixes} random MP3s!" + color.END + "\n")

        # Get 3 random MP3s
        self.MP3ToolOptions.output_folder = "output\\mix\\"
        allMp3s = Utils.findFiles('*.mp3', self.MP3ToolOptions.source_folder)
        allMp3s_sample = random.sample(allMp3s, 3)

        # How many songs are we mixing?
        if self.MP3ToolOptions.mixes == 2:
            # Mix 2 songs...
            self.MP3ToolOptions.song1 = allMp3s_sample[0]
            self.MP3ToolOptions.song2 = allMp3s_sample[1]

            f_song1 = os.path.basename(allMp3s_sample[0]).replace(
                " ", "_").replace(".mp3", "")
            f_song2 = os.path.basename(allMp3s_sample[1]).replace(
                " ", "_").replace(".mp3", "")
            self.MP3ToolOptions.outputFile = f_song1 + "--" + f_song2 + ".mp3"

            if self.MP3ToolOptions.custom_output_file != None:
                self.MP3ToolOptions.outputFile = self.MP3ToolOptions.custom_output_file

            print("Song 1:\t\t" + color.BOLD +
                  f"{self.MP3ToolOptions.song1}" + color.END)
            print("Song 2:\t\t" + color.BOLD +
                  f"{self.MP3ToolOptions.song2}" + color.END)

        else:
            # Mix 3 songs...
            self.MP3ToolOptions.song1 = allMp3s_sample[0]
            self.MP3ToolOptions.song2 = allMp3s_sample[1]
            self.MP3ToolOptions.song3 = allMp3s_sample[2]

            f_song1 = os.path.basename(allMp3s_sample[0]).replace(
                " ", "_").replace(".mp3", "")
            f_song2 = os.path.basename(allMp3s_sample[1]).replace(
                " ", "_").replace(".mp3", "")
            f_song3 = os.path.basename(allMp3s_sample[2]).replace(
                " ", "_").replace(".mp3", "")
            self.MP3ToolOptions.outputFile = f_song1 + \
                "--" + f_song2 + "--" + f_song3 + ".mp3"

            if self.MP3ToolOptions.custom_output_file != None:
                self.MP3ToolOptions.outputFile = self.MP3ToolOptions.custom_output_file

            print("Song 1:\t\t" + color.BOLD +
                  f"{self.MP3ToolOptions.song1}" + color.END)
            print("Song 2:\t\t" + color.BOLD +
                  f"{self.MP3ToolOptions.song2}" + color.END)
            print("Song 3:\t\t" + color.BOLD +
                  f"{self.MP3ToolOptions.song3}" + color.END)

        # Opening file
        try:
            song1 = AudioSegment.from_mp3(self.MP3ToolOptions.song1)
            song2 = AudioSegment.from_mp3(self.MP3ToolOptions.song2)
            if self.MP3ToolOptions.mixes != 2:
                song3 = AudioSegment.from_mp3(self.MP3ToolOptions.song3)
        except Exception as e:
            print("Problem with input file, aborted.")
            print(e)
            exit(1)

        # Specify the output file fadeout, duration and reveal timings
        hms_start = "0:01:00"
        hms_end = "0:01:30"
        start_time = Utils.getMsTime(hms_start)
        end_time = Utils.getMsTime(hms_end)

        # Extract segments
        song_extract1 = song1[start_time:end_time]
        song_extract2 = song2[start_time:end_time]
        if self.MP3ToolOptions.mixes != 2:
            song_extract3 = song3[start_time:end_time]

        # Normalize volume
        song1_vol = -self.MP3ToolOptions.song1_vol
        song2_vol = -self.MP3ToolOptions.song2_vol
        song1_adjusted = Utils.soundSetToTargetLevel(
            song_extract1, song1_vol)
        song2_adjusted = Utils.soundSetToTargetLevel(
            song_extract2, song2_vol)
        if self.MP3ToolOptions.mixes != 2:
            song3_vol = -self.MP3ToolOptions.song3_vol
            song3_adjusted = Utils.soundSetToTargetLevel(
                song_extract3, song3_vol)

        # Create the mix by combining the extracted segments
        played_together = song1_adjusted.overlay(song2_adjusted)
        if self.MP3ToolOptions.mixes != 2:
            played_together2 = played_together.overlay(song3_adjusted)

        # Get bitrate
        mp3Info = mediainfo(self.MP3ToolOptions.song1)
        if "bit_rate" in mp3Info:
            original_bitrate = mp3Info['bit_rate']
        else:
            original_bitrate = 128000

        # Save Mix
        try:
            file_mix = self.MP3ToolOptions.output_folder + self.MP3ToolOptions.outputFile
            if self.MP3ToolOptions.mixes == 2:
                played_together.export(
                    file_mix, format="mp3", bitrate=original_bitrate)
            else:
                played_together2.export(
                    file_mix, format="mp3", bitrate=original_bitrate)
            print("Mix File:\t" + color.BOLD + f"{file_mix}" + color.END)
        except Exception as e:
            print("Problem creating output file, aborted.")
            print(e)
            exit(1)

    def songMixSelected(self):
        print(color.BOLD + color.GREEN +
              f"Create mix from {self.MP3ToolOptions.mixes} MP3s!" + color.END + "\n")
        self.MP3ToolOptions.output_folder = "output\\mix\\"

        # How many songs are we mixing?
        if self.MP3ToolOptions.mixes == 2:
            # Mix 2 songs...
            if self.MP3ToolOptions.song1 is None:
                print("Must Specify Song 1!")
                exit(1)

            if self.MP3ToolOptions.song2 is None:
                print("Must Specify Song 2!")
                exit(1)

            f_song1 = os.path.basename(self.MP3ToolOptions.song1).replace(
                " ", "_").replace(".mp3", "")
            f_song2 = os.path.basename(self.MP3ToolOptions.song2).replace(
                " ", "_").replace(".mp3", "")
            self.MP3ToolOptions.outputFile = f_song1 + "--" + f_song2 + ".mp3"

            print("Song 1:\t\t" + color.BOLD +
                  f"{self.MP3ToolOptions.song1}" + color.END)
            print("Song 2:\t\t" + color.BOLD +
                  f"{self.MP3ToolOptions.song2}" + color.END)

        else:
            # Mix 3 songs...
            f_song1 = os.path.basename(self.MP3ToolOptions.song1).replace(
                " ", "_").replace(".mp3", "")
            f_song2 = os.path.basename(self.MP3ToolOptions.song2).replace(
                " ", "_").replace(".mp3", "")
            f_song3 = os.path.basename(self.MP3ToolOptions.song3).replace(
                " ", "_").replace(".mp3", "")
            self.MP3ToolOptions.outputFile = f_song1 + \
                "--" + f_song2 + "--" + f_song3 + ".mp3"

            print("Song 1:\t\t" + color.BOLD +
                  f"{self.MP3ToolOptions.song1}" + color.END)
            print("Song 2:\t\t" + color.BOLD +
                  f"{self.MP3ToolOptions.song2}" + color.END)
            print("Song 3:\t\t" + color.BOLD +
                  f"{self.MP3ToolOptions.song3}" + color.END)

        # Opening file
        try:
            song1 = AudioSegment.from_mp3(self.MP3ToolOptions.song1)
            song2 = AudioSegment.from_mp3(self.MP3ToolOptions.song2)
            if self.MP3ToolOptions.mixes != 2:
                song3 = AudioSegment.from_mp3(self.MP3ToolOptions.song3)
        except Exception as e:
            print("Problem with input file, aborted.")
            print(e)
            exit(1)

        # Specify the output file fadeout, duration and reveal timings
        hms_start = "0:00:30"
        hms_end = "0:01:00"
        start_time = Utils.getMsTime(hms_start)
        end_time = Utils.getMsTime(hms_end)

        # Extract segments
        song_extract1 = song1[start_time:end_time]
        song_extract2 = song2[start_time:end_time]
        if self.MP3ToolOptions.mixes != 2:
            song_extract3 = song3[start_time:end_time]

        # Normalize volume
        song1_vol = -self.MP3ToolOptions.song1_vol
        song2_vol = -self.MP3ToolOptions.song2_vol
        if self.MP3ToolOptions.mixes != 2:
            song3_vol = -self.MP3ToolOptions.song3_vol
        song1_adjusted = Utils.soundSetToTargetLevel(
            song_extract1, song1_vol)
        song2_adjusted = Utils.soundSetToTargetLevel(
            song_extract2, song2_vol)
        if self.MP3ToolOptions.mixes != 2:
            song3_adjusted = Utils.soundSetToTargetLevel(
                song_extract3, song3_vol)

        # Create the mix by combining the extracted segments
        played_together = song1_adjusted.overlay(song2_adjusted)
        if self.MP3ToolOptions.mixes != 2:
            played_together2 = played_together.overlay(song3_adjusted)

        # Get bitrate
        mp3Info = mediainfo(self.MP3ToolOptions.song1)
        if "bit_rate" in mp3Info:
            original_bitrate = mp3Info['bit_rate']
        else:
            original_bitrate = 128000

        # Opening file
        try:
            file_mix = self.MP3ToolOptions.output_folder + self.MP3ToolOptions.outputFile
            if self.MP3ToolOptions.mixes == 2:
                played_together.export(self.MP3ToolOptions.output_folder +
                                       self.MP3ToolOptions.outputFile, format="mp3", bitrate=original_bitrate)
            else:
                played_together2.export(self.MP3ToolOptions.output_folder +
                                        self.MP3ToolOptions.outputFile, format="mp3", bitrate=original_bitrate)
            print("Mix File:\t" + color.BOLD + f"{file_mix}" + color.END)
        except Exception as e:
            print("Problem creating output file, aborted.")
            print(e)
            exit(1)
