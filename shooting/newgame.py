import pygame
import random
import sys

pygame.init()

# --- CONFIG ---
WIDTH, HEIGHT = 800, 600
FPS = 60
FONT = pygame.font.SysFont(None, 48)
SMALL_FONT = pygame.font.SysFont(None, 32)

# Game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Shooter")

clock = pygame.time.Clock()

# --- WORDS ---
word_list = ["apple", "dream", "python", "code", "game", "snow", "space",
             "rocket", "enemy", "keyboard", "shoot", "speed", "level", "typing"]

# --- GAME STATE ---
falling_words = []
typed_word = ""
score = 0
lives = 6
level = 1
spawn_delay = 2000  # ms
# --- CONFIG ---
BASE_SPEED = .70     # starting speed
SPEED_INCREASE = 0.01 # extra speed per level

last_spawn = pygame.time.get_ticks()

# --- FUNCTIONS ---
def spawn_word():
    word = random.choice(word_list)
    x = random.randint(50, WIDTH - 100)
    y = -50
    speed = BASE_SPEED + (level - 1) * SPEED_INCREASE
    falling_words.append({"text": word, "x": x, "y": y, "speed": speed})

def draw_game():
    screen.fill((0, 0, 0))

    # Draw falling words
    for w in falling_words:
        word_surface = FONT.render(w["text"], True, (255, 255, 255))
        screen.blit(word_surface, (w["x"], w["y"]))

    # Draw typed word
    typed_surface = FONT.render(typed_word, True, (0, 255, 0))
    screen.blit(typed_surface, (20, HEIGHT - 50))

    # Score, lives, level
    hud = SMALL_FONT.render(f"Score: {score}  Lives: {lives}  Level: {level}", True, (255, 255, 0))
    screen.blit(hud, (20, 20))

    pygame.display.flip()

def game_over():
    screen.fill((0, 0, 0))
    msg = FONT.render("GAME OVER", True, (255, 0, 0))
    score_msg = SMALL_FONT.render(f"Final Score: {score}", True, (255, 255, 255))
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 50))
    screen.blit(score_msg, (WIDTH//2 - score_msg.get_width()//2, HEIGHT//2 + 10))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# --- GAME LOOP ---
running = True
while running:
    clock.tick(FPS)

    # Check for spawn
    now = pygame.time.get_ticks()
    if now - last_spawn > spawn_delay:
        spawn_word()
        last_spawn = now

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                typed_word = typed_word[:-1]
            elif event.key == pygame.K_RETURN:
                # Check if typed word matches any falling word
                for w in falling_words:
                    if typed_word == w["text"]:
                        falling_words.remove(w)
                        score += 1
                        # Difficulty scaling
                        if score % 10 == 0:  # every 10 points → new level
                            level += 1
                            spawn_delay = max(500, spawn_delay - 200)  # faster spawns
                        break
                typed_word = ""
            else:
                typed_word += event.unicode 

                for w in falling_words:
                    if typed_word == w["text"]:
                        falling_words.remove(w)
                        score += 1
                        # Difficulty scaling
                        if score % 10 == 0:  # every 10 points → new level
                            level += 1
                            spawn_delay = max(500, spawn_delay - 200)  # faster spawns
                        typed_word = ""
                        break


    # Update falling words
    for w in falling_words[:]:
        w["y"] += w["speed"]
        if w["y"] > HEIGHT:
            falling_words.remove(w)
            lives -= 1
            if lives <= 0:
                game_over()

    draw_game()

pygame.quit()
