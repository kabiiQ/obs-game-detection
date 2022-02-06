import csv
import os
import shutil
import subprocess
from io import StringIO

import obspython as obs

# CONFIG

alias_filename = "games.cfg"
start_buffer_on_startup = True

# END CONFIG

aliases: dict

# OBS GLOBAL FUNCTION EXPORTS

def script_description():
    return f"Assists in placing recordings into subdirectories using active game/scene info.\n\nAdd games for detection by adding the process to {alias_filename}.\n\nAdditionally, starts the replay buffer on startup."

def script_load(settings):
    # load process:game aliases
    try:
        with open(os.path.join(os.path.dirname(__file__), alias_filename)) as cfg:
            global aliases
            aliases = dict(load_aliases(cfg.readlines()))
            obs.script_log(obs.LOG_INFO, f"Loaded {len(aliases)} process aliases from {alias_filename}.")
    except IOError as err:
        obs.script_log(obs.LOG_ERROR, f"Unable to open game alias file: {alias_filename}. :: {err}")
    
    # hook OBS events
    obs.obs_frontend_add_event_callback(on_event)

    # start replay buffer
    if start_buffer_on_startup:
        obs.obs_frontend_replay_buffer_start()

# END GLOBAL FUNCTION EXPORTS 

def load_aliases(lines):
    for line in lines:
        if line.strip():
            split = line.strip().split(":", 1)
            if len(split) > 1:
                yield [split[0].strip() + '.exe', split[1].strip()]
            else:
                yield [split[0].strip() + '.exe', split[0].strip()]

def detect():
    # pull process list
    tasklist = subprocess.run(['tasklist', '/FO', 'csv', '/NH'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    io = StringIO(tasklist.stdout)
    reader = csv.reader(io)
    for row in reader:
        if row[0] in aliases:
            match = aliases[row[0]]
            obs.script_log(obs.LOG_INFO, f"Process match found: {match}")
            return match

def on_event(event):
    if event == obs.OBS_FRONTEND_EVENT_REPLAY_BUFFER_SAVED:
        on_replay_buffer_saved()

def on_replay_buffer_saved():
    game = detect()
    if not game: 
        scene = obs.obs_frontend_get_current_scene()
        game = obs.obs_source_get_name(scene)
        obs.script_log(obs.LOG_INFO, f"No process match found, using scene: {game}")

    # access last saved replay file
    replay_buffer = obs.obs_frontend_get_replay_buffer_output()

    call = obs.calldata_create()
    proc = obs.obs_output_get_proc_handler(replay_buffer)
    obs.proc_handler_call(proc, "get_last_replay", call)
    replay = obs.calldata_string(call, "path")

    obs.calldata_destroy(call)
    obs.obs_output_release(replay_buffer)

    obs.script_log(obs.LOG_INFO, f"Replay buffer output detected: {replay}")

    root = os.path.dirname(replay)
    filename = os.path.basename(replay)
    
    target_dir = os.path.normpath(os.path.join(root, game))
    target_full = os.path.join(target_dir, filename)

    obs.script_log(obs.LOG_INFO, f"Moving {replay} to {target_dir}")

    os.makedirs(target_dir, exist_ok=True)
    shutil.move(replay, target_full)
