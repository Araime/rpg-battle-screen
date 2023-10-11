import pygame

from settings import *

# game window
bottom_panel = 150
screen_width = 800
screen_height = 450 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption('RPG Battle')

# load images
# panel image
panel_img = pygame.image.load(path.join(ico_dir, 'panel.png')).convert_alpha()

# button images
heal_img = pygame.image.load(path.join(ico_dir, 'heal.png')).convert()

# restart image
restart_img = pygame.image.load(path.join(ico_dir, 'restart.png')).convert_alpha()

# victory and defeat images
victory_img = pygame.image.load(path.join(ico_dir, 'victory.png')).convert_alpha()
defeat_img = pygame.image.load(path.join(ico_dir, 'defeat.png')).convert_alpha()

# hand image
hand_img = pygame.image.load(path.join(ico_dir, 'hand.png')).convert_alpha()

# sword image
sword_img = pygame.image.load(path.join(ico_dir, 'sword.png')).convert_alpha()

# idle image
idle_img = pygame.image.load(path.join(ico_dir, 'idle.png')).convert_alpha()

# heal animation
heal_animation = []
heal_eff_dir = path.join(effect_dir, 'heal')
img_sheet = listdir(heal_eff_dir)
img_sheet.sort(key=lambda x: int(x.split('.')[0]))
for img in img_sheet:
    img = pygame.image.load(path.join(heal_eff_dir, f'{img}')).convert_alpha()
    img = pygame.transform.scale(img, (img.get_width() * 1.5, img.get_height() * 1.5))
    heal_animation.append(img)
