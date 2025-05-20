import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_img2 = pg.transform.flip(bg_img, True, False)# 背景画像反転
    kk_img = pg.image.load("fig/3.png") # キャラクターの画像読み込み
    kk_img = pg.transform.flip(kk_img, True, False)
    kk_img = pg.transform.rotozoom(kk_img, 10, 1.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 150, 500 # こうかとん初期座標
    M = kk_rct.move_ip
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        X = tmr %3200 # 背景ループ
        
        key_lst = pg.key.get_pressed()
        if key_lst[pg.K_UP]: # こうかとん移動キー
            M((-1,-1))
        elif key_lst[pg.K_DOWN]:
            M((-1,1))
        elif key_lst[pg.K_LEFT]:
            M((-1,0))
        elif key_lst[pg.K_RIGHT]:
            M((1,0))
        
        screen.blit(bg_img, [-X, 0])  # 背景貼り付け 
        screen.blit(bg_img2, [-X+1600,0])
        screen.blit(bg_img, [-X+3200,0])
        screen.blit(kk_img, kk_rct) # キャラクター貼り付け
        pg.display.update()
        tmr += 1        
        clock.tick(200) # FPS設定

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()