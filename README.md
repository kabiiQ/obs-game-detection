# obs-game-detection

### Support the Developer

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/E1E5AF13X)

A short script for OBS (**Windows** platform only) that seeks to add a "game detection" functionality enabling OBS replay buffer recordings to be automatically placed into sub-directories/folders based on the game being played when it is saved. 

This is similar to the functionality of ShadowPlay instant replay recordings, although desired games must be added manually. 

## Functionality

- Replay buffer output files will be **automatically moved** after being saved to file.

    - If there is a detected game running (add games to `games.cfg`, see below), the buffer recording will be placed into the directory/folder for that game.

    - If there are no detected games running, the buffer recording will be placed in a directory using the current OBS scene name.

- This script will also **start the replay buffer automatically** when OBS launches. This functionality can be disabled by replacing a line near the top of the script `start_buffer_on_startup = True` with `start_buffer_on_startup = False`.

<hr />

## Installation into OBS Studio

- **Install Python3.6.** Python version required is determined by OBS. As of the time of writing (OBS 27.1.3), other versions of Python are not supported. Python3.9 did not work when I first tried. 
    - Download from: https://www.python.org/ftp/python/3.6.0/python-3.6.0-amd64.exe
        - Other download options found at the bottom of [Python Release 3.6.0](https://www.python.org/downloads/release/python-360/)
    - Make note of where Python is installed to!
<br />
- **Point OBS to your Python install**
    - In the OBS script settings, select the directory with your Python3.6 installation.

![](https://i.imgur.com/C0e9Z2z.png)

![](https://i.imgur.com/gwKxZJS.png)

- **Download this script**
    - Place both `obs-game-detection.py` and `games.cfg` in the same directory somewhere on your PC.
    - The "scripts" folder for OBS is at the path `obs-studio/data/obs-plugins/frontend-tools/scripts`, but I would recommend instead placing the script somewhere you can find and edit the `games.cfg` file easily, such as your Documents folder. 
    - Make note of where you place this script.

- **Point OBS to this script** 
    - In the OBS script settings, you can then navigate and add the script. Scripts only need to be added once, and they will start with OBS once added. 

![](https://i.imgur.com/J8GtBM3.png)

<hr /> 

 ## Adding Games

 Adding games to be detected is done in the `games.cfg` file, and the format should be fairly self-explanatory, some examples are included in the file. Each game must be on a new line, and it is the PROCESS NAME (check for running games in task manager, do not include .exe in `games.cfg`). If you wish to specify a custom output folder name for a game, use a colon, as can be seen in the example entries in the file. If no name is provided, the process name will also be used as the folder name. 

 The custom folder name must be a valid Windows filename or the output will fail. Process names can be assumed to be valid Windows filenames. 

 The script must be reloaded (🔁 icon in the OBS scripts UI, or restarting OBS will also accomplish this).

 Non-aliased: The line  `Beat Saber` being present in the `games.cfg` means that if `Beat Saber.exe` is running when the replay buffer is saved, that file will be moved to a `Beat Saber` sub-directory in your recording directory. 

 Aliased: The line `r5apex: Apex Legends` being present in the `games.cfg` means that if `r5apex.exe` is running when the replay buffer is saved, that file will be moved to an `Apex Legends` subdirectory in your recording directory.