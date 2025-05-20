import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
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
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

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
        
        screen.blit(bg_img, [-X, 0])
        screen.blit(bg_img2, [-X+1600,0])#練習7,8
        screen.blit(bg_img, [-X+3200,0])#練習9
        screen.blit(kk_img, kk_rct) #練習4,10-5
        pg.display.update()
        tmr += 1        
        clock.tick(200) #練習5

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()