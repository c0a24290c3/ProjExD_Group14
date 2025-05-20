import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Score:
    #スコアの表示
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (0, 200, 100)
        self.value = 0
        self.image = self.font.render(f"Score: {self.value}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (100,80)

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"Score: {self.value}", 0, self.color)
        screen.blit(self.image, self.rect)

class Health:
    #HPの表示
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (255,0,255)
        self.health = 100 #初期HP
        self.image = self.font.render(f"HP: {self.health}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (100,40)
    
    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"HP: {self.health}", 0, self.color)
        screen.blit(self.image, self.rect)

def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    score=Score()
    health=Health()
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
        if tmr % 10 == 0:
            health.health -=1
            score.value+=1 #タイマー10ごとにスコア1加算
        if health.health==0: #HPが0になったときgameover
            score_image = score.font.render(f"Score: {score.value}", 0, score.color)
            score_rect = score_image.get_rect()
            score_rect.center=400, 400
            screen.blit(score_image,score_rect)
            gmfo=pg.font.Font(None,150)
            gmov=gmfo.render(f"GAME OVER",0, (0,0,0))
            gmov_rect=gmov.get_rect()
            gmov_rect.center=(400, 200)
            screen.blit(gmov,gmov_rect)
            pg.display.update()
            return
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
        score.update(screen)
        health.update(screen)
        pg.display.update()
        tmr += 1       
        clock.tick(200) #練習5

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()