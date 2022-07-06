# MP3Tool

MP3 Tool was created to generate audio clips from MP3 files.

MP3Tool has the following abilities:

* Create reverse/backwards clip from a specified or random MP3.
* Create short intro clip from a specified or random MP3.
* Create speed-modified (faster or slower) clip from a specified or random MP3.
* Create a mix from a specified or random MP3s.

## Why?

This was devised to create interesting clips for the Audio part of a Pub Quiz!

# Requirements

Assumes you have Python 3.9.1 installed.

MP3Tool uses the following packages:

* mutagen==1.45.1
* pydub==0.25.1

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements for MP3Tool.

```bash
pip install -r requirements.txt
```
# Usage

```bash
usage: mp3tool.py [-h] -tl TOOL [-sf SOURCE_FOLDER] [-dr DURATION] [-mx MIXES] [-s SONG] [-s1 SONG1] [-s2 SONG2] [-s3 SONG3] [-sv1 SONG1_VOL] [-sv2 SONG2_VOL] [-sv3 SONG3_VOL] [-ss SONG_SPEED] [-cof CUSTOM_OUTPUT_FILE]

MP3 Tool

optional arguments:
  -h, --help            show this help message and exit
  -tl TOOL, --tool TOOL
                        Tool to invoke.
  -sf SOURCE_FOLDER, --source_folder SOURCE_FOLDER
                        Folder to read from
  -dr DURATION, --duration DURATION
                        Duration of clip, 30 seconds default
  -mx MIXES, --mixes MIXES
                        Num of songs to mix 2 or 3
  -s SONG, --song SONG  1st Song
  -s1 SONG1, --song1 SONG1
                        1st Song
  -s2 SONG2, --song2 SONG2
                        2nd Song
  -s3 SONG3, --song3 SONG3
                        3rd Song
  -sv1 SONG1_VOL, --song1_vol SONG1_VOL
                        1st Song Volume
  -sv2 SONG2_VOL, --song2_vol SONG2_VOL
                        2nd Song Volume
  -sv3 SONG3_VOL, --song3_vol SONG3_VOL
                        3rd Song Volume
  -ss SONG_SPEED, --song_speed SONG_SPEED
                        Song Speed, 1.0 = unchanged, < 0 = slower, > 0 = faster
  -cof CUSTOM_OUTPUT_FILE, --custom_output_file CUSTOM_OUTPUT_FILE
                        Output Filename
```

Not all arguments affect every 'tool', i.e. specifying song_speed will have no effect on a clip produced by the 'Intro' tool.

## Usage Examples

Some non-exhaustive usage examples.

Create a 25 second 'Intro' clip of a random file:
```bash
python mp3tool.py -tl intro -sf 'C:\music\' -dr 25
```

Create a 25 second 'Intro' clip of a specific file:
```bash
python mp3tool.py -tl intro -sf 'C:\music\' -s 'song.mp3' -dr 25
```

Create a 25 second 'Reversed' clip of a random file:
```bash
python mp3tool.py -tl reverse -sf 'C:\music\' --duration 25
```

Create a 25 second 'Speed Changed' clip of a random file - slowed down, value must be between 0.1 an 1, 1 being 'normal' speed:
```bash
python mp3tool.py -tl speed_change -sf 'C:\music\' --duration 25 --song_speed 0.5
```

Create a 25 second 'Speed Changed' clip of a random file - made faster, value must be > 1, 1 being 'normal' speed:
```bash
python mp3tool.py -tl speed_change -sf 'C:\music\' --duration 25 --song_speed 0.5
```

Create a 'Mix' of 2 files:
```bash
python mp3tool.py -tl mix -sf 'C:\music\'
```

Create a 'Mix' of 3 files:
```bash
python mp3tool.py -tl mix -sf 'C:\music\' -mx 3
```

Create a 'Mix' of 2 specific files:
```bash
python mp3tool.py -tl mix_selected -s1 'C:\music\song1.mp3' -s2 'C:\music\song2.mp3'
```

Create a 'Mix' of 3 specific files:
```bash
python mp3tool.py -tl mix_selected -s1 'C:\music\song1.mp3' -s2 'C:\music\song2.mp3' -s3 'C:\music\song3.mp3' -mx 3
```

## Known issues

As I put this together for personal use some error handling could perhaps be better, if you find such a case let me know or create a PR!

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)
