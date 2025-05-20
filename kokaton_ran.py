import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main() -> None:
    """
    「走れ！こうかとん」ゲームのメイン処理を実行する。
    画面初期化、画像読み込み、イベントループ、キャラクター制御、描画処理を行う。
    """
    pg.display.set_caption("走れ！こうかとん")
    screen_width: int = 800  # 画面幅
    screen_height: int = 600 # 画面高さ 
    screen: pg.Surface = pg.display.set_mode((screen_width, screen_height))
    clock: pg.time.Clock  = pg.time.Clock()

    # 背景画像
    try:
        bg_img_original: pg.Surface = pg.image.load("fig/pg_bg.jpg")
    except pg.error as e:
        pg.quit()
        sys.exit()
    bg_img_flipped: pg.Surface = pg.transform.flip(bg_img_original, True, False) # 背景画像反転

    # こうかとんの元画像をロード
    try:
        kk_img_base: pg.Surface = pg.image.load("fig/3.png").convert_alpha()
    except pg.error as e:
        pg.quit()
        sys.exit()
    kk_img_base = pg.transform.flip(kk_img_base, True, False) # 右向きにする

    kk_angle: int = 10      # こうかとんの傾き角度
    kk_zoom: float = 1.0    # こうかとんの拡大率

    # 通常時のこうかとん画像
    kk_img_normal: pg.Surface = pg.transform.rotozoom(kk_img_base, kk_angle, kk_zoom)

    # しゃがみ時のこうかとん画像
    crouch_scale_y: float = 0.6 # Y方向の縮小率
    kk_img_crouch: pg.Surface = pg.transform.scale(
        kk_img_normal,
        (kk_img_normal.get_width(), int(kk_img_normal.get_height() * crouch_scale_y))
    )

    # こうかとんの初期設定
    current_kk_img: pg.Surface = kk_img_normal 
    kk_rect: pg.Rect = current_kk_img.get_rect()
    kk_rect.centerx = 150 # 初期X位置 
    kk_rect.bottom = 500  # 初期Y位置 
    ground_y: int = kk_rect.bottom

    # ジャンプ関連
    is_jumping: bool = False
    jump_power: float = -5.0   # ジャンプの初速 
    gravity: float = 0.0625    # 重力加速度 
    y_velocity: float = 0.0    # Y方向の現在の速度

    # しゃがみ関連
    is_crouching: bool = False

    tmr: int = 0 
    running: bool = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False 

        pressed_keys: pg.key.ScancodeWrapper = pg.key.get_pressed()

        # こうかとんのX方向の移動量
        delta_x: int = 0
        if pressed_keys[pg.K_LEFT]:
            delta_x = -2 # 左移動速度 
        elif pressed_keys[pg.K_RIGHT]:
            delta_x = 1  # 右移動速度

        # 下キーが押され、かつジャンプ中でない場合
        if pressed_keys[pg.K_DOWN] and not is_jumping:
            if not is_crouching: # まだしゃがんでいなければ、しゃがみ状態に移行
                is_crouching = True
                current_kk_img = kk_img_crouch
                old_centerx: int = kk_rect.centerx
                kk_rect = current_kk_img.get_rect()
                kk_rect.centerx = old_centerx
                kk_rect.bottom = ground_y # 足元を地面に合わせる
        # しゃがみ中に下キーが押されていなければ、立ち上がり状態に移行
        elif is_crouching and not pressed_keys[pg.K_DOWN]:
            is_crouching = False
            current_kk_img = kk_img_normal
            old_centerx: int = kk_rect.centerx
            kk_rect = current_kk_img.get_rect()
            kk_rect.centerx = old_centerx
            kk_rect.bottom = ground_y # 足元を地面に合わせる

        # 上キーが押され、かつジャンプ中でなく、かつしゃがんでもいない場合ジャンプする
        if pressed_keys[pg.K_UP] and not is_jumping and not is_crouching:
            is_jumping = True
            y_velocity = jump_power 
            kk_rect.bottom = ground_y

        if is_jumping:
            y_velocity += gravity       # 速度に重力を加算
            kk_rect.y += int(y_velocity) # Y座標を更新
            if kk_rect.bottom >= ground_y: # 地面に着地したら
                kk_rect.bottom = ground_y  # 地面の位置に修正
                is_jumping = False         # ジャンプ終了
                y_velocity = 0.0           # Y速度リセット

        kk_rect.x += delta_x

        # 画面外に出ないようにする処理 (こうかとん)
        if kk_rect.left < 0:
            kk_rect.left = 0
        if kk_rect.right > screen_width:
            kk_rect.right = screen_width

        background: int = tmr % 3200

        # 背景描画
        screen.blit(bg_img_original, [-background, 0])
        screen.blit(bg_img_flipped, [-background + 1600, 0])
        screen.blit(bg_img_original, [-background + 3200, 0])

        # こうかとん描画
        screen.blit(current_kk_img, kk_rect)

        pg.display.update() # 画面全体を更新
        tmr += 1
        clock.tick(200) # FPS設定

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    pg.init()
    main()