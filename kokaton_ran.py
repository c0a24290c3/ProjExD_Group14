import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen_width = 800  # 画面幅を定数化
    screen_height = 600 # 画面高さを定数化
    screen = pg.display.set_mode((screen_width, screen_height))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_img2 = pg.transform.flip(bg_img, True, False) # 背景画像反転

    # こうかとんの元画像をロード
    kk_img_base = pg.image.load("fig/3.png").convert_alpha()
    kk_img_base = pg.transform.flip(kk_img_base, True, False)

    kk_angle = 10  # こうかとんの角度
    kk_zoom = 1.0  # こうかとんの拡大率

    # 通常時のこうかとん画像
    kk_img_normal = pg.transform.rotozoom(kk_img_base, kk_angle, kk_zoom)

    # しゃがみ時のこうかとん画像
    crouch_scale_y = 0.6 # Y方向の縮小率
    kk_img_crouch = pg.transform.scale(
        kk_img_normal,
        (kk_img_normal.get_width(), int(kk_img_normal.get_height() * crouch_scale_y))
    )

    kk_img = kk_img_normal
    kk_rct = kk_img.get_rect()
    kk_rct.center = 150, 500

    ground_y = kk_rct.bottom

    # ジャンプ関連の変数
    is_jumping = False
    jump_power = -5     # ジャンプの初速を調整
    gravity = 0.0625    # 重力を調整
    y_velocity = 0

    # しゃがみ関連の変数
    is_crouching = False

    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        X = tmr % 3200

        key_lst = pg.key.get_pressed()

        dx = 0
        if key_lst[pg.K_LEFT]:
            dx = -2
        elif key_lst[pg.K_RIGHT]:
            dx = 1

        if key_lst[pg.K_DOWN] and not is_jumping:
            if not is_crouching:
                is_crouching = True
                kk_img = kk_img_crouch
                old_centerx = kk_rct.centerx
                kk_rct = kk_img.get_rect()
                kk_rct.centerx = old_centerx
                kk_rct.bottom = ground_y
        elif is_crouching and not key_lst[pg.K_DOWN]:
            is_crouching = False
            kk_img = kk_img_normal
            old_centerx = kk_rct.centerx
            kk_rct = kk_img.get_rect()
            kk_rct.centerx = old_centerx
            kk_rct.bottom = ground_y

        if key_lst[pg.K_UP] and not is_jumping and not is_crouching:
            is_jumping = True
            y_velocity = jump_power
            # ジャンプ開始時に足元の位置がずれないようにする
            kk_rct.bottom = ground_y

        if is_jumping:
            y_velocity += gravity
            kk_rct.y += y_velocity
            if kk_rct.bottom >= ground_y: # 地面に着地したら
                kk_rct.bottom = ground_y  # 地面の位置に補正
                is_jumping = False        # ジャンプ終了
                y_velocity = 0            # 速度リセット

        kk_rct.x += dx

        # 画面外に出ないようにする処理
        if kk_rct.left < 0:
            kk_rct.left = 0
        if kk_rct.right > screen_width:
            kk_rct.right = screen_width

        screen.blit(bg_img, [-X, 0])
        screen.blit(bg_img2, [-X+1600, 0])
        screen.blit(bg_img, [-X+3200, 0])
        screen.blit(kk_img, kk_rct)
        pg.display.update()
        tmr += 1
        clock.tick(200) # FPS設定

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()