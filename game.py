import pygame, sys
from pygame.locals import *
from pygame import mixer

mixer.init()

pygame.init()

global greenhouse_effect
greenhouse_effect = 50

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)

    return hit_list

def collisions_testing(player_rect, obj_list, greenhouse_effect):
    counter = -1
    obj_list_copy = obj_list[:]
    for i in range(len(obj_list_copy)-1):
        counter += 1
        if player_rect.colliderect(obj_list[i][0]):
            del obj_list[i]
            greenhouse_effect -= 5
            collect.set_volume(0.3)
            collect.play()

    return greenhouse_effect

def move(rect, movement, tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

def show_health(health):
    font = pygame.font.Font("freesansbold.ttf", 15)
    colour = "darkgreen"
    if health < 50:
        colour = "darkgreen"
    if health > 50 and health < 76:
        colour = "orange"
    if health > 75:
        colour = "red"
    scoreSurf = font.render("Greenhouse Effect: %s percent"%(health),True,colour)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (10,10)
    display.blit(scoreSurf,scoreRect)

def showVictoryScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('YOU', True, "purple")
    overSurf = gameOverFont.render('WON!', True, "red")
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (700 / 2, 370 / 2 - 150)
    overRect.midtop = (700 / 2, 370 / 2)

    screen.blit(gameSurf, gameRect)
    screen.blit(overSurf, overRect)

    win_sound.play()

    pygame.display.update()
    pygame.time.wait(5000)

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, "purple")
    overSurf = gameOverFont.render('Over', True, "red")
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (700 / 2, 370 / 2 - 150)
    overRect.midtop = (700 / 2, 370 / 2)

    screen.blit(gameSurf, gameRect)
    screen.blit(overSurf, overRect)

    death_sound.play()

    pygame.display.update()
    pygame.time.wait(5000)
    


WINDOW_SIZE = [700, 370]

global clock
clock = pygame.time.Clock()

air_timer = 0

timer = 50
greenhouse_counter = 0

screen = pygame.display.set_mode(WINDOW_SIZE)
global display
display = pygame.Surface((350, 185))

run = True

player_gravity = 0

true_scroll = [0,0]

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]],[0.25,[420,50,120,200]],[0.5,[500,50,50,400]]]

moving_right = False
moving_left = False

grass_img = pygame.image.load("images/grass.png")
grass_img = pygame.transform.scale(grass_img, (10,10))

dirt_img = pygame.image.load("images/dirt.png")
dirt_img = pygame.transform.scale(dirt_img, (10,10))

player_flip = False

global death_sound, win_sound, collect
death_sound = pygame.mixer.Sound("gameover.wav")
win_sound = pygame.mixer.Sound("victory.wav")
collect = pygame.mixer.Sound("score.wav")

