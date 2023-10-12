from random import choice, randint

import pygame

from button import Button
from images import *
from settings import *
from sounds import *

# define fonts
FONT = pygame.font.SysFont('Times New Roman', 22)
DMG_FONT = pygame.font.SysFont('Times New Roman', 36, bold=True)

# define characters stats
HEROES = {
    'warrior': {
        'max_hp': 40,
        'strength': 12,
        'potions': 1,
        'zoom': 3.3,
        'death_snd': warrior_death_snd,
        'potion_effect': 30,
        'attack_type': 'physic'
    },
    'knight': {
        'max_hp': 55,
        'strength': 9,
        'potions': 2,
        'zoom': 2.9,
        'death_snd': knight_death_snd,
        'potion_effect': 30,
        'attack_type': 'physic'
    },
    'witch': {
        'max_hp': 35,
        'strength': 9,
        'potions': 3,
        'zoom': 2,
        'death_snd': witch_death_snd,
        'potion_effect': 35,
        'attack_type': 'magic'
    }
}

# define enemies stats
ENEMIES = {
    'bandit': {
        'max_hp': 20,
        'strength': 5,
        'potions': 1,
        'zoom': 3,
        'death_snd': human_death_snd,
        'potion_effect': 20,
        'attack_type': 'physic'
    },
    'mercenary': {
        'max_hp': 35,
        'strength': 6,
        'potions': 1,
        'zoom': 3,
        'death_snd': human_death_snd,
        'potion_effect': 25,
        'attack_type': 'physic'
    },
    'skeleton': {
        'max_hp': 30,
        'strength': 7,
        'potions': 1,
        'zoom': 3,
        'death_snd': skeleton_death_snd,
        'potion_effect': 15,
        'attack_type': 'physic'
    },
    'fly-eye': {
        'max_hp': 15,
        'strength': 4,
        'potions': 1,
        'zoom': 2,
        'death_snd': fly_death_snd,
        'potion_effect': 15,
        'attack_type': 'physic'
    },
    'fire-worm': {
        'max_hp': 40,
        'strength': 8,
        'potions': 1,
        'zoom': 2.5,
        'death_snd': worm_death_snd,
        'potion_effect': 15,
        'attack_type': 'magic'
    },
}


# create function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# drawing background
def draw_bg(bg_img):
    screen.blit(bg_img, (0, 0))


# drawing panel
def draw_panel(panel_img, player_list, enemy_list):
    # draw panel rectangle
    screen.blit(panel_img, (0, screen_height - bottom_panel))

    # show heroes stats
    for count, i in enumerate(player_list):
        draw_text(f'{i.name} {i.hp}/{i.max_hp}', FONT, gold, 130,
                  (screen_height - bottom_panel + 10) + count * 40)

    for count, i in enumerate(enemy_list):
        # show name and health
        draw_text(f'{i.name} {i.hp}/{i.max_hp}', FONT, gold, 520,
                  (screen_height - bottom_panel + 10) + count * 40)


# load random background image
def select_background(bg_dir):
    selected_bg = choice(listdir(bg_dir))
    bg_img = pygame.image.load(path.join(bg_dir, f'{selected_bg}')).convert_alpha()
    bg_img = pygame.transform.scale(bg_img, (800, 450))
    return bg_img


def create_hero(hero_coord, heroes_list):
    x_cor = hero_coord[0]
    y_cor = hero_coord[1]
    name = choice(heroes_list)
    hero = HEROES[name]
    return Fighter(
        x_cor,
        y_cor,
        hero_dir,
        name,
        hero['max_hp'],
        hero['strength'],
        hero['potions'],
        hero['zoom'],
        hero['death_snd'],
        hero['potion_effect'],
        hero['attack_type']
    )


def create_enemy(enemy_coord, enemy_dir):
    name = choice(listdir(enemy_dir))
    enemy = ENEMIES[name]
    return Fighter(
        enemy_coord[0],
        enemy_coord[1],
        enemy_dir,
        name,
        enemy['max_hp'],
        enemy['strength'],
        enemy['potions'],
        enemy['zoom'],
        enemy['death_snd'],
        enemy['potion_effect'],
        enemy['attack_type']
    )


