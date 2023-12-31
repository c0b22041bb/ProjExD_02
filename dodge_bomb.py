import random 
import sys
import pygame as pg
import random as ran


WIDTH, HEIGHT = 1600, 900

delta = { #移動量タプル
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0)
}




def check_bound(obj_rct: pg.Rect):#pg.Rectのクラスのインスタンスが来ることを指定
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル(横方向判定効果、縦方向判定効果)
    画面内ならTrue:画面外ならFalse
    """
    yoko,tate = True,True

    if obj_rct.left < 0 or WIDTH < obj_rct.right:#横方向判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:#縦方向判定
        tate = False
    return yoko,tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    """こうかとん"""
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)#二倍に拡大
    kk_rct = kk_img.get_rect() #SurfaceからRectを抽出する
    kk_rct.center = (900,400)

    kk_img2 = pg.transform.flip(kk_img, True, False) 
    muki = {
        (-5,0) :pg. transform.rotozoom (kk_img, 0,1.0), 
        (-5, -5):pg.transform.rotozoom (kk_img, -45, 1.0),
        (0, -5) :pg. transform.rotozoom (kk_img2,90,1.0), 
        (5, -5) :pg. transform.rotozoom (kk_img2, 45,1.0),        
        (5,0) :pg. transform. rotozoom (kk_img2,0,1.0), 
        (5,5):pg.transform.rotozoom(kk_img2, -45,1.0), 
        (0, 5) :pg. transform.rotozoom(kk_img2, -90,1.0),
        (-5, 5) :pg. transform.rotozoom(kk_img,45 ,1.0),
        (0,0): kk_img
    }

    """ばくだん"""
    bd_img= pg.Surface((20, 20))#爆弾Surfaceをつくる
    bd_img.set_colorkey((0,0,0))#黒を透過させる
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)#中心に半径10の赤い円
    bd_rct = bd_img.get_rect() #SurfaceからRectを抽出する
    x,y = random.randint(0,WIDTH),random.randint(0,HEIGHT)#座標をランダムに生成
    bd_rct.center = (x,y)#Rectにランダムな座標を設定する
    vx,vy = +5,+5

    clock = pg.time.Clock()
    tmr = 0
    """物体表示"""
    bom_img = pg.Surface((20, 20))
    pg.draw.circle(bom_img, (0, 0, 255), (10, 10), 10)
    bom_img.set_colorkey((0, 0, 0))
    bom_rct = bom_img.get_rect()
    r_w = ran.randint(0, WIDTH)
    r_h = ran.randint(0, HEIGHT)
    bom_rct.center = (r_w, r_h)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            

        if kk_rct.colliderect(bd_rct):#ぶつかったらTrue
            kk_img2 = pg.image.load("ex02/fig/9.png")
            screen.blit(kk_img2, kk_rct)

            return  
     



        screen.blit(bg_img, [0, 0])
        """こうかとん"""
        key_lst = pg.key.get_pressed()#すべてのキーの押下状態を取得する
        sum_mv = [0,0]
        for key, mv in delta.items():
            if key_lst[key] :#keyが押されていたら
                sum_mv[0] += mv[0] #横方向の合計移動量
                sum_mv[1] += mv[1] #縦方向の合計移動量
        kk_img = muki[tuple(sum_mv)]
        kk_rct.move_ip(sum_mv[0],sum_mv[1])

  

        if check_bound(kk_rct) != (True,True):#画面外に出ないように制限
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])

        screen.blit(kk_img,kk_rct)

        screen.blit(bom_img, [r_w, r_h])


        """ばくだん"""
        bd_rct.move_ip(vx,vy) #練習2　爆弾を移動させる
        yoko, tate = check_bound(bd_rct)
        if not yoko: #横方向にはみ出したら
            vx *= -1
        if not tate: #縦方向にはみ出したら
            vy *= -1

        screen.blit(bd_img,bd_rct)#練習1　Rectを使って試しにblit
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()