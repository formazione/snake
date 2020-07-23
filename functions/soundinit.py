import pygame
from glob import glob
from pathlib import Path
import os
import random

def init(directory):
    '''
        "Initializing pygame and mixer"
    To play a sound:
        pygame.mixer.Sound.play(Puzzle.sounds[name])

    *'name' is the name of the wav file without wav.
    *Puzzle is the name of the class where you put:

    =============== EXAMPLE OF CODE =============
    from functions.soundinit import init, play

    class Puzzle:
        "Class with the global variables"
        #'sounds' is the dir where the sounds are (you can change it).
        sounds = init('sounds')

    def play(snd):
        "To play wav in sounds directory by the name"
        pygame.mixer.Sound.play(Puzzle.sounds[snd]))


    play("click")
    ==============================================
    '''

    # This is to avoid lag
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.mixer.quit()
    pygame.mixer.init(44100, -16, 2, 512)
    pygame.mixer.set_num_channels(32)
    # Load all sounds
    lsounds = glob(f"{directory}/*.mp3")
    # Dictionary with all sounds, keys are the name of wav
    sounds = {}
    random_sounds = []
    for sound in lsounds:
        filepath = Path(sound)
        if filepath.stem.startswith("Marker"):
            random_sounds.append(pygame.mixer.Sound(f"{filepath}"))
        else:
            sounds[filepath.stem] = pygame.mixer.Sound(f"{filepath}")
    return sounds, random_sounds

sounds, random_sounds = init("sounds")
print(sounds)
print(random_sounds)
print(os.getcwd())

def play(snd):
    print(snd)
    pygame.mixer.Sound.play(sounds[snd])

def random_play(snd):
    if random.randrange(1, 5) == 3:
        pygame.mixer.Sound.play(snd)