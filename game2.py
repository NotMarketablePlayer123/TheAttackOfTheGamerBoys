import pygame
import random

# Global leaderboard will persist until the game is closed.
leaderboard = []

# Init
pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gamer Boy vs The Haters")

# Colors
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
BG    = (30, 30, 30)

# Clock
FPS = 60

# Load Images from sprites folder
player_img = pygame.image.load("sprites/player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (50, 50))

# Increase controller size: originally (10, 5), now 4x -> (40, 20)
controller_img = pygame.image.load("sprites/contoler.png").convert_alpha()
controller_img = pygame.transform.scale(controller_img, (40, 20))

enemy_img = pygame.image.load("sprites/enemy.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (40, 40))

# Increase ps5_controller size to 4x: originally (12, 6), now (48, 24)
ps5_controller = pygame.image.load("sprites/ps5_controller.png").convert_alpha()
ps5_controller = pygame.transform.scale(ps5_controller, (48, 24))

special_controller = pygame.image.load("sprites/special_controller.png").convert_alpha()
special_controller = pygame.transform.scale(special_controller, (30, 15))  # Increased to 3x its previous size

# Replace the nuke image with the new image.
nuke_img = pygame.image.load("sprites/nuke.png").convert_alpha()
nuke_img = pygame.transform.scale(nuke_img, (20, 20))

# Load skells image.
skells_img = pygame.image.load("sprites/skells.png").convert_alpha()
skells_img = pygame.transform.scale(skells_img, (40, 40))

# Fonts
font = pygame.font.SysFont("Arial", 20)


# FloatingText class to display fading numbers (for enemy HP).
class FloatingText:
    def __init__(self, x, y, text, color, lifetime=60):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifetime = lifetime  # lifetime in frames
        self.counter = 0
        self.alpha = 255
        self.image = font.render(text, True, color)
        self.image.set_alpha(self.alpha)

    def update(self):
        self.counter += 1
        self.alpha = max(0, 255 - int((255 / self.lifetime) * self.counter))
        self.image.set_alpha(self.alpha)
        self.y -= 0.5  # float upward slowly

    def draw(self):
        WIN.blit(self.image, (self.x, self.y))


class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 60
        self.speed = 5
        # Powerup timers stored in frames; 600 frames = ~10 sec.
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


# New enemy type "Skells"
class Skells:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 40)
        self.y = -40
        self.hp = 5  # Takes 5 hits.
        self.rect = skells_img.get_rect(topleft=(self.x, self.y))

    def move(self):
        self.y += 3
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        WIN.blit(skells_img, (self.x, self.y))


def spawn_powerup():
    r = random.randint(1, 40)
    if r == 1:
        choice = "nuke"
    else:
        choice = random.choice(["ps5", "special"])
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
    # Sort scores in descending order.
    sorted_scores = sorted(leaderboard, reverse=True)
    running = True
    restart_requested = False

    # Define buttons.
    restart_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT - 150, 100, 40)
    exit_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT - 150, 100, 40)

    while running:
        WIN.fill(BG)
        title_text = font.render("Leaderboard", True, WHITE)
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        # Display each score.
        for i, score in enumerate(sorted_scores):
            entry_text = font.render(f"{i + 1}. {score}", True, WHITE)
            WIN.blit(entry_text, (WIDTH // 2 - entry_text.get_width() // 2, 100 + i * 30))

        # Draw Restart button.
        pygame.draw.rect(WIN, WHITE, restart_button)
        restart_text = font.render("Restart", True, BG)
        WIN.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2,
                                restart_button.centery - restart_text.get_height() // 2))

        # Draw Exit button.
        pygame.draw.rect(WIN, WHITE, exit_button)
        exit_text = font.render("Exit", True, BG)
        WIN.blit(exit_text, (exit_button.centerx - exit_text.get_width() // 2,
                             exit_button.centery - exit_text.get_height() // 2))

        instructions = font.render("Click a button", True, WHITE)
        WIN.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT - 80))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
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
        # End event loop

    return restart_requested


def main():
    run = True
    clock = pygame.time.Clock()
    player = Player()
    controllers = []
    enemies = []
    powerups = []
    floating_texts = []  # List for FloatingText instances.
    score = 0

    shoot_cooldown = 0
    spawn_timer = 0       # Spawns occur every 30 frames (~0.5 sec).
    powerup_timer = 0     # Powerups spawn every 600 frames (~10 sec).
    escalation_timer = 0  # Timer to increase enemy spawn count.
    enemy_spawn_count = 1 # Starting spawn count.

    player_hits = 0       # Number of collisions between player and enemies.
    game_over = False

    while run:
        clock.tick(FPS)
        WIN.fill(BG)
        keys = pygame.key.get_pressed()
        player.move(keys)

        shoot_cooldown -= 1
        spawn_timer += 1
        powerup_timer += 1
        escalation_timer += 1

        # Decrement active powerup timers if active.
        if player.powerups["ps5"] > 0:
            player.powerups["ps5"] -= 1
        if player.powerups["special"] > 0:
            player.powerups["special"] -= 1

        # Increase enemy spawn count every 30 seconds (1800 frames).
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

        # Spawn enemies every 30 frames (~0.5 sec).
        if spawn_timer >= 30:
            for _ in range(enemy_spawn_count):
                # 1 in 5 chance to spawn a Skells enemy.
                if random.randint(1, 5) == 1:
                    enemies.append(Skells())
                else:
                    enemies.append(Enemy())
            spawn_timer = 0

        # Spawn powerups every 600 frames (~10 sec).
        if powerup_timer >= 600:
            powerups.append(spawn_powerup())
            powerup_timer = 0

        # Update and draw controllers.
        for c in controllers[:]:
            c.move()
            c.draw()
            if c.y < -10:
                controllers.remove(c)

        # Update and draw enemies.
        for e in enemies[:]:
            e.move()
            e.draw()
            if e.y > HEIGHT:
                enemies.remove(e)

        # Temporary counters for scoring this frame.
        special_kills_this_frame = 0
        normal_kills_this_frame = 0

        # Collision detection: controllers vs. enemies.
        for c in controllers[:]:
            for e in enemies[:]:
                if c.rect.colliderect(e.rect):
                    e.hp -= c.damage
                    # Create floating text with remaining HP.
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

        # Award points.
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

        # Update and draw floating texts.
        for ft in floating_texts[:]:
            ft.update()
            ft.draw()
            if ft.alpha <= 0:
                floating_texts.remove(ft)

        # Game over: update leaderboard and show the leaderboard screen with buttons.
        if game_over:
            leaderboard.append(score)
            restart = display_leaderboard(leaderboard)
            if restart:
                main()  # Restart the game.
                return
            else:
                run = False
                break

        # Powerup collision detection.
        for p in powerups[:]:
            p["rect"].y += 3
            draw_powerup(p)
            if p["rect"].colliderect(pygame.Rect(player.x, player.y, 50, 50)):
                if p["type"] == "nuke":
                    enemies.clear()
                else:
                    # Activate powerup for 600 frames (≈10 seconds).
                    player.powerups[p["type"]] = 600
                powerups.remove(p)

        # Draw player.
        player.draw()

        # UI: Display instructions, score, hit count, and powerup countdowns.
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


if __name__ == "__main__":
    main()
