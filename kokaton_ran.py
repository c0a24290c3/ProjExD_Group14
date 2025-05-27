import os
import sys
import pygame as pg
import time
import random

os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH = 1200  # ゲームウィンドウの幅
HEIGHT = 600  # ゲームウィンドウの高さ

class RedScreenOfDeath: 
    """
    体力に応じて画面端が赤くなる効果を実装するクラス
    """
    def __init__(self, rsod_img: str = "fig/RSOD.png"):
        try:
            self.rsod_img_original = pg.image.load(rsod_img).convert_alpha()
            self.rsod_img = self.rsod_img_original
        except pg.error as e:
            self.rsod_img = None

    def effect(self, screen: pg.Surface, health: int) -> None:
        if self.rsod_img is None:
            return
        if 1 <= health <= 100:
            toumeido = 255 - (255 * (health / 100))
            toumeido = max(0, min(255, toumeido))
            self.rsod_img.set_alpha(toumeido)
            screen.blit(self.rsod_img, (0, 0))

class Enemy(pg.sprite.Sprite): 
    """
    障害物, 敵に関するクラス
    ランダムの敵画像を表示する(出現範囲も指定)
    """
    try:
        imgs = [pg.image.load(f"fig/{i}.png") for i in range(1, 4)]
    except pg.error as e:
        imgs = []

    def __init__(self) -> None:
        super().__init__()
        if not __class__.imgs:
            self.image = pg.Surface((50,50))
            self.image.fill((255,0,0))
        else:
            self.image = pg.transform.rotozoom(random.choice(__class__.imgs), 0, 1)
        self.rect = self.image.get_rect()
        self.rect.center = random.randint(WIDTH, WIDTH + 200), random.randint(HEIGHT - 300, HEIGHT - 90) 
        self.vx, self.vy = -5, 0

    def update(self) -> None:
        self.rect.move_ip(self.vx, self.vy)
        if self.rect.right < 0:
            self.kill()

class Score:
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (0, 200, 100)
        self.value = 0
        self.image = self.font.render(f"Score: {self.value}", True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (100, 80)

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"Score: {self.value}", True, self.color)
        screen.blit(self.image, self.rect)

class Health:
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (255, 0, 255)
        self.max_health = 100
        self.health = self.max_health
        self.image = self.font.render(f"HP: {self.health}", True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (100, 40)
    
    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"HP: {self.health}", True, self.color)
        screen.blit(self.image, self.rect)

class Player(pg.sprite.Sprite):
    def __init__(self, kk_img_normal, kk_img_crouch, ground_y):
        super().__init__()
        self.img_normal = kk_img_normal
        self.img_crouch = kk_img_crouch
        self.image = self.img_normal
        self.rect = self.image.get_rect()
        self.rect.centerx = 150
        self.rect.bottom = ground_y
        self.ground_y = ground_y

        self.is_jumping = False
        self.jump_power = -5.5
        self.gravity = 0.07
        self.y_velocity = 0.0
        self.is_crouching = False

    def update(self, pressed_keys):
        delta_x = 0
        if pressed_keys[pg.K_LEFT]:
            delta_x = -2
        elif pressed_keys[pg.K_RIGHT]:
            delta_x = 1

        if pressed_keys[pg.K_DOWN] and not self.is_jumping:
            if not self.is_crouching:
                self.is_crouching = True
                self.image = self.img_crouch
                old_centerx = self.rect.centerx
                self.rect = self.image.get_rect()
                self.rect.centerx = old_centerx
                self.rect.bottom = self.ground_y
        elif self.is_crouching and not pressed_keys[pg.K_DOWN]:
            self.is_crouching = False
            self.izmage = self.img_normal
            old_centerx = self.rect.centerx
            self.rect = self.image.get_rect()
            self.rect.centerx = old_centerx
            self.rect.bottom = self.ground_y

        if pressed_keys[pg.K_UP] and not self.is_jumping and not self.is_crouching:
            self.is_jumping = True
            self.y_velocity = self.jump_power

        if self.is_jumping:
            self.y_velocity += self.gravity
            self.rect.y += int(self.y_velocity)
            if self.rect.bottom >= self.ground_y:
                self.rect.bottom = self.ground_y
                self.is_jumping = False
                self.y_velocity = 0.0

        self.rect.x += delta_x
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


def show_title_screen(screen: pg.Surface) -> bool:
    title_font = pg.font.Font(None, 80)
    small_font = pg.font.Font(None, 60)

    txt_title = title_font.render("KOUKATON RUN", True, (255, 255, 255))
    txt_start = small_font.render("START : PRESS ENTER", True, (255, 255, 255))
    
    title_rect = txt_title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    start_rect = txt_start.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))

    title_running = True
    while title_running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    return True

        screen.fill((0, 0, 0))
        screen.blit(txt_title, title_rect)
        screen.blit(txt_start, start_rect)
        pg.display.update()
        pg.time.Clock().tick(60)
    return False


def main_game(screen: pg.Surface) -> None:
    pg.display.set_caption("走れ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock: pg.time.Clock = pg.time.Clock()
    rsod = RedScreenOfDeath()
    score_obj = Score()
    health_obj = Health()

    try:
        bg_img_original: pg.Surface = pg.image.load("fig/pg_bg.jpg")
    except pg.error as e:
        pg.quit()
        sys.exit()
    bg_img_flipped: pg.Surface = pg.transform.flip(bg_img_original, True, False)

    try:
        kk_img_base: pg.Surface = pg.image.load("fig/3.png").convert_alpha()
    except pg.error as e:
        pg.quit()
        sys.exit()
    kk_img_base = pg.transform.flip(kk_img_base, True, False)

    kk_angle: int = 10
    kk_zoom: float = 1.0
    kk_img_normal: pg.Surface = pg.transform.rotozoom(kk_img_base, kk_angle, kk_zoom)
    crouch_scale_y: float = 0.6
    kk_img_crouch: pg.Surface = pg.transform.scale(
        kk_img_normal,
        (kk_img_normal.get_width(), int(kk_img_normal.get_height() * crouch_scale_y))
    )
    
    ground_y: int = HEIGHT - 100 
    
    player = Player(kk_img_normal, kk_img_crouch, ground_y)
    all_sprites = pg.sprite.Group() 
    all_sprites.add(player)


    tmr: int = 0
    game_running: bool = True
    enemy_group = pg.sprite.Group() # 敵グループ作り
    enemy_spawn_interval = 400

    
    while game_running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_running = False

        pressed_keys = pg.key.get_pressed()
        player.update(pressed_keys) 
        enemy_group.update()

        if tmr % enemy_spawn_interval == 0:
            enemy_group.add(Enemy()) # 敵出現

        if tmr % 10 == 0: 
            score_obj.value += 1

        if health_obj.health == 0:
            screen.fill((0,0,0)) 
            
            gmfo = pg.font.Font(None, 150)
            gmov = gmfo.render("GAME OVER", True, (255, 0, 0))
            gmov_rect = gmov.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))
            screen.blit(gmov, gmov_rect)

            score_img_gameover = score_obj.font.render(f"Score: {score_obj.value}", True, score_obj.color)
            score_rect_gameover = score_img_gameover.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
            screen.blit(score_img_gameover, score_rect_gameover)
            
            pg.display.update()
            time.sleep(3)
            game_running = False

        collided_enemies = pg.sprite.spritecollide(player, enemy_group, True) # Trueで衝突した敵をグループから削除
        for enemy in collided_enemies:
            health_obj.health -= 10 # HPを10減らす
            if health_obj.health < 0:
                health_obj.health = 0

        background_scroll = tmr % bg_img_original.get_width()
        screen.blit(bg_img_original, [-background_scroll, 0])
        screen.blit(bg_img_flipped, [-background_scroll + bg_img_original.get_width(), 0])
        screen.blit(bg_img_original, [-background_scroll + bg_img_original.get_width() * 2, 0])

        all_sprites.draw(screen) 
        enemy_group.draw(screen)
        
        score_obj.update(screen)
        health_obj.update(screen)

        rsod.effect(screen, health_obj.health)
        pg.display.update()
        tmr += 1
        clock.tick(200)


if __name__ == "__main__":
    pg.init()
    main_screen_surface = pg.display.set_mode((WIDTH, HEIGHT))
    
    if show_title_screen(main_screen_surface):
        main_game(main_screen_surface)
    
    pg.quit()
    sys.exit()