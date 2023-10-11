import pygame

from settings import *

pygame.mixer.init()
pygame.init()

# load all sounds
# battle music
pygame.mixer.music.load(path.join(snd_dir, 'battle.wav'))

# bottle
heal_snd = pygame.mixer.Sound(path.join(snd_dir, 'spell.wav'))
heal_snd.set_volume(0.6)

# sword attack
sword_snd = []
for i in range(1, 4):
    sword_s = pygame.mixer.Sound(path.join(snd_dir, f'swing{i}.wav'))
    sword_s.set_volume(0.7)
    sword_snd.append(sword_s)

# magic attack
magic_snd = []
for i in range(1, 5):
    magic_s = pygame.mixer.Sound(path.join(snd_dir, f'magic{i}.ogg'))
    magic_s.set_volume(0.4)
    magic_snd.append(magic_s)

# hit
hit_snd = pygame.mixer.Sound(path.join(snd_dir, 'hit.wav'))
hit_snd.set_volume(0.7)

# death sounds
knight_death_snd = pygame.mixer.Sound(path.join(snd_dir, 'knight-death.wav'))
knight_death_snd.set_volume(0.8)
warrior_death_snd = pygame.mixer.Sound(path.join(snd_dir, 'warrior-death.wav'))
warrior_death_snd.set_volume(0.9)
witch_death_snd = pygame.mixer.Sound(path.join(snd_dir, 'witch-death.wav'))
human_death_snd = pygame.mixer.Sound(path.join(snd_dir, 'human-death.wav'))
human_death_snd.set_volume(0.7)
skeleton_death_snd = pygame.mixer.Sound(path.join(snd_dir, 'skeleton-death.wav'))
skeleton_death_snd.set_volume(0.7)
fly_death_snd = pygame.mixer.Sound(path.join(snd_dir, 'fly-death.wav'))
fly_death_snd.set_volume(0.7)
worm_death_snd = pygame.mixer.Sound(path.join(snd_dir, 'worm-death.wav'))
worm_death_snd.set_volume(0.7)
