import pygame
from glob import glob
from pathlib import Path
import os
import random

def init(directory):
    '''
    How to use this module:

    - THE FOLDER STRUCTURE

    main.py
        |
        functions
        |    |
        |   soundinit.py
        |
        sounds
            |
            click.mp3        call this with play("click")
            Marker #1.mp3    call this with random_play() ... a random sound will be played for the files starting with Marker
            ...

    - HOW TO USE THIS

    In the main.py (or other main file) import like this
    ----------------------------------------------------------
    from functions.soundinit import play, random_play
    
    play("click")
    random_play()
    -----------------------------------------------------------
    @ Giovanni Gatto 2020

    '''

    # This is to avoid lag
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.mixer.quit()
    pygame.mixer.init(44100, -16, 2, 512)
    pygame.mixer.set_num_channels(32)
    # Load all sounds
    lsounds = glob(f"{directory}/*.wav")
    # Dictionary with all sounds, keys are the name of wav
    sounds = {}
    random_sounds = []
    for sound in lsounds:
        filepath = Path(sound)
        # Creates a list with all the sounds that starts with Marker (from fl studio)
        if filepath.stem.startswith("Marker"):
            random_sounds.append(pygame.mixer.Sound(f"{filepath}"))
        else:
            sounds[filepath.stem] = pygame.mixer.Sound(f"{filepath}")
    return sounds, random_sounds

def play(snd):
    "Plays one of the sounds in the sounds folder using play('name')"
    # This is how you play a sound
    pygame.mixer.Sound.play(sounds[snd])


def random_play(rnd=3):
    "Plays a random sounds at a randrange(1, 5) == rnd"
    if random.randrange(1, 5) == rnd:
        sound = pygame.mixer.Sound(random.choice(random_sounds))
        sound.set_volume(1 / random.randrange(1, 10))
        sound.play()

# List of songs for the soundtrack
base = pygame.mixer.music
music = ["sounds/" + f
for f in os.listdir("sounds/")
if f.startswith("base")]

def load_random_song():
    song = random.choice(music)
    return song

def soundtrack(play="yes", loop=1):
    "This load a base from sounds directory"
    filename = load_random_song()
    if play == "yes":
        base.load(filename)
    elif play == "stop" and filename != None:
        base.stop()
    if loop == 1 and play == "yes":
        base.play(-1)

sounds, random_sounds = init("sounds")