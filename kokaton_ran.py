import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class RedScreenOfDeath:
    """
    体力に応じて画面端が赤くなる効果を実装するクラス
    """
    def __init__(self, rsod_img: str = "fig/RSOB1.png"):
        """
        画像を読み込む
        引数1 rsod_img : 画像のパス
        """
        self.rsod_img = pg.image.load(rsod_img).convert_alpha() #rsod_imgのアルファ値を利用

    def effect(self, screen: pg.Surface, hp: int) -> None:
        """
        エフェクトを画面に適応する関数
        引数1 screen : 画面Surface
        引数2 hp : こうかとんの体力
        """
        if 1 <= hp <= 3:
            toumeido = 140 - (hp - 1) * 85
            self.rsod_img.set_alpha(toumeido)
            screen.blit(self.rsod_img, (0, 0))


def main():
    width = 800
    height = 600
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/bg_pattern2_aozora.png") 
    bg_img = pg.transform.scale(bg_img, (800, 600)) #画面の解像度に合わせる
    bg_img2 = pg.image.load("fig/bg_pattern4_yoru.png")
    bg_img2 = pg.transform.scale(bg_img2, (800, 600)) #画面の解像度に合わせる
    kk_img = pg.image.load("fig/3.png") #練習2
    kk_img = pg.transform.flip(kk_img, True, False)
    kk_img = pg.transform.rotozoom(kk_img, 10, 1.0)
    kk_rct = kk_img.get_rect()#練習10-1
    kk_rct.center = 300, 200#練習10-2
    
    
    tmr = 0
    i = 0
    M = kk_rct.move_ip
    
    hp = 1
    rsod = RedScreenOfDeath()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        X = tmr%8000 #練習6,9
        
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
        

        for i in range(10): # 7000フレーム目で終了を予定
            if i < 4:
                screen.blit(bg_img, [-X + i * 800, 0]) #昼の画像
            elif i == 9:
                screen.blit(bg_img, [-X + i * 800, 0])
            else:
                screen.blit(bg_img2, [-X + i * 800, 0]) #夜の画像
        
            
        rsod.effect(screen, hp)
        
        screen.blit(kk_img, kk_rct) #練習4,10-5
        pg.display.update()
        tmr += 1        
        if tmr > 7200:
            tmr = 0
        clock.tick(200) #練習5

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()