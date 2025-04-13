import pygame
import random
import sys

# ---------------------------
# Initialize Pygame and Globals
# ---------------------------
pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Attack Of The Gamer Boys")

# Colors
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
BG    = (30, 30, 30)

# Clock & FPS
FPS = 60

# Global setting to enable the N key to spawn a nuke powerup.
enable_nuke_key = False

# Global leaderboard (persists until the game is closed)
leaderboard = []

# ---------------------------
# Load Images and Fonts
# ---------------------------
player_img = pygame.image.load("sprites/player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (50, 50))

controller_img = pygame.image.load("sprites/contoler.png").convert_alpha()
controller_img = pygame.transform.scale(controller_img, (40, 20))

enemy_img = pygame.image.load("sprites/enemy.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (40, 40))

ps5_controller = pygame.image.load("sprites/ps5_controller.png").convert_alpha()
ps5_controller = pygame.transform.scale(ps5_controller, (48, 24))

special_controller = pygame.image.load("sprites/special_controller.png").convert_alpha()
special_controller = pygame.transform.scale(special_controller, (30, 15))  # increased to 3x

nuke_img = pygame.image.load("sprites/nuke.png").convert_alpha()
nuke_img = pygame.transform.scale(nuke_img, (20, 20))

skells_img = pygame.image.load("sprites/skells.png").convert_alpha()
skells_img = pygame.transform.scale(skells_img, (40, 40))

font = pygame.font.SysFont("Arial", 20)

# ---------------------------
# Game Classes
# ---------------------------
class FloatingText:
    def __init__(self, x, y, text, color, lifetime=60):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifetime = lifetime  # in frames
        self.counter = 0
        self.alpha = 255
        self.image = font.render(text, True, color)
        self.image.set_alpha(self.alpha)

    def update(self):
        self.counter += 1
        self.alpha = max(0, 255 - int((255 / self.lifetime) * self.counter))
        self.image.set_alpha(self.alpha)
        self.y -= 0.5  # slowly float upward

    def draw(self):
        WIN.blit(self.image, (self.x, self.y))


class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 60
        self.speed = 5
        self.powerups = {"ps5": 0, "special": 0, "nuke": 0}

    def draw(self):
        WIN.blit(player_img, (self.x, self.y))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x - self.speed > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.speed < WIDTH - 50:
            self.x += self.speed

    def get_rect(self):
        return pygame.Rect(self.x, self.y, player_img.get_width(), player_img.get_height())


class Controller:
    def __init__(self, x, y, damage, img, controller_type="normal"):
        self.x = x
        self.y = y
        self.damage = damage
        self.img = img
        self.controller_type = controller_type
        self.rect = self.img.get_rect(topleft=(x, y))

    def move(self):
        self.y -= 10
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        WIN.blit(self.img, (self.x, self.y))


class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 40)
        self.y = -40
        self.hp = 3
        self.rect = enemy_img.get_rect(topleft=(self.x, self.y))

    def move(self):
        self.y += 3
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        WIN.blit(enemy_img, (self.x, self.y))


class Skells:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 40)
        self.y = -40
        self.hp = 5  # takes 5 hits
        self.rect = skells_img.get_rect(topleft=(self.x, self.y))

    def move(self):
        self.y += 3
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        WIN.blit(skells_img, (self.x, self.y))


def spawn_powerup():
    # Regular powerup spawner: 1 in 15 chance to be a nuke; otherwise randomly ps5 or special.
    r = random.randint(1, 15)
    choice = "nuke" if r == 1 else random.choice(["ps5", "special"])
    x = random.randint(0, WIDTH - 20)
    return {"type": choice, "rect": pygame.Rect(x, 0, 20, 20)}


def draw_powerup(powerup):
    if powerup["type"] == "ps5":
        WIN.blit(ps5_controller, powerup["rect"].topleft)
    elif powerup["type"] == "special":
        WIN.blit(special_controller, powerup["rect"].topleft)
    elif powerup["type"] == "nuke":
        WIN.blit(nuke_img, powerup["rect"].topleft)


