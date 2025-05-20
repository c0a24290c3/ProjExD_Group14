import os
import sys
import random
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH = 1100  # ゲームウィンドウの幅
HEIGHT = 600  # ゲームウィンドウの高さ


class Enemy(pg.sprite.Sprite):
    """
    障害物, 敵に関するクラス
    ランダムの敵画像を表示する(出現範囲も指定)
    """
    imgs = [pg.image.load(f"fig/{i}.png") for i in range(1, 4)] # 画像
    
    def __init__(self) -> None:
        super().__init__()
        self.image = pg.transform.rotozoom(random.choice(__class__.imgs), 0, 1)
        self.rect = self.image.get_rect()
        self.rect.center = random.randint(WIDTH, WIDTH + 200), random.randint(HEIGHT - 300, HEIGHT) 
        self.vx, self.vy = -1, 0 #背景とともに移動

    def update(self) -> None:
        """
        敵を背景とともに左にスクロール
        画面外に出たら削除する
        """
        self.rect.move_ip(self.vx, self.vy)
        if self.rect.right < 0:
            self.kill()


def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_img2 = pg.transform.flip(bg_img, True, False)#練習8
    kk_img = pg.image.load("fig/3.png") #練習2
    kk_img = pg.transform.flip(kk_img, True, False)
    kk_img = pg.transform.rotozoom(kk_img, 10, 1.0)
    kk_rct = kk_img.get_rect()#練習10-1
    kk_rct.center = 300, 200#練習10-2
    tmr = 0
    M = kk_rct.move_ip
    enemy_group = pg.sprite.Group() # 敵グループ作り
    enemy_spawn_interval = 400
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        if tmr % enemy_spawn_interval == 0:
            enemy_group.add(Enemy()) # 敵出現

        X = tmr%3200 #練習6,9
        
        key_lst = pg.key.get_pressed()#練習10-3
        if key_lst[pg.K_UP]:#練習10-4
            M((-1,-1))
        elif key_lst[pg.K_DOWN]:
            M((-1,1))
        elif key_lst[pg.K_LEFT]:
            M((-1,0))
        elif key_lst[pg.K_RIGHT]:
            M((2,0))
        else: M((-1,0))

        for enemy in enemy_group: # 当たり判定を各敵スプライトとこうかとんのRectを個別に(こうかとんのクラス作るなら書き換え必要)
            if kk_rct.colliderect(enemy.rect):
                enemy.kill()
                return
        pg.display.update()

        screen.blit(bg_img, [-X, 0])
        screen.blit(bg_img2, [-X+1600,0])#練習7,8
        screen.blit(bg_img, [-X+3200,0])#練習9
        screen.blit(kk_img, kk_rct) #練習4,10-5
        enemy_group.update()
        enemy_group.draw(screen)
        pg.display.update()
        tmr += 1        
        clock.tick(200) #練習5

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()