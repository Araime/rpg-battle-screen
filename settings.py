from os import listdir, path

import pygame

hero_dir = path.join(path.dirname(__file__), 'img', 'heroes')
enemy_dir = path.join(path.dirname(__file__), 'img', 'enemies')
bg_dir = path.join(path.dirname(__file__), 'img', 'bg')
ico_dir = path.join(path.dirname(__file__), 'img', 'icons')
snd_dir = path.join(path.dirname(__file__), 'snd')
effect_dir = path.join(path.dirname(__file__), 'img', 'effects')

# define colours
red = (255, 0, 0)
green = (0, 255, 0)
gold = (255, 215, 0)
white = (255, 255, 255)