def display_leaderboard(leaderboard):
    sorted_scores = sorted(leaderboard, reverse=True)
    running = True
    restart_requested = False

    restart_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT - 150, 100, 40)
    exit_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT - 150, 100, 40)

    while running:
        WIN.fill(BG)
        title_text = font.render("Leaderboard", True, WHITE)
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        for i, score in enumerate(sorted_scores):
            entry_text = font.render(f"{i + 1}. {score}", True, WHITE)
            WIN.blit(entry_text, (WIDTH // 2 - entry_text.get_width() // 2, 100 + i * 30))

        pygame.draw.rect(WIN, WHITE, restart_button)
        restart_text = font.render("Restart", True, BG)
        WIN.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2,
                                restart_button.centery - restart_text.get_height() // 2))

        pygame.draw.rect(WIN, WHITE, exit_button)
        exit_text = font.render("Exit", True, BG)
        WIN.blit(exit_text, (exit_button.centerx - exit_text.get_width() // 2,
                             exit_button.centery - exit_text.get_height() // 2))

        instructions = font.render("Click a button", True, WHITE)
        WIN.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT - 80))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    restart_requested = True
                    running = False
                    break
                if exit_button.collidepoint(event.pos):
                    restart_requested = False
                    running = False
                    break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_requested = True
                    running = False
                    break

    return restart_requested

# ---------------------------
# Menu Functions
# ---------------------------
def main_menu():
    while True:
        WIN.fill(BG)
        title = font.render("The Attack Of The Gamer Boys", True, WHITE)
        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        start_button = pygame.Rect(WIDTH // 2 - 100, 150, 200, 50)
        settings_button = pygame.Rect(WIDTH // 2 - 100, 220, 200, 50)
        about_button = pygame.Rect(WIDTH // 2 - 100, 290, 200, 50)
        exit_button = pygame.Rect(WIDTH // 2 - 100, 360, 200, 50)

        pygame.draw.rect(WIN, WHITE, start_button)
        pygame.draw.rect(WIN, WHITE, settings_button)
        pygame.draw.rect(WIN, WHITE, about_button)
        pygame.draw.rect(WIN, WHITE, exit_button)

        txt_start = font.render("Start Game", True, BG)
        txt_settings = font.render("Settings", True, BG)
        txt_about = font.render("About", True, BG)
        txt_exit = font.render("Exit", True, BG)

        WIN.blit(txt_start, (start_button.centerx - txt_start.get_width() // 2,
                              start_button.centery - txt_start.get_height() // 2))
        WIN.blit(txt_settings, (settings_button.centerx - txt_settings.get_width() // 2,
                                 settings_button.centery - txt_settings.get_height() // 2))
        WIN.blit(txt_about, (about_button.centerx - txt_about.get_width() // 2,
                              about_button.centery - txt_about.get_height() // 2))
        WIN.blit(txt_exit, (exit_button.centerx - txt_exit.get_width() // 2,
                             exit_button.centery - txt_exit.get_height() // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return "Start Game"
                elif settings_button.collidepoint(event.pos):
                    settings_menu()
                elif about_button.collidepoint(event.pos):
                    about_menu()
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


def pause_menu():
    paused = True
    while paused:
        # Draw a translucent overlay.
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BG)
        WIN.blit(overlay, (0, 0))

        resume_button = pygame.Rect(WIDTH // 2 - 100, 150, 200, 50)
        settings_button = pygame.Rect(WIDTH // 2 - 100, 220, 200, 50)
        about_button = pygame.Rect(WIDTH // 2 - 100, 290, 200, 50)
        exit_button = pygame.Rect(WIDTH // 2 - 100, 360, 200, 50)

        pygame.draw.rect(WIN, WHITE, resume_button)
        pygame.draw.rect(WIN, WHITE, settings_button)
        pygame.draw.rect(WIN, WHITE, about_button)
        pygame.draw.rect(WIN, WHITE, exit_button)

        txt_resume = font.render("Resume", True, BG)
        txt_settings = font.render("Settings", True, BG)
        txt_about = font.render("About", True, BG)
        txt_exit = font.render("Exit", True, BG)

        WIN.blit(txt_resume, (resume_button.centerx - txt_resume.get_width() // 2,
                              resume_button.centery - txt_resume.get_height() // 2))
        WIN.blit(txt_settings, (settings_button.centerx - txt_settings.get_width() // 2,
                                 settings_button.centery - txt_settings.get_height() // 2))
        WIN.blit(txt_about, (about_button.centerx - txt_about.get_width() // 2,
                              about_button.centery - txt_about.get_height() // 2))
        WIN.blit(txt_exit, (exit_button.centerx - txt_exit.get_width() // 2,
                             exit_button.centery - txt_exit.get_height() // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "Resume"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.collidepoint(event.pos):
                    return "Resume"
                elif settings_button.collidepoint(event.pos):
                    settings_menu()
                elif about_button.collidepoint(event.pos):
                    about_menu()
                elif exit_button.collidepoint(event.pos):
                    return "Exit"


def settings_menu():
    global enable_nuke_key
    in_settings = True
    checkbox_rect = pygame.Rect(WIDTH // 2 - 50, 200, 20, 20)
    back_button = pygame.Rect(WIDTH // 2 - 100, 300, 200, 50)
    while in_settings:
        WIN.fill(BG)
        title_text = font.render("Settings", True, WHITE)
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        # Draw the checkbox and label.
        pygame.draw.rect(WIN, WHITE, checkbox_rect, 2)
        if enable_nuke_key:
            pygame.draw.line(WIN, WHITE, (checkbox_rect.left, checkbox_rect.top),
                             (checkbox_rect.right, checkbox_rect.bottom), 2)
            pygame.draw.line(WIN, WHITE, (checkbox_rect.left, checkbox_rect.bottom),
                             (checkbox_rect.right, checkbox_rect.top), 2)
        label = font.render("Enable Nuke (press N to spawn)", True, WHITE)
        WIN.blit(label, (checkbox_rect.right + 10, checkbox_rect.top))

        pygame.draw.rect(WIN, WHITE, back_button)
        back_text = font.render("Back", True, BG)
        WIN.blit(back_text, (back_button.centerx - back_text.get_width() // 2,
                             back_button.centery - back_text.get_height() // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if checkbox_rect.collidepoint(event.pos):
                    enable_nuke_key = not enable_nuke_key
                elif back_button.collidepoint(event.pos):
                    in_settings = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_settings = False


def about_menu():
    in_about = True
    back_button = pygame.Rect(WIDTH // 2 - 100, 400, 200, 50)
    while in_about:
        WIN.fill(BG)
        about_lines = [
            "The Attack Of The Gamer Boys",
            "Version 1.0",
            "A fun Pygame project.",
            "Press ESC to return."
        ]
        start_y = 150
        for line in about_lines:
            text = font.render(line, True, WHITE)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, start_y))
            start_y += 40
        pygame.draw.rect(WIN, WHITE, back_button)
        back_text = font.render("Back", True, BG)
        WIN.blit(back_text, (back_button.centerx - back_text.get_width() // 2,
                             back_button.centery - back_text.get_height() // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    in_about = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_about = False

# ---------------------------
# Main Game Loop ("run_game")
# ---------------------------
def run_game():
    run = True
    clock = pygame.time.Clock()
    player = Player()
    controllers = []
    enemies = []
    powerups = []
    floating_texts = []
    score = 0

    shoot_cooldown = 0
    spawn_timer = 0       # spawn enemies every 30 frames (~0.5 sec)
    powerup_timer = 0     # spawn powerups every 600 frames (~10 sec)
    escalation_timer = 0  # increases enemy spawn count over time
    enemy_spawn_count = 1

    player_hits = 0
    game_over = False

    while run:
        clock.tick(FPS)
        # Process events, including pause (Esc) and N key for spawning nuke powerup.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    choice = pause_menu()
                    if choice == "Exit":
                        run = False
                        break
                # Instead of immediately nuking enemies, N spawns a nuke powerup to pick-up.
                elif event.key == pygame.K_n and enable_nuke_key:
                    x = random.randint(0, WIDTH - 20)
                    new_nuke = {"type": "nuke", "rect": pygame.Rect(x, 0, 20, 20)}
                    powerups.append(new_nuke)

        keys = pygame.key.get_pressed()
        player.move(keys)

        shoot_cooldown = max(shoot_cooldown - 1, -999)
        spawn_timer += 1
        powerup_timer += 1
        escalation_timer += 1

        if player.powerups["ps5"] > 0:
            player.powerups["ps5"] -= 1
        if player.powerups["special"] > 0:
            player.powerups["special"] -= 1

        if escalation_timer >= 1800:
            enemy_spawn_count += 3
            escalation_timer = 0

        # Shooting logic.
        if keys[pygame.K_SPACE] and shoot_cooldown <= 0:
            damage = 1
            img = controller_img
            count = 1
            controller_type = "normal"
            if player.powerups["ps5"] > 0:
                damage = 3
                img = ps5_controller
            if player.powerups["special"] > 0:
                count = 2
                controller_type = "special"

            for i in range(count):
                offset = (i - (count - 1) / 2) * 15
                controllers.append(Controller(player.x + 20 + offset, player.y, damage, img, controller_type))
            shoot_cooldown = 15

        # Spawn enemies every 30 frames.
        if spawn_timer >= 30:
            for _ in range(enemy_spawn_count):
                if random.randint(1, 5) == 1:
                    enemies.append(Skells())
                else:
                    enemies.append(Enemy())
            spawn_timer = 0

        # Spawn regular powerups every 600 frames.
        if powerup_timer >= 600:
            powerups.append(spawn_powerup())
            powerup_timer = 0

        # Update controllers.
        for c in controllers[:]:
            c.move()
            if c.y < -10:
                controllers.remove(c)

        # Update enemies.
        for e in enemies[:]:
            e.move()
            if e.y > HEIGHT:
                enemies.remove(e)

        # Handle collisions: controllers vs. enemies.
        special_kills_this_frame = 0
        normal_kills_this_frame = 0
        for c in controllers[:]:
            for e in enemies[:]:
                if c.rect.colliderect(e.rect):
                    e.hp -= c.damage
                    floating_texts.append(FloatingText(e.x, e.y, str(e.hp), RED, lifetime=60))
                    if e.hp <= 0:
                        if c.controller_type == "special":
                            special_kills_this_frame += 1
                        else:
                            normal_kills_this_frame += 1
                        enemies.remove(e)
                    if c in controllers:
                        controllers.remove(c)
                    break

        frame_points = (normal_kills_this_frame * 15 +
                        (special_kills_this_frame // 2) * 25 +
                        (special_kills_this_frame % 2) * 15)
        score += frame_points

        # Collision detection: player vs. enemies.
        for e in enemies[:]:
            if e.rect.colliderect(player.get_rect()):
                player_hits += 1
                enemies.remove(e)
                if player_hits >= 3:
                    game_over = True
                    break

        # Update floating texts.
        for ft in floating_texts[:]:
            ft.update()
            if ft.alpha <= 0:
                floating_texts.remove(ft)

        # Collision detection: player picks up powerups.
        for p in powerups[:]:
            p["rect"].y += 3
            if p["rect"].colliderect(player.get_rect()):
                if p["type"] == "nuke":
                    enemies.clear()
                else:
                    player.powerups[p["type"]] = 600
                powerups.remove(p)

        # Draw game elements.
        WIN.fill(BG)
        for c in controllers:
            c.draw()
        for e in enemies:
            e.draw()
        for p in powerups:
            draw_powerup(p)
        player.draw()
        for ft in floating_texts:
            ft.draw()

        # Draw UI information.
        txt_instructions = font.render("Press SPACE to throw controllers!", True, WHITE)
        WIN.blit(txt_instructions, (10, 10))
        txt_score = font.render(f"Score: {score}", True, WHITE)
        WIN.blit(txt_score, (10, 35))
        txt_hits = font.render(f"Player Hits: {player_hits}", True, WHITE)
        WIN.blit(txt_hits, (10, 60))
        if player.powerups["ps5"] > 0:
            ps5_count = player.powerups["ps5"] // FPS
            txt_ps5 = font.render(f"PS5: {ps5_count}", True, WHITE)
            WIN.blit(txt_ps5, (10, 85))
        if player.powerups["special"] > 0:
            special_count = player.powerups["special"] // FPS
            txt_special = font.render(f"Special: {special_count}", True, WHITE)
            WIN.blit(txt_special, (10, 110))

        pygame.display.update()

        if game_over:
            leaderboard.append(score)
            restart = display_leaderboard(leaderboard)
            if restart:
                run_game()  # restart the game
                return
            else:
                run = False

# ---------------------------
# Main Function / State Machine
# ---------------------------
def main():
    while True:
        option = main_menu()
        if option == "Start Game":
            run_game()

if __name__ == "__main__":
    main()