game_map = [[0,0,0,0,0,0,0,0,0,0,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,50,0,0,0,0,0,0,0,0,0,0,40,1,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,40,0,50,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,30,2,2,1,1,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0],
            [0,0,0,0,0,0,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,20,0,0,40,0,0,0,0,0,0,20,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,1,1,1,0,0,0,0],
            [0,0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,0,0,0,2,1,1,1,1,1,1,1,1,2,2,2,2],
            [60,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,30,0,0,0,0,0,0,0,50,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [2,2,0,0,0,0,0,0,30,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,2,0,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,0,0,0,0,2,2,1,1,2,2,0,0,40,0,0,0,2,2,2,1,2,2,0,0,0,0,0,0,10,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,20,0,1,1,1,1,1,0,0,0,0,0,0,2,1,1,1,1,1,1,0,0,0,0,0,2,2,2,0,2,2,2,2,2,2,2,2,2,2,1,1,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0,2,2,2,2,1,1,1,1,1,1,1,0,60,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,2,2,2,2],
            [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,1,60,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0],
            [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0]]

frame_number = 0
animated_num = 1
animation_type = "run"

player_img = pygame.image.load('images/RUN_1.png')
player_img = pygame.transform.scale(player_img, (12, 17))
player_rect = pygame.Rect(0, 0, player_img.get_width(), player_img.get_height())

obj_list = []
y = 0
for row in game_map:
    x = 0
    for tile in row:
        if tile == 10:
            image = pygame.image.load("trash_images/t1.png")
            image.set_colorkey((255,255,255))
            image = pygame.transform.scale(image, (15,15))
            image_rect = pygame.Rect(x * 15, y * 10, 15, 15)
            obj_list.append([image_rect, image, [x * 15, y * 10, 15, 15], "t1"])
        if tile == 20:
            image = pygame.image.load("trash_images/t2.png")
            image.set_colorkey((255,255,255))
            image = pygame.transform.scale(image, (15,15))
            image_rect = pygame.Rect(x * 15, y * 10, 15, 15)
            obj_list.append([image_rect, image, [x * 15, y * 10, 15, 15], "t2"])
        if tile == 30:
            image = pygame.image.load("trash_images/t3.png")
            image.set_colorkey((255,255,255))
            image = pygame.transform.scale(image, (15,15))
            image_rect = pygame.Rect(x * 15, y * 10, 15, 15)
            obj_list.append([image_rect, image, [x * 15, y * 10, 15, 15], "t3"])
        if tile == 40 or tile == 50:
            image = pygame.image.load("trash_images/t4.png")
            image.set_colorkey((255,255,255))
            image = pygame.transform.scale(image, (15,15))
            image_rect = pygame.Rect(x * 15, y * 10, 15, 15)
            obj_list.append([image_rect, image, [x * 15, y * 10, 15, 15], "t4"])
        if tile == 60:
            image = pygame.image.load("trash_images/t1.png")
            image.set_colorkey((255,255,255))
            image = pygame.transform.scale(image, (15,15))
            image_rect = pygame.Rect(x * 15, y * 10, 15, 15)
            obj_list.append([image_rect, image, [x * 15, y * 10, 15, 15], "t1"])
        x += 1
    y += 1

time_remaining = 30
timer = pygame.USEREVENT
pygame.time.set_timer(timer, 3000)

win = False
game_over = False

def start_screen():
    run = True
    pygame.mixer.music.load("home_screen_bg.mp3")
    pygame.mixer.music.play(-1)
    show_controls = False
    count = 0
    while run:

        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False
            if event.type ==QUIT:
                run = False
            if event.type == MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if x >= 250 and x <= 450:
                    if y >= (370 / 2 + 120 - 75/2) and y <= (370 / 2 + 120 + 75/2):
                        run = False
                if x >= 0 and x <= 150:
                    if y >= 50 and y <= 125:
                        if count == 1:
                            count = 0
                            show_controls = False
                        elif count == 0:
                            count = 1
                            show_controls = True

        screen.fill("black")
        intro_1 = "You are a Climate Warrior who has to collect as many"
        intro_2 = "items in order to bring down the Greenhouse Effect to zero."
        intro_3 = "The greenhouse effect is ever-increasing due to"
        intro_4 = "incessant land pollution by humans."

    
        titleFont = pygame.font.Font("freesansbold.ttf",80)
        title = titleFont.render("CLIMATE", True, "white")
        title1 = titleFont.render("WARRIOR", True, "white")
        title_rect = title.get_rect()
        title_rect1 = title1.get_rect()
        title_rect.center = (700/2, 370 / 2 - 120)
        title_rect1.center = (700/2, 370 / 2 - 45)

        titleFont = pygame.font.Font("freesansbold.ttf", 40)
        play = titleFont.render("PLAY", True, "white")
        titleFont = pygame.font.Font("freesansbold.ttf", 25)
        c = titleFont.render("Controls", True, "white")

        titleFont = pygame.font.Font("freesansbold.ttf",17)
        titleSurf1 = titleFont.render(intro_1, True, "yellow")
        titleSurf2 = titleFont.render(intro_2, True, "yellow")
        titleSurf3 = titleFont.render(intro_3, True, "yellow")
        titleSurf4 = titleFont.render(intro_4, True, "yellow")
        
        controls1 = titleFont.render("W/Space-bar to Jump", True, "green")
        controls2 = titleFont.render("A to Run Left", True, "green")
        controls3 = titleFont.render("D to Run Right", True, "green")
        Rect1 = titleSurf1.get_rect()
        Rect2 = titleSurf2.get_rect()
        Rect3 = titleSurf3.get_rect()
        Rect4 = titleSurf4.get_rect()
        play_rect = play.get_rect()
        c_rect = c.get_rect()
        
        control_rect1 = controls1.get_rect()
        control_rect2 = controls2.get_rect()
        control_rect3 = controls3.get_rect()
        Rect1.center = (700 / 2, 370 / 2 +20)
        Rect2.center = (700 / 2, 370 / 2 +40)
        Rect3.center = (700 / 2, 370 / 2 + 60)
        Rect4.center = (700 / 2, 370 / 2 + 80)
        play_rect.center = (700 / 2, 370 / 2 +135)

        button = pygame.Rect(700 / 2, 370 / 2 + 120, 200, 75)
        button.center = (700 / 2, 370 / 2 + 135)
        button2 = pygame.Rect(700 / 2, 370 / 2 + 120, 175, 50)
        button2.center = (700 / 2, 370 / 2 + 135)

        button3 = pygame.Rect(700 / 2, 370 / 2 + 120, 150, 75)
        button3.center = (75, 50)
        button4 = pygame.Rect(700 / 2, 370 / 2 + 120, 125, 50)
        button4.center = (75, 50)
        c_rect.center = (75, 50)

        control_rect1.topleft = (10, 370 / 2 + 100)
        control_rect2.topleft = (10, 370 / 2 + 120)
        control_rect3.topleft = (10, 370 / 2 + 140)
        screen.blit(title, title_rect)
        screen.blit(title1, title_rect1)
        screen.blit(titleSurf1, Rect1)
        screen.blit(titleSurf2, Rect2)
        screen.blit(titleSurf3, Rect3)
        screen.blit(titleSurf4, Rect4)

        if show_controls == True:
            screen.blit(controls1, control_rect1)
            screen.blit(controls2, control_rect2)
            screen.blit(controls3, control_rect3)

        pygame.draw.rect(screen, (20, 61, 89), button)
        pygame.draw.rect(screen, (255, 186, 68), button2)
        screen.blit(play, play_rect)

        pygame.draw.rect(screen, (20, 61, 89), button3)
        pygame.draw.rect(screen, (255, 186, 68), button4)
        screen.blit(c, c_rect)
        
        pygame.display.update()
    
    clock.tick(60)
    
    pygame.mixer.music.fadeout(200)
        

start_screen()

pygame.mixer.music.load("game_bg.wav")
pygame.mixer.music.play(-1)

while run:
    if greenhouse_effect <= 0:
        win = True
    if greenhouse_effect >= 100 or player_rect.y > 150:
        game_over = True
    
    if game_over == True:
        pygame.mixer.music.fadeout(500)
        showGameOverScreen()
        pygame.quit()
    if win == True:
        pygame.mixer.music.fadeout(500)
        showVictoryScreen()
        pygame.quit()

    frame_number += 1
    if frame_number == 5:
        animated_num += 1
        player_img = pygame.image.load('images/RUN_' + str(animated_num) + '.png')
        if animated_num == 2 or animated_num == 5:
            player_img = pygame.transform.scale(player_img, (8,17))
        else:
            player_img = pygame.transform.scale(player_img, (12,17))
        player_rect = pygame.Rect(player_rect.x, player_rect.y, player_img.get_width(), player_img.get_height())
        frame_number = 0
    if animated_num == 6:
        animated_num = 0
    
    display.fill((146, 244, 255))
    
    tile_Rects = []

    true_scroll[0] += (player_rect.x - true_scroll[0] - 150) / 20
    true_scroll[1] += (player_rect.y - true_scroll[1] - 92) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(true_scroll[0])
    scroll[1] = int(true_scroll[1])

    pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,500,80))
    for bg_obj in background_objects:
        obj_rect = pygame.Rect(bg_obj[1][0] - scroll[0] * bg_obj[0], bg_obj[1][1] - scroll[1] * bg_obj[0], bg_obj[1][2], bg_obj[1][3])
        if bg_obj[0] == 0.5:
            pygame.draw.rect(display, (14, 222, 150), obj_rect)
        else:
            pygame.draw.rect(display, (2, 54, 2), obj_rect)
    
    show_health(greenhouse_effect)
        
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == 1:
                display.blit(dirt_img, (x * 10 - scroll[0], y * 10 - scroll[1]))
            if tile == 2:
                display.blit(grass_img, (x * 10 - scroll[0], y * 10 - scroll[1]))
            if tile == 10:
                image = pygame.image.load("trash_images/t1.png")
                image.set_colorkey((255,255,255))
                image = pygame.transform.scale(image, (15,15))
                image_rect = image.get_rect()
            if tile == 20:
                image = pygame.image.load("trash_images/t2.png")
                image.set_colorkey((255,255,255))
                image = pygame.transform.scale(image, (15,15))
                image_rect = image.get_rect()
            if tile == 30:
                image = pygame.image.load("trash_images/t3.png")
                image.set_colorkey((255,255,255))
                image = pygame.transform.scale(image, (15,15))
                image_rect = image.get_rect()
            if tile == 40 or tile == 50:
                image = pygame.image.load("trash_images/t4.png")
                image.set_colorkey((255,255,255))
                image = pygame.transform.scale(image, (15,15))
                image_rect = image.get_rect()
            if tile == 60:
                image = pygame.image.load("trash_images/t1.png")
                image.set_colorkey((255,255,255))
                image = pygame.transform.scale(image, (15,15))
                image_rect = image.get_rect()
            if tile == 1 or tile == 2:
                tile_Rects.append(pygame.Rect(x * 10, y * 10, 10, 10))
            x += 1
        y += 1

    for obj in obj_list:
        display.blit(obj[1], (obj[2][0] - scroll[0], obj[2][1] - scroll[1]))
    
    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += 2
        player_flip = False
    if moving_left == True:
        player_movement[0] -= 2
        player_flip = True
    player_movement[1] += player_gravity
    player_gravity += 0.2
    if player_gravity > 3:
        player_gravity = 3
    
    player_rect, collisions = move(player_rect, player_movement, tile_Rects)

    greenhouse_effect = collisions_testing(player_rect, obj_list, greenhouse_effect)
    
    if collisions['bottom'] == True:
        player_gravity = 0
        air_timer = 0
    else:
        air_timer += 1
    
    if moving_left == False and moving_right == False:
        player_img = pygame.image.load('images/idle_player.png')
        player_img = pygame.transform.scale(player_img, (9, 18))
        player_rect = pygame.Rect(player_rect.x, player_rect.y, player_img.get_width(), player_img.get_height())
        display.blit(pygame.transform.flip(player_img, player_flip, False), (player_rect.x - true_scroll[0], player_rect.y - true_scroll[1]))
    else:
        display.blit(pygame.transform.flip(player_img, player_flip, False), (player_rect.x - true_scroll[0], player_rect.y - true_scroll[1]))
    
    
    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == timer:
            greenhouse_effect += 4
        if event.type == KEYDOWN:
            if event.key == K_d:
                moving_right = True
                animation_type = "run"
            if event.key == K_a:
                moving_left = True
                animation_type = "run"
            if event.key == K_w or event.key == K_SPACE:
                if air_timer < 6:
                    player_gravity = -5
        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False
    
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    
    pygame.display.update()
    
    clock.tick(60)
