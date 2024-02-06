import pygame
import random

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("whatisgame")
icon = pygame.image.load('images/211668.png').convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load('images/5f8.png').convert_alpha()

walk_left = [
pygame.image.load('images/left/2c41_800_09.png').convert_alpha(),
pygame.image.load('images/left/2c41_800_10.png').convert_alpha(),
pygame.image.load('images/left/2c41_800_11.png').convert_alpha(),
pygame.image.load('images/left/2c41_800_12.png').convert_alpha()
]

walk_right = [
pygame.image.load('images/right/2c41_800_13.png').convert_alpha(),
pygame.image.load('images/right/2c41_800_14.png').convert_alpha(),
pygame.image.load('images/right/2c41_800_15.png').convert_alpha(),
pygame.image.load('images/right/2c41_800_16.png').convert_alpha()
]

fat = pygame.image.load('images/enemy.png').convert_alpha()
fat_list_in_time = []

trap = pygame.image.load('images/trap.png').convert_alpha()
trap_list_in_time = []

player_anim_count = 0
bg_x = 0

player_speed = 10
player_x = 150
player_y = 575

is_jump = False
jump_count = 12

bg_sound = pygame.mixer.Sound('sounds/b19.mp3')
bg_sound.play(-1)

vyistrel_sound = pygame.mixer.Sound("sounds/vyistrel-pistoleta.mp3")
no_vyistrel_sound = pygame.mixer.Sound("sounds/no-vyistrel.mp3")

fat_timer = pygame.USEREVENT+1
pygame.time.set_timer(fat_timer,5000)

trap_timer = pygame.USEREVENT+3
pygame.time.set_timer(trap_timer,9000)

bul_timer = pygame.USEREVENT
pygame.time.set_timer(bul_timer, 13000)

label = pygame.font.Font('fonts/Akrobat-Bold.otf',40)
lose_label = label.render('Вы проиграли!', False, "White")
restart_label = label.render('Играть заново', False, "White")
restart_label_rect = restart_label.get_rect(topleft=(180,200))

bullets_left = 5
bullet = pygame.image.load('images/bullet.png').convert_alpha()
bullets = []

new_bullets_left = 3
new_bullet = pygame.image.load('images/new_bul.png').convert_alpha()
new_bul_list = []

gameplay = True

running = True
while running:

    screen.blit(bg,(bg_x,0))
    screen.blit(bg, (bg_x+1280, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x,player_y))

        if fat_list_in_time:
            for (i, el) in enumerate(fat_list_in_time):
                screen.blit(fat, el)
                el.x -= 10

                if el.x < -10:
                    fat_list_in_time.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False


        if trap_list_in_time:
            for (i, el) in enumerate(trap_list_in_time):
                screen.blit(trap, el)
                el.x -= 10

                if el.x < -10:
                    trap_list_in_time.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        if new_bul_list:
            for (i, el) in enumerate(new_bul_list):
                screen.blit(new_bullet, el)
                el.x -= 10

                if el.x < -10:
                    new_bul_list.pop(i)

                if player_rect.colliderect(el):
                    new_bul_list.pop(i)
                    bullets_left = new_bullets_left


        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count],(player_x,player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))


        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_x>50:
            player_x -= player_speed


        elif keys[pygame.K_RIGHT] and player_x<1200:
            player_x += player_speed



        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -12:
                if jump_count > 0:
                    player_y -= (jump_count ** 2)/2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 12

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -1280:
            bg_x = 0


        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4
                if el.x > 1300:
                    bullets.pop(i)

                if fat_list_in_time:
                    for (index, fat_el) in enumerate(fat_list_in_time):
                        if el.colliderect(fat_el):
                            fat_list_in_time.pop(index)
                            bullets.pop(i)

    else:
        screen.fill(('red'))
        screen.blit(lose_label,(180,100))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            fat_list_in_time.clear()
            trap_list_in_time.clear()
            bullets.clear()
            bullets_left = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == fat_timer:
            fat_list_in_time.append(fat.get_rect(topleft=(1280,550)))
        if event.type == trap_timer:
            trap_list_in_time.append(trap.get_rect(topleft=(1280,625)))
        if event.type == bul_timer:
            new_bul_list.append(new_bullet.get_rect(topleft=(1280,random.randint(100,600))))

        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left>0:
            bullets.append(bullet.get_rect(topleft=(player_x+120,player_y+80)))
            vyistrel_sound.play()
            bullets_left -= 1
        elif gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left==0:
            no_vyistrel_sound.play()
    clock.tick(10)