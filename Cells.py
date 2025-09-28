#First game being made with Atalia
#Late into prgraming I thoguht of a cell royale where diferent cells would be classes with different ablities :(
#See Atalia for Ideas.
#A game where you play as different cells in different minigames.
#Each game state for each game (and whats shown in it)
#0  Title Screen - 
#1  Selection screen
#2 Red blood cells - Racing 
#3  White cells - Invasion
#Brain is guide
#Bugs:
#1  Enemy spawner only showing when enemy spawns - We were drawing it in the list lol.
#2  Projector not having right dimensions - 
#3  Whole screen red if we spend too long in Red cell Rush then invasion -  Reset?
#To Do:
#1  Fix code



import pygame as pg
import sys
import random
import Settings as Set
from pygame.locals import QUIT


FPS = 60
WIN = 500

pg.init()
pg.font.init()
pg.mixer.init()
#allows for multiple sfx to be played at the same time but we can only do this 10 times as des
pg.mixer.set_num_channels(10)
scrn = pg.display.set_mode((WIN*2, WIN))
pg.display.set_caption('Cells!')


clock = pg.time.Clock()
scrn_width = scrn.get_width()
scrn_height = scrn.get_height()
font_t = pg.font.SysFont("Arial",90)
font_st = pg.font.SysFont("Arial",40)
font_s = pg.font.SysFont("Arial",30)

def title_screen(title_y,prcr,start_but,sbut_hover):
    pg.draw.rect(scrn,"white",prcr)
    #Tile
    title_text = font_t.render("CELLS!",1,"black")
    scrn.blit(title_text,(scrn_width/2 - title_text.get_width()/2,title_y + title_text.get_height()))
    sub_title = font_st.render("BattleForTheBody(Demo)",1,"black")
    scrn.blit(sub_title,(scrn_width/2 - sub_title.get_width()/2,title_y + title_text.get_height() + 90))
    prcr.y = title_y 
    start_but.y = title_y + 320
    #Buttons
    if (sbut_hover == True):
        pg.draw.rect(scrn,"gray",start_but)
        pg.draw.rect(scrn,"black",start_but,5)
    pg.draw.rect(scrn,"black",start_but,5)
    # start button words
    st_title = font_st.render("Start",1,"black")
    scrn.blit(st_title, (start_but.x + start_but.width/2 - st_title.get_width()/2,start_but.y + start_but.height/2 - st_title.get_height()/2))


def brain_guide():
    pass


def enemy_update(enemies,prcr,e_spawn,walls,game_sate):
    #Spawner
    if (game_sate == 2):
        pg.draw.rect(scrn,"darkred",e_spawn)
    if (game_sate == 3):
        pg.draw.rect(scrn,"red",e_spawn)
    #Enemies
    for e in enemies:
        if (game_sate == 2):
            pg.draw.rect(scrn,"yellow",e)
        if (game_sate == 3):
            pg.draw.rect(scrn,"green",e)


def bones_update(bones,prcr,enemies):
    for b in bones:
        # update look
        pg.draw.rect(scrn,"white",b)
        pg.draw.rect(scrn,"white",(b.x - 10,b.y,b.width + 20,10))
        pg.draw.rect(scrn,"white",(b.x - 10,b.y + b.height,b.width + 20,10))
        b.y -= 7
        if (b.y + b.height < prcr.y):
            bones.remove(b) 
        for e in enemies:
            if (b.colliderect(e)):
                bones.remove(b) 
                enemies.remove(e) 


def player_update(prcr,player,ivb,oxygen,game_state):
    #Player
    # hit
    if (ivb == True):
        pg.draw.rect(scrn,"white",player)
    else:
        pg.draw.rect(scrn,Set.player_col[game_state],player)
    if (game_state == 2):
        #Oxygen
        for ox in oxygen:
            # update x value
            ox.x = player.x + oxygen.index(ox) * 10 + 10
            pg.draw.rect(scrn,"lightblue",ox)


def walls_update(walls):
    for wall in walls:
        pg.draw.rect(scrn,(150,0,0),wall)
        #outline
        pg.draw.rect(scrn,(150,0,50),wall,10) 


def time_update(game_state,prcr,time,time_rect,time_rect_out):
    if (game_state == 2):
        pg.draw.rect(scrn,"white",time_rect)
        #outline
        pg.draw.rect(scrn,"black",time_rect_out,5)
    if (game_state == 3):
        time_text = font_s.render(f"Time: {time}",1,"white")
        scrn.blit(time_text, (prcr.x + prcr.width/2 - time_text.get_width()/2,prcr.y + 100))


def selection_screen(prcr,info_box,cur_mg,r_but,i_but,d_but):
    pg.draw.rect(scrn,"white",prcr)
    #body image
    body = pg.transform.scale(pg.image.load('body.jpg').convert_alpha(),(270,750))
    body = pg.transform.rotate(body, 270)
    scrn.blit(body,(info_box.x + 50,prcr.y + 70))
    #Buttons
    pg.draw.rect(scrn,"red",r_but)
    pg.draw.rect(scrn,"green",d_but)
    pg.draw.rect(scrn,"gray",i_but)
    #Info Box
    pg.draw.rect(scrn,"black",info_box)
    # brain guide
    # free select
    if (cur_mg == 0):
        ph_text1 = font_s.render(Set.info_words[0],1,"white")
        scrn.blit(ph_text1, (prcr.x,info_box.y))
        ph_text2 = font_s.render(Set.info_words[1],1,"white")
        scrn.blit(ph_text2, (prcr.x,info_box.y + ph_text1.get_height() + 10))
    if (cur_mg == 1):
        r_text1 = font_s.render(Set.info_words[2],1,"red")
        scrn.blit(r_text1, (prcr.x,info_box.y))
        r_text2 = font_s.render(Set.info_words[3],1,"white")
        scrn.blit(r_text2, (prcr.x,info_box.y + r_text1.get_height() + 10))
        r_text3 = font_s.render(Set.info_words[4],1,"white")
        scrn.blit(r_text3, (prcr.x,info_box.y + r_text2.get_height() + r_text3.get_height() + 10))
        r_text4 = font_s.render(Set.info_words[5],1,"white")
        scrn.blit(r_text4, (prcr.x,info_box.y + r_text2.get_height() + r_text3.get_height() + r_text4.get_height() + 10))
    if (cur_mg == 2):    
        i_text1 = font_s.render(Set.info_words[6],1,"gray")
        scrn.blit(i_text1, (prcr.x,info_box.y))
        i_text2 = font_s.render(Set.info_words[7],1,"white")
        scrn.blit(i_text2, (prcr.x,info_box.y + i_text1.get_height() + 10))
        i_text3 = font_s.render(Set.info_words[8],1,"white")
        scrn.blit(i_text3, (prcr.x,info_box.y + i_text2.get_height() + i_text3.get_height() + 10))
        i_text4 = font_s.render(Set.info_words[9],1,"white")
        scrn.blit(i_text4, (prcr.x,info_box.y + i_text2.get_height() + i_text3.get_height() + i_text4.get_height() + 10))
        i_text5 = font_s.render(Set.info_words[10],1,"white")
        scrn.blit(i_text5, (prcr.x,info_box.y + i_text2.get_height() + i_text3.get_height() + i_text4.get_height() + i_text5.get_height() + 10))


def draw(game_state,prcr,title_y,start_but,sbut_hover,
         info_box,cur_mg,r_but,i_but,d_but,
         time,time_rect,time_rect_out,enemies,e_spawn,player,ivb,oxygen,bones,lives,walls):
    #Backend
    scrn.fill("darkgreen")
    pg.draw.rect(scrn,"brown",(0,0,scrn_width,scrn_height),5)
    if (game_state == 0):
        #Title
        title_screen(title_y,prcr,start_but,sbut_hover)
    if (game_state == 1):
        selection_screen(prcr,info_box,cur_mg,r_but,i_but,d_but)
    if (game_state == 2):
        #Bkgrnd
        pg.draw.rect(scrn,"darkred",prcr)
        #Entities
        enemy_update(enemies,prcr,e_spawn,walls,game_state)
        player_update(prcr,player,ivb,oxygen,game_state)
        walls_update(walls)
    if (game_state == 3):
        #Bkgrnd
        pg.draw.rect(scrn,"tan",prcr)
        #Entities
        enemy_update(enemies,prcr,e_spawn,walls,game_state)
        player_update(prcr,player,ivb,oxygen,game_state)
        bones_update(bones,prcr,enemies)
        #Infection Line (aka the lose game)
        pg.draw.line(scrn,"red",(prcr.x,prcr.y + prcr.height/2),(prcr.x + prcr.width + 10, prcr.y + prcr.height/2))
    #Multiple gamestates
    if (game_state > 1):
        time_update(game_state,prcr,time,time_rect,time_rect_out)
        pg.draw.rect(scrn,"darkgreen",(0,scrn_height-50,scrn_width,scrn_height)) #This rect was made to make it that whenver someting goes off screen more cleaner
    pg.display.flip()


def main():
    #Setup
    game_state = 0
    #Title screen
    title_y = -200
    title_y_vel = 20
    prcr = pg.Rect(scrn_width/2 - 400,title_y,800,500)
    # buttons
    start_but = pg.Rect(prcr.x + prcr.width/2 - 100, prcr.bottom - 10,200,100)
    sbut_hover = False
    #cells
    #Select screen
    info_box = pg.Rect(prcr.x,300, prcr.width, 170)
    cur_mg = 0
    # minigame buttons
    r_but = pg.Rect(prcr.x + 550,135,50,50)
    i_but = pg.Rect(prcr.x + 360,prcr.y + prcr.height/2 + 15, 200,60)
    d_but = pg.Rect(prcr.x + 425,140,70,50)
    #Enemies
    enemies = []
    enemy_cc = 0
    enemy_add_inc = 160
    e_spawn = pg.Rect(prcr.x,0,prcr.width,50)
    # vars
    e_vel = 1
    e_min_size = 20
    ev_add_inc = 700
    ev_cc = 0
    # walls
    walls = []
    wall_1 = pg.Rect(prcr.x,prcr.y,250,650)
    walls.append(wall_1)
    wall_2 = pg.Rect(prcr.x + 600,prcr.y,200,650)
    walls.append(wall_2)
    #Player
    lives = 3
    player = pg.Rect(prcr.x + prcr.width/2 - 80,prcr.y + prcr.height,70,70)
    p_vel = 4
    #Timer system
    time = 30
    time_add_inc = 100
    time_dc = 0
    # Red Cell Rush
    # oxygen
    oxygen = []
    for i in range(3):
        ox = pg.Rect(player.x + (i*10) + 10,player.y + player.height/2 - 10,20,20)
        oxygen.append(ox)
    # iframes
    ivb = False
    ivb_add_inc = 150
    ivb_cc = 0
    # Intugemary Invasion
    # bones
    bone_add_inc = 50
    bone_cc = 0
    bones = []
    bone = pg.Rect(0,0,15,50)
    # Downward Digestion
    #  
    time_rect = pg.Rect(walls[1].x + walls[1].width/2, walls[1].y + walls[1].height - 100, 40, 50)
    time_rect_out = pg.Rect(time_rect.x,100,time_rect.width,300)
    # wall moving
    wall_x = 0
    wx_add_inc = 200
    wx_cc = 0
    w_moving = False
    while True:
        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pos()
        #Game
        #Opening animation
        if (keys[pg.K_SPACE]):
            time_rect.y = time_rect_out.y + 5
        if (game_state == 0):
            if (title_y + prcr.y + prcr.height < scrn_height - 100):
                title_y += title_y_vel
                if (title_y_vel >= 2):
                    title_y_vel -= 1
            #Buttons
            if (start_but.collidepoint(mouse)):
                sbut_hover = True
                if (pg.mouse.get_pressed()[0]):
                    game_state = 1
            else:
                sbut_hover = False
        #Selection Screen (rarely use 'elif' but i do love em :)
        if (game_state == 1):
            # Hover
            if (r_but.collidepoint(mouse)):
                cur_mg = 1
                if (pg.mouse.get_pressed()[0]):
                    game_state = 2
            elif (i_but.collidepoint(mouse)):
                cur_mg = 2
                if (pg.mouse.get_pressed()[0]):
                    game_state = 3
            elif (d_but.collidepoint(mouse)):
                cur_mg = 3
            else:
                cur_mg = 0
            # Reset
            e_spawn.height = 50
            time_rect = pg.Rect(walls[1].x + walls[1].width/2, walls[1].y + walls[1].height - 100, 40, 50)
            time_rect_out = pg.Rect(time_rect.x,100,time_rect.width,300)
            player.x = walls[0].x + walls[0].width + 50
        
        #Red Cell Rush
        if (game_state == 2):
            #Timer
            time_dc += 1
            if (time_dc >= time_add_inc):
                time_rect.y -= 5
                time_rect.height += 5
                time_dc = 0 
            #Move wall back and forth
            if (w_moving == False):
                #if (walls[0].x != wall_x):
                    wx_cc += 1
                    if (wx_cc >= wx_add_inc):
                        wall_x = random.randint(prcr.x + 100, prcr.x + 400)
                        wx_cc = 0
                        w_moving = True
            if (w_moving == True):
                if (walls[0].x + walls[0].width < wall_x):
                    walls[0].width += 1
                if (walls[0].x + walls[0].width > wall_x):
                    walls[0].width -= 1
                if (walls[0].x + walls[0].width == wall_x):
                    w_moving = False
                # touching player
                if (player.colliderect(walls[0])):
                    if (player.x <= walls[0].x + walls[0].width):
                        player.x += p_vel
            #Spawn enemies
            e_vel = 3
            # Set spawn
            e_spawn.x = walls[0].x + walls[0].width
            e_spawn.width = walls[1].x - (walls[0].x + walls[0].width)
            e_spawn.height = 1
            enemy_cc += 1
            if (enemy_cc >= enemy_add_inc):
                enemy = pg.Rect(random.randint(e_spawn.x, e_spawn.x + e_spawn.width - 80), e_spawn.y + e_spawn.height,random.randint(e_min_size,90),50)
                enemies.append(enemy)
                enemy_cc = 0
            # enemy win
            for enemy in enemies:
                # enemy min size change
                if (e_min_size <= 60):
                    ev_cc += 1
                    if (ev_cc >= ev_add_inc):
                        e_min_size += 20
                        ev_cc = 0
                enemy.y += e_vel
                if (enemy.colliderect(player)):
                    if (ivb == False):
                        del oxygen[-1] # delete last item in list
                        lives -= 1
                    ivb = True
                    enemies.remove(enemy)
            #Lose 
            if (lives == 0):
                game_state = 1
                lives = 3
                # reset
                ivb = False
                time = 30
                ivb_cc = 0
                e_min_size = 20
                ev_cc = 0
                enemy_cc = 0
                while (len(oxygen) < 3):
                    ox = pg.Rect(player.x + (i*10) + 10,player.y + player.height/2 - 10,20,20)
                    oxygen.append(ox)
            #Win
            if (time_rect.y <= time_rect_out.y):
                game_state = 1
                lives = 3
                # reset
                ivb = False
                time = 30
                ivb_cc = 0
                e_min_size = 20
                ev_cc = 0
                enemy_cc = 0
                while (len(oxygen) < 3):
                    ox = pg.Rect(player.x + (i*10) + 10,player.y + player.height/2 - 10,20,20)
                    oxygen.append(ox)

            #Invincible frames
            if(ivb == True):
                ivb_cc += 1
                if (ivb_cc >= ivb_add_inc):
                    ivb = False
                    ivb_cc = 0
            #Player
            player.y = 300
            # move
            if (keys[pg.K_a] and player.x > wall_1.x + wall_1.width):
                player.x -= p_vel
            if (keys[pg.K_d] and player.x + player.width < wall_2.x):
                player.x += p_vel
        
        #Intugemary Invasion
        if (game_state == 3):
            #Timer
            time_dc += 1
            if (time_dc >= time_add_inc):
                time -= 1
                time_dc = 0 
            #Spawn enemies
            e_spawn.x = prcr.x 
            e_spawn.width = prcr.width
            enemy_cc += 1
            if (enemy_cc >= enemy_add_inc):
                enemy = pg.Rect(random.randint(prcr.x,prcr.x + prcr.width - 100), e_spawn.y + e_spawn.height,50,50)
                enemies.append(enemy)
                enemy_cc = 0
            # enemy win
            for enemy in enemies:
                # enemy speed change
                if (e_vel <= 4):
                    ev_cc += 1
                    if (ev_cc >= ev_add_inc):
                        e_vel += 1
                        ev_cc = 0
                enemy.y += e_vel
                if (enemy.y > prcr.y + prcr.height):
                    e_spawn.height += 50
                    lives -= 1
                    enemies.remove(enemy)
            #Lose 
            if (lives == -1):
                time = 30
                game_state = 1
                e_spawn.x = prcr.x 
                e_spawn.width = prcr.width
                lives = 3
                bone_cc = 0
                e_vel = 2
                enemy_cc = 0

            #Win 
            if (time <= 0):
                time = 30
                game_state = 1
                e_spawn.x = prcr.x 
                e_spawn.width = prcr.width
                lives = 3
                bone_cc = 0
                e_vel = 2
                enemy_cc = 0

            #Player
            player.y = prcr.y + prcr.height - 80
            # move
            if (keys[pg.K_a] and player.x > prcr.x):
                player.x -= p_vel
            if (keys[pg.K_d] and player.x + player.width < prcr.x + prcr.width):
                player.x += p_vel
            # shoot
            if (keys[pg.K_SPACE]):
                if (bone_cc <= 0):
                    bone = pg.Rect(player.x + player.width/2 - bone.width/2, player.y,bone.width,bone.height)
                    bones.append(bone)
                    bone_cc = bone_add_inc
            if (bone_cc >= 0):
                bone_cc -= 1
           


        #Close window 
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
        if keys[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()
        clock.tick(FPS)
        draw(game_state,prcr,title_y,start_but,sbut_hover,
             info_box,cur_mg,r_but,i_but,d_but,
             time,time_rect,time_rect_out,enemies,e_spawn,player,ivb,oxygen,bones,lives,walls)

if __name__ == "__main__":
    main()
