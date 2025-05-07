import pygame, random, os
pygame.init()
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCORE_FONT = pygame.font.Font(None, 36)
DINO_WIDTH, DINO_HEIGHT = 50, 50
CACTUS_WIDTH, CACTUS_HEIGHT = 30, 45
GROUND_Y = HEIGHT - 40
DINO_Y_POSITION = GROUND_Y
def load_high_score():
    highscore_path = os.path.join(BASE_DIR, "highscore.txt")
    if os.path.exists(highscore_path):
        with open(highscore_path, "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 0
    else:
        return 0
def save_high_score(score):
    highscore_path = os.path.join(BASE_DIR, "highscore.txt")
    with open(highscore_path, "w") as f:
        f.write(str(score))
def check_collision(dino, cactus_group):
    return pygame.sprite.spritecollide(dino, cactus_group, False)
class Dino(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (DINO_WIDTH, DINO_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.bottom = DINO_Y_POSITION
        self.jump_speed = -18
        self.gravity = 1
        self.velocity = 0
        self.jumping = False
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.jumping:
            self.velocity = self.jump_speed
            self.jumping = True
        self.velocity += self.gravity
        self.rect.y += self.velocity
        if self.rect.bottom >= DINO_Y_POSITION:
            self.rect.bottom = DINO_Y_POSITION
            self.jumping = False
class Cactus(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (CACTUS_WIDTH, CACTUS_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        offset = random.randint(0, 60)
        self.rect.bottom = DINO_Y_POSITION - offset
    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()
def draw_score(score, high_score):
    score_text = SCORE_FONT.render(f"Score: {score}", True, (0, 0, 0))
    hs_text = SCORE_FONT.render(f"High Score: {high_score}", True, (0, 0, 0))
    WIN.blit(score_text, (10, 10))
    WIN.blit(hs_text, (10, 40))
def main(skip_start=False):
    dino_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "dino.png")).convert_alpha()
    cactus_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "cactus.png")).convert_alpha()
    background_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "background.png")).convert()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    dino = Dino(dino_img)
    dino_group = pygame.sprite.GroupSingle(dino)
    cactus_group = pygame.sprite.Group()
    SPAWNCACTUS = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWNCACTUS, 1500)
    score = 0
    high_score = load_high_score()
    game_over = False
    waiting_to_start = not skip_start
    run = True
    while run:
        CLOCK.tick(60)
        if not game_over and not waiting_to_start:
            score += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == SPAWNCACTUS and not game_over and not waiting_to_start:
                cactus = Cactus(cactus_img)
                cactus_group.add(cactus)
            if event.type == pygame.KEYDOWN:
                if waiting_to_start and event.key == pygame.K_SPACE:
                    waiting_to_start = False
                    score = 0
                if game_over and event.key == pygame.K_r:
                    main(skip_start=True)
                    return
        if waiting_to_start:
            WIN.blit(background_img, (0, 0))
            font = pygame.font.Font(None, 40)
            text = font.render("Apasă SPACE pentru a începe", True, (0, 0, 0))
            dino.rect.bottom = DINO_Y_POSITION
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
            dino_group.draw(WIN)
            pygame.display.update()
            continue
        if not game_over:
            WIN.blit(background_img, (0, 0))
            dino_group.update()
            cactus_group.update()
            if check_collision(dino, cactus_group):
                game_over = True
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
            dino_group.draw(WIN)
            cactus_group.draw(WIN)
            draw_score(score, high_score)
            pygame.display.update()
        else:
            WIN.fill((255, 255, 255))
            font_large = pygame.font.Font(None, 80)
            font_small = pygame.font.Font(None, 40)
            text_game_over = font_large.render("GAME OVER", True, (200, 0, 0))
            text_restart = font_small.render("Apasă R pentru a reîncepe", True, (0, 0, 0))
            text_score = font_small.render(f"Scorul tău: {score}", True, (0, 0, 0))
            text_high = font_small.render(f"High Score: {high_score}", True, (0, 0, 0))
            WIN.blit(text_game_over, (WIDTH // 2 - text_game_over.get_width() // 2, HEIGHT // 3))
            WIN.blit(text_score, (WIDTH // 2 - text_score.get_width() // 2, HEIGHT // 2))
            WIN.blit(text_high, (WIDTH // 2 - text_high.get_width() // 2, HEIGHT // 2 + 40))
            WIN.blit(text_restart, (WIDTH // 2 - text_restart.get_width() // 2, HEIGHT // 2 + 80))
            pygame.display.update()
    pygame.quit()
if __name__ == "__main__":
    main()