# fighter class
class Fighter:
    def __init__(self, x, y, img_dir, name, max_hp, strength, potions, zoom, death_snd, potion_effect, attack_type):
        self.name = name
        self.dir = img_dir
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.potion_effect = potion_effect
        self.zoom = zoom
        self.alive = True
        self.attacking = False
        self.attacked = False
        self.at_type = attack_type
        self.dmg_received = 0
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:attack, 2:hurt, 3:death, 4:react
        self.death_snd = death_snd
        self.update_time = pygame.time.get_ticks()

        # load all images for the players
        animation_types = ['idle', 'attack', 'hurt', 'death', 'react']
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            action_dir = path.join(path.dirname(__file__), 'img', self.dir, f'{self.name}', f'{animation}')

            # count and sort files in the folder
            img_sheet = listdir(action_dir)
            img_sheet.sort(key=lambda x: int(x.split('.')[0]))
            for img in img_sheet:
                img = pygame.image.load(path.join(action_dir, f'{img}'))
                img = pygame.transform.scale(img, (img.get_width() * self.zoom, img.get_height() * self.zoom))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cd = 90
        attacked_cd = 75

        # handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]

        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cd:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()
                self.attacking = False

        if self.action == 1 and self.animation_list[1][len(self.animation_list[1]) // 2 + 2] and not self.attacking:
            if self.at_type == 'physic':
                choice(sword_snd).play()
            elif self.at_type == 'magic':
                choice(magic_snd).play()
            self.attacking = True

        # deal damage
        if self.attacked:
            if pygame.time.get_ticks() - self.update_time > attacked_cd:
                self.hp -= self.dmg_received
                hit_snd.play()

                # check if target has died
                if self.hp < 1:
                    self.hp = 0
                    self.alive = False
                    self.death()
                    self.attacked = False
                    self.death_snd.play()
                    damage_text = DamageText(self.rect.centerx, self.rect.y, f'-{self.dmg_received}', red)
                    damage_text_group.add(damage_text)
                else:
                    # run target hurt animation
                    self.hurt()
                    self.attacked = False
                    damage_text = DamageText(self.rect.centerx, self.rect.y, f'-{self.dmg_received}', red)
                    damage_text_group.add(damage_text)

    def idle(self):
        # set variables to attack animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # calculate damage to enemy
        rand = randint(-3, 3)
        target.attacked = True
        target.dmg_received = self.strength + rand

        # set variables to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        # set variables to hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        # set variables to death animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def healing(self):
        # set variables to react animation
        self.action = 4
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # check if the potion would heal the player beyond max health
        if self.max_hp - self.hp > self.potion_effect:
            heal_amount = self.potion_effect
        else:
            heal_amount = self.max_hp - self.hp
        self.hp += heal_amount
        self.potions -= 1
        damage_text = DamageText(self.rect.centerx, self.rect.y, f'+{heal_amount}', green)
        damage_text_group.add(damage_text)
        healing_eff = HealEffect(self.rect.centerx, self.rect.bottom)
        heal_effects_group.add(healing_eff)

    def draw(self):
        screen.blit(self.image, self.rect)


class HealthBar:
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        # update with new health
        self.hp = hp

        # calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 10))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 10))


class DamageText(pygame.sprite.Sprite):

    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = DMG_FONT.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # move damage text up
        self.rect.y -= 0.5

        # delete text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()


class HealEffect(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = heal_animation
        self.frame_rate = 40
        self.frame = 0
        self.image = self.animation_list[self.frame]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.update_time = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.update_time > self.frame_rate:
            self.update_time = now
            self.frame += 1
            if self.frame == len(self.animation_list):
                self.kill()
            else:
                self.image = self.animation_list[self.frame]


if __name__ == '__main__':
    # hide mouse
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()
    fps = 60

    # define game variables
    current_fighter = 1
    total_fighters = 5
    action_cooldown = 0
    action_wait_time = 90
    attack = False
    potion = False
    clicked = False
    game_over = 0
    change_bgm = True
    hero_xy = [250, 170]
    hero2_xy = [180, 310]
    enemy_xy = [500, 170]
    enemy2_xy = [450, 310]
    enemy3_xy = [630, 290]

    # define background image
    bg_img = select_background(bg_dir)

    damage_text_group = pygame.sprite.Group()
    heal_effects_group = pygame.sprite.Group()

    heroes_list = listdir(hero_dir)
    player1 = create_hero(hero_xy, heroes_list)
    heroes_list.remove(player1.name)
    player2 = create_hero(hero2_xy, heroes_list)
    player_list = [player1, player2]

    enemy1 = create_enemy(enemy_xy, enemy_dir)
    enemy2 = create_enemy(enemy2_xy, enemy_dir)
    enemy3 = create_enemy(enemy3_xy, enemy_dir)
    enemy_list = [enemy1, enemy2, enemy3]

    player1_health_bar = HealthBar(130, screen_height - bottom_panel + 40, player1.hp, player1.max_hp)
    player2_health_bar = HealthBar(130, screen_height - bottom_panel + 80, player2.hp, player2.max_hp)
    enemy1_health_bar = HealthBar(520, screen_height - bottom_panel + 40, enemy1.hp, enemy1.max_hp)
    enemy2_health_bar = HealthBar(520, screen_height - bottom_panel + 80, enemy2.hp, enemy2.max_hp)
    enemy3_health_bar = HealthBar(520, screen_height - bottom_panel + 120, enemy3.hp, enemy3.max_hp)

    # create buttons
    heal_button1 = Button(screen, 300, screen_height - bottom_panel + 30, heal_img, 64, 64)
    heal_button2 = Button(screen, 300, screen_height - bottom_panel + 30, heal_img, 64, 64)
    restart_button = Button(screen, 350, 120, restart_img, 120, 30)

    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1, fade_ms=8000)

    run = True
    while run:
        clock.tick(fps)

        # draw background
        draw_bg(bg_img)

        # draw panel
        draw_panel(panel_img, player_list, enemy_list)
        player1_health_bar.draw(player1.hp)
        player2_health_bar.draw(player2.hp)
        enemy1_health_bar.draw(enemy1.hp)
        enemy2_health_bar.draw(enemy2.hp)
        enemy3_health_bar.draw(enemy3.hp)

        # draw heroes
        for player in player_list:
            player.update()
            player.draw()

        # draw enemies
        for enemy in enemy_list:
            enemy.update()
            enemy.draw()

        # draw damage text
        damage_text_group.update()
        damage_text_group.draw(screen)

        # draw heal effects
        heal_effects_group.update()
        heal_effects_group.draw(screen)

        # control player actions
        # reset action variables
        attack = False
        potion = False
        target = None

        # draw heal button for current hero
        if current_fighter == 1:
            if heal_button1.draw():
                potion = True
        elif current_fighter == 2:
            if heal_button2.draw():
                potion = True

        # show number of potions remaining
        if current_fighter == 1:
            draw_text(str(player1.potions), FONT, gold, 350, screen_height - bottom_panel + 30)
        elif current_fighter == 2:
            draw_text(str(player2.potions), FONT, gold, 350, screen_height - bottom_panel + 30)

        # draw which fighter turn
        if current_fighter == 1 and player1.alive:
            draw_text(player1.name, DMG_FONT, green, 350, 390)
        elif current_fighter == 2 and player2.alive:
            draw_text(player2.name, DMG_FONT, green, 350, 390)
        elif current_fighter == 3 and enemy1.alive:
            draw_text(enemy1.name, DMG_FONT, green, 350, 390)
        elif current_fighter == 4 and enemy2.alive:
            draw_text(enemy2.name, DMG_FONT, green, 350, 390)
        elif current_fighter == 5 and enemy3.alive:
            draw_text(enemy3.name, DMG_FONT, green, 350, 390)

        # pick target
        pos = pygame.mouse.get_pos()
        for num, player in enumerate(player_list):
            if current_fighter == 1 + num:
                for count, enemy in enumerate(enemy_list):
                    if enemy.rect.collidepoint(pos):
                        if clicked and enemy.alive:
                            attack = True
                            target = enemy_list[count]

        if game_over == 0:
            # heroes action
            for count, player in enumerate(player_list):
                if current_fighter == 1 + count:
                    if player.alive:
                        action_cooldown += 1
                        if action_cooldown >= action_wait_time:
                            # look for player action
                            # attack
                            if attack:
                                player.attack(target)
                                current_fighter += 1
                                action_cooldown = 0
                            # potion
                            if potion and player.potions > 0 and player.hp != player.max_hp:
                                # check if the potion would heal the player beyond max health
                                player.healing()
                                heal_snd.play()
                                current_fighter += 1
                                action_cooldown = 0
                    else:
                        current_fighter += 1

            # enemy action
            for count, enemy in enumerate(enemy_list):
                if current_fighter == 3 + count:
                    if enemy.alive:
                        action_cooldown += 1
                        if action_cooldown >= action_wait_time:
                            # check if bandit needs to heal first
                            if (enemy.hp / enemy.max_hp) < 0.5 and enemy.potions > 0:
                                enemy.healing()
                                heal_snd.play()
                                current_fighter += 1
                                action_cooldown = 0
                            # attack
                            else:
                                targets = [player for player in player_list if player.alive]
                                enemy.attack(choice(targets))
                                current_fighter += 1
                                action_cooldown = 0
                    else:
                        current_fighter += 1

            # if all fighters have had a turn then reset
            if current_fighter > total_fighters:
                current_fighter = 1

        # check if all heroes are dead
        alive_heroes = 0
        for player in player_list:
            if player.alive:
                alive_heroes += 1
        if alive_heroes == 0:
            game_over = -1

        # check if all bandits are dead
        alive_enemies = 0
        for enemy in enemy_list:
            if enemy.alive:
                alive_enemies += 1
        if alive_enemies == 0:
            game_over = 1

        # check if game over
        if game_over != 0:
            if game_over == 1:
                screen.blit(victory_img, (270, 50))
                # change music
                if change_bgm:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(path.join(snd_dir, 'victory.wav'))
                    pygame.mixer.music.set_volume(0.4)
                    pygame.mixer.music.play(fade_ms=2000)
                    change_bgm = False
            if game_over == -1:
                screen.blit(defeat_img, (290, 50))
                # change music
                if change_bgm:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(path.join(snd_dir, 'defeat.mp3'))
                    pygame.mixer.music.set_volume(0.4)
                    pygame.mixer.music.play(fade_ms=2000)
                    change_bgm = False
            if restart_button.draw():
                # change background image
                bg_img = select_background(bg_dir)

                # reset fighters
                heroes_list = listdir(hero_dir)
                player1 = create_hero(hero_xy, heroes_list)
                heroes_list.remove(player1.name)
                player2 = create_hero(hero2_xy, heroes_list)
                player_list = [player1, player2]
                enemy1 = create_enemy(enemy_xy, enemy_dir)
                enemy2 = create_enemy(enemy2_xy, enemy_dir)
                enemy3 = create_enemy(enemy3_xy, enemy_dir)
                enemy_list = [enemy1, enemy2, enemy3]
                player1_health_bar = HealthBar(130, screen_height - bottom_panel + 40, player1.hp, player1.max_hp)
                player2_health_bar = HealthBar(130, screen_height - bottom_panel + 80, player2.hp, player2.max_hp)
                enemy1_health_bar = HealthBar(520, screen_height - bottom_panel + 40, enemy1.hp, enemy1.max_hp)
                enemy2_health_bar = HealthBar(520, screen_height - bottom_panel + 80, enemy2.hp, enemy2.max_hp)
                enemy3_health_bar = HealthBar(520, screen_height - bottom_panel + 120, enemy3.hp, enemy3.max_hp)
                current_fighter = 1
                action_cooldown = 0
                game_over = 0

                # change music
                change_bgm = True
                pygame.mixer.music.stop()
                pygame.mixer.music.load(path.join(snd_dir, 'battle.wav'))
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1, fade_ms=8000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            else:
                clicked = False

        # show mouse cursor
        if current_fighter == 1 and action_cooldown >= action_wait_time:
            if enemy1.rect.collidepoint(pos) and enemy1.alive:
                screen.blit(sword_img, pos)
            elif enemy2.rect.collidepoint(pos) and enemy2.alive:
                screen.blit(sword_img, pos)
            elif enemy3.rect.collidepoint(pos) and enemy3.alive:
                screen.blit(sword_img, pos)
            else:
                screen.blit(hand_img, pos)
        elif current_fighter == 2 and action_cooldown >= action_wait_time:
            if enemy1.rect.collidepoint(pos) and enemy1.alive:
                screen.blit(sword_img, pos)
            elif enemy2.rect.collidepoint(pos) and enemy2.alive:
                screen.blit(sword_img, pos)
            elif enemy3.rect.collidepoint(pos) and enemy3.alive:
                screen.blit(sword_img, pos)
            else:
                screen.blit(hand_img, pos)
        elif game_over != 0:
            screen.blit(hand_img, pos)
        else:
            screen.blit(idle_img, pos)

        pygame.display.flip()

    pygame.quit()
