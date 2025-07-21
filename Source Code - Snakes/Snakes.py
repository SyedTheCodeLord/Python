import pygame
import random
import os
import sys
pygame.init()
pygame.mixer.init()
white = (255, 255, 255)
red = (255, 0, 0)
cyan = (0, 255, 255)
pink = (230, 204, 220)
green = (0, 255, 0)
screen_width = 900
screen_height = 600
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snakes")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

bg_img = pygame.image.load(resource_path("Snake.png"))
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height)).convert_alpha()
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)
def screen_text(text, color, x, y):
    screen_text = font.render(text, True, color)
    window.blit(screen_text, [x, y])
def plot_snake(window, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(window, color, [x, y, snake_size, snake_size])
def welcome():
    fps = 60
    exit_game = False
    while not exit_game:
        window.fill(pink)
        screen_text("Welcome to Snakes!", green, screen_width/3, (screen_height/2)- 40)
        screen_text("(Press Spacebar To Play.)", cyan, screen_width/3.4, (screen_height/2))
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                exit_game = True
            if (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load(resource_path("Back.mp3"))
                    pygame.mixer.music.play()
                    gameloop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
        pygame.display.update()
        clock.tick(fps)
def gameloop():
    exit_game = False
    game_over = False
    paused = False
    music_on = True
    snake_x = 100
    snake_y = 100
    snake_size = 20
    velocity_x = 0
    velocity_y = 0
    snake_list = []
    snake_length = 1
    food_x = random.randint(50, (screen_width - 50))
    food_y = random.randint(50, (screen_height - 50))
    score = 0
    init_velocity = 5
    fps = 60
    if (not os.path.exists("High Score.txt")):
        with open("High Score.txt", "w") as f:
            f.write("0")
    with open("High Score.txt", "r") as f:
        hi_score = f.read()
    while not exit_game:
        if game_over:
            with open("High Score.txt", "w") as f:
                f.write(str(hi_score))
            window.fill(white)
            screen_text("GAME OVER! (Press Enter To Continue.)", red, screen_width/5, (screen_height/2) - 20)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    exit_game = True
                if (event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    exit_game = True
                if (event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                        paused = True
                        while paused:
                            screen_text("Paused (Press Alt to Resume.)", red, screen_width / 4, screen_height / 2)
                            pygame.display.update()
                            for ev in pygame.event.get():
                                if ev.type == pygame.QUIT:
                                    pygame.quit()
                                    quit()
                                if ev.type == pygame.KEYDOWN:
                                    if ev.key == pygame.K_LALT or ev.key == pygame.K_RALT:
                                        paused = False
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_m:
                        if music_on:
                            pygame.mixer.music.pause()
                            music_on = False
                        else:
                            pygame.mixer.music.unpause()
                            music_on = True
            snake_x += velocity_x
            snake_y += velocity_y
            if (abs(snake_x - food_x) < 6) and (abs(snake_y - food_y) < 6):
                score += 10
                food_x = random.randint(50, 850)
                food_y = random.randint(50, 550)
                snake_length += 5
                if (score > int(hi_score)):
                    hi_score = score
            window.fill(white)
            window.blit(bg_img, (0, 0))
            screen_text(f"Score: {score}"+ f"    High-Score: {hi_score}", cyan, 5, 5)
            pygame.draw.rect(window, red, [food_x, food_y, snake_size, snake_size])
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)
            if len(snake_list)> snake_length:
                del(snake_list[0])
            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load(resource_path("Game Over.mp3"))
                pygame.mixer.music.play()
            if (snake_x < 0) or (snake_x > screen_width) or (snake_y < 0) or (snake_y > screen_height):
                game_over = True
                pygame.mixer.music.load(resource_path("Game Over.mp3"))
                pygame.mixer.music.play()
            plot_snake(window, green, snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)
welcome()
pygame.quit()
