import pygame
import time
pygame.init()
pygame.mixer.init()
from stockfish import Stockfish
stockfish = Stockfish(path="stockfish") 
# Or use path="/usr/bin/stockfish" if the above doesn't work
stockfish.set_skill_level(20)
WIDTH = 1440
HEIGHT = 830
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
font = pygame.font.SysFont(None,25)
pygame.display.set_caption("Chess game")
take_sound = pygame.mixer.Sound("capture.mp3")
check_sound = pygame.mixer.Sound("move-check.mp3")
move_sound = pygame.mixer.Sound("move-self.mp3")
promote_sound = pygame.mixer.Sound("promote.mp3")
blackpieces = ['rook','knight','bishop','queen','king','bishop','knight','rook',
               'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn']
blackpieces_loc = [(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),
                   (2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),(9,2)]
whitepieces = ['pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn',
               'rook','knight','bishop','queen','king','bishop','knight','rook']
whitepieces_loc = [(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),(9,7),
                   (2,8),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8),(9,8)]
whites_caught_pieces = []
blacks_caught_pieces = []
#white pieces
w_rook_img = pygame.image.load("White-Rook.png")
w_rook_img_s = pygame.transform.scale(w_rook_img,(40,40))
w_rook_img_s.convert()
w_rook_img.convert()
w_knight_img = pygame.image.load("White-Knight.png")
w_knight_img_s = pygame.transform.scale(w_knight_img,(40,40))
w_knight_img_s.convert()
w_knight_img.convert()
w_bishop_img = pygame.image.load("White-Bishop.png")
w_bishop_img_s = pygame.transform.scale(w_bishop_img,(40,40))
w_bishop_img_s.convert()
w_bishop_img.convert()
w_pawn_img = pygame.image.load("White-Pawn.png")
w_pawn_img_s = pygame.transform.scale(w_pawn_img,(40,40))
w_pawn_img_s.convert()
w_pawn_img.convert()
w_queen_img = pygame.image.load("White-Queen.png")
w_queen_img_s = pygame.transform.scale(w_queen_img,(40,40))
w_queen_img_s.convert()
w_queen_img.convert()
w_king_img = pygame.image.load("White-King.png")
w_king_img_s = pygame.transform.scale(w_king_img,(40,40))
w_king_img_s.convert()
w_king_img.convert()
#black pieces
b_rook_img = pygame.image.load("Black-Rook.png")
b_rook_img_s = pygame.transform.scale(b_rook_img,(40,40))
b_rook_img_s.convert()
b_rook_img.convert()
b_knight_img = pygame.image.load("Black-Knight.png")
b_knight_img_s = pygame.transform.scale(b_knight_img,(40,40))
b_knight_img_s.convert()
b_knight_img.convert()
b_bishop_img = pygame.image.load("Black-Bishop.png")
b_bishop_img_s = pygame.transform.scale(b_bishop_img,(40,40))
b_bishop_img.convert()
b_bishop_img.convert()
b_pawn_img = pygame.image.load("Black-Pawn.png")
b_pawn_img_s = pygame.transform.scale(b_pawn_img,(40,40))
b_pawn_img_s.convert()
b_pawn_img.convert()
b_queen_img = pygame.image.load("Black-Queen.png")
b_queen_img_s = pygame.transform.scale(b_queen_img,(40,40))
b_queen_img_s.convert()
b_queen_img.convert()
b_king_img = pygame.image.load("Black-King.png")
b_king_img_s = pygame.transform.scale(b_king_img,(40,40))
b_king_img_s.convert()
b_king_img.convert()
w_img_list = [w_pawn_img,w_bishop_img,w_knight_img,w_rook_img,w_queen_img,w_king_img]
b_img_list = [b_pawn_img,b_bishop_img,b_knight_img,b_rook_img,b_queen_img,b_king_img]
pieces_list=['pawn','bishop','knight','rook','queen','king']
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 40
buttons = {
    "Player V Player": pygame.Rect(750, 350, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Player V CPU": pygame.Rect(1000, 350, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Start": pygame.Rect(920, 450, 100, 40)
}
fps = 10
white = (255,255,255)
light_brown = (240, 217, 181)
brown = (181, 136, 99)
black = (0,0,0)
red = (255,0,0)
grey = (184,184,184)
dark_grey = (100, 100, 100)
green = (0, 200, 0)
def chesBoard(): 
    for i in range(64):  
        column = i % 8  
        row = i // 8 
        x = column * 60 + 120
        y = row * 60 + 60
        sqr = [x,y,60,60]
        if (row + column) % 2 == 0:
            pygame.draw.rect(screen,light_brown,sqr)
        else:
            pygame.draw.rect(screen,brown,sqr)
    for y in range(0, 480, 60):
        for x in range(0, 480, 60):
            pygame.draw.rect(screen, black, (120 + x, 60 + y, 60, 60), 1)
    pygame.draw.rect(screen, black, (120, 60, 480, 480), 2)
def chess_board_cords():
    r1 = font.render("a",True,black)
    screen.blit(r1,(145,540))
    r2 = font.render("b",True,black)
    screen.blit(r2,(205,540))
    r3 = font.render("c",True,black)
    screen.blit(r3,(265,540))
    r4 = font.render("d",True,black)
    screen.blit(r4,(325,540))
    r5 = font.render("e",True,black)
    screen.blit(r5,(385,540))
    r6 = font.render("f",True,black)
    screen.blit(r6,(445,540))
    r7 = font.render("g",True,black)
    screen.blit(r7,(505,540))
    r8 = font.render("h",True,black)
    screen.blit(r8,(565,540))
    c1 = font.render("1",True,black)
    c2 = font.render("2",True,black)
    c3 = font.render("3",True,black)
    c4 = font.render("4",True,black)
    c5 = font.render("5",True,black)
    c6 = font.render("6",True,black)
    c7 = font.render("7",True,black)
    c8 = font.render("8",True,black)
    screen.blit(c1,(100,500))
    screen.blit(c2,(100,440))
    screen.blit(c3,(100,380))
    screen.blit(c4,(100,320))
    screen.blit(c5,(100,260))
    screen.blit(c6,(100,200))
    screen.blit(c7,(100,140))
    screen.blit(c8,(100,80))
def piecesdraw():
    for x in range(len(blackpieces)):#16
        for i in range(6):
            if blackpieces[x] == None :
                """"""
            elif blackpieces[x] == pieces_list[i] :
                rect = b_img_list[i].get_rect()
                x_locs = blackpieces_loc[x][0]
                y_locs = blackpieces_loc[x][1]
                x_locs *= 60
                y_locs *= 60
                rect = (x_locs,y_locs,60,60)
                screen.blit(b_img_list[i],rect)
                break
    for x in range(len(whitepieces)):#16
        for i in range(6):
            if whitepieces[x] == None :
                """"""
            elif whitepieces[x] == pieces_list[i] :
                rect = w_img_list[i].get_rect()
                x_locs = whitepieces_loc[x][0]
                y_locs = whitepieces_loc[x][1]
                x_locs *= 60
                y_locs *= 60
                rect = (x_locs,y_locs,60,60)
                screen.blit(w_img_list[i],rect)
                break
def draw_possible_moves(moves):
    for move in moves:
        x, y = move
        pygame.draw.circle(screen,white, (x * 60 + 30, y * 60 + 30), 20, 10)
        pygame.draw.circle(screen,black, (x * 60 + 30, y * 60 + 30), 20, 4)
        pygame.draw.circle(screen,black, (x * 60 + 30, y * 60 + 30), 12, 4)
def stepsdisplayer(sc_val): 
    if sc_val%2 == 0 and sc_val != 0 :
        img = font.render(f"Move {sc_val} : Blacks turn ",True,black)
    else:
        img = font.render(f"Move {sc_val} : Whites turn ",True,black)
    return img
def points_of_material():
    img1 = font.render("CAPTURED WHITE PIECES",True,black)
    img2 = font.render("CAPTURED BLACK PIECES",True,black)
    pygame.draw.rect(screen, light_brown, (960, 120, 330, 40))
    pygame.draw.rect(screen, light_brown, (960, 200, 330, 40))
    pygame.draw.rect(screen, light_brown, (960, 280, 330, 40))  
    pygame.draw.rect(screen, brown, (960, 80, 330, 40))
    pygame.draw.rect(screen, brown, (960, 160, 330, 40))
    pygame.draw.rect(screen, brown, (960, 240, 330, 40))  
    pygame.draw.rect(screen, grey, (960, 40, 330, 40))
    pygame.draw.rect(screen, black, (960, 80, 330, 3))
    pygame.draw.rect(screen, black, (960, 120, 330, 3))
    pygame.draw.rect(screen, black, (960, 160, 330, 3))
    pygame.draw.rect(screen, black, (960, 200, 330, 3))
    pygame.draw.rect(screen, black, (960, 240, 330, 3))
    pygame.draw.rect(screen, black, (960, 280, 330, 3))
    pygame.draw.rect(screen, grey, (960, 340, 330, 40)) 
    pygame.draw.rect(screen, brown, (960, 380, 330, 40))
    pygame.draw.rect(screen, brown, (960, 460, 330, 40))
    pygame.draw.rect(screen, brown, (960, 540, 330, 40))
    pygame.draw.rect(screen, light_brown, (960,420, 330, 40))
    pygame.draw.rect(screen, light_brown, (960,500, 330, 40))
    pygame.draw.rect(screen, light_brown, (960,580, 330, 40))
    pygame.draw.rect(screen, black, (960, 380, 330, 3))
    pygame.draw.rect(screen, black, (960, 420, 330, 3))
    pygame.draw.rect(screen, black, (960, 460, 330, 3))
    pygame.draw.rect(screen, black, (960, 500, 330, 3))
    pygame.draw.rect(screen, black, (960, 540, 330, 3))
    pygame.draw.rect(screen, black, (960, 580, 330, 3))
    screen.blit(img2,(1000,350))
    screen.blit(img1,(1000,50))
    pygame.draw.rect(screen,black,(960,40,330,280),3)
    pygame.draw.rect(screen,black,(960,340,330,280),3)
def material_caught():
    p_val2,r_val2,b_val2,k_val2,q_val2,ki_val2 = 24,24,24,24,24,24
    for x in whites_caught_pieces:
        if x == 'pawn':
            screen.blit(w_pawn_img_s,(40*p_val2,80))
            p_val2 = p_val2 + 1
        elif x == 'knight':
            screen.blit(w_knight_img_s,(40*k_val2,120))
            k_val2 = k_val2 + 1
        elif x == 'bishop':
            screen.blit(w_bishop_img_s,(40*b_val2,160))
            b_val2 = b_val2 + 1
        elif x == 'rook':
            screen.blit(w_rook_img_s,(40*r_val2,200))
            r_val2 = r_val2 + 1
        elif x == 'queen':
            screen.blit(w_queen_img_s,(40*q_val2,240))
            q_val2 = q_val2 + 1
        elif x == 'king':
            screen.blit(w_king_img_s,(40*ki_val2 ,280))
            ki_val2 = ki_val2 + 1
    p_val2,r_val2,b_val2,k_val2,q_val2,ki_val2 = 24,24,24,24,24,24
    for x in blacks_caught_pieces:
        if x == 'pawn':
            screen.blit(b_pawn_img_s,(40*p_val2,380))
            p_val2 = p_val2 + 1
        elif x == 'knight':
            screen.blit(b_knight_img_s,(40*k_val2,420))
            k_val2 = k_val2 + 1
        elif x == 'bishop':
            screen.blit(b_bishop_img_s,(40*b_val2,460))
            b_val2 = b_val2 + 1
        elif x == 'rook':
            screen.blit(b_rook_img_s,(40*r_val2,500))
            r_val2 = r_val2 + 1
        elif x == 'queen':
            screen.blit(b_queen_img_s,(40*q_val2,540))
            q_val2 = q_val2 + 1
        elif x == 'king':
            screen.blit(b_king_img_s,(40*ki_val2 ,580))
            ki_val2 = ki_val2 + 1
def checklocs(clicked_loc):
    if clicked_loc in blackpieces_loc:
        return 0
    elif clicked_loc in whitepieces_loc:
        return 1
    else:
        return None
def check_locks_valid(val,old_locks,new_locks):
    x,y = new_locks
    if not (2 <= x <= 9 and 1 <= y <= 8):
        return False
    if new_locks == old_locks :
        return False
    elif val == 1 and new_locks in whitepieces_loc:
        return False
    elif val == 0 and new_locks in blackpieces_loc:
        return False
    else:
        return True
def locks_changer(pre_locks, new_locks, sc_val):
    global minutes1, second1,minutes2,second2,timer1,timer2,last_time,run1,run2,blacks_caught_pieces, whites_caught_pieces, moved
    cap_chk = False
    run = True
    if sc_val % 2 == 0:
        index_forplace = blackpieces_loc.index(pre_locks)
        if new_locks in whitepieces_loc:
            index_forremove = whitepieces_loc.index(new_locks)
            whites_caught_pieces.append(whitepieces[index_forremove])
            whitepieces[index_forremove] = None
            whitepieces_loc[index_forremove] = (0, 0)
            cap_chk = True
        blackpieces_loc[index_forplace] = new_locks
        moved = True
        if blackpieces[index_forplace] == 'pawn' and blackpieces_loc[index_forplace][1] == 8:
            while run:
                screen.fill(white)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_k:
                            blackpieces[index_forplace] = 'knight'
                            run = False
                            cap_chk = False
                            if run1:
                                run1 = False
                                run2 = True
                                last_time = time.time()
                            elif run2:
                                run2 = False
                                run1 = True
                                last_time = time.time()
                            promote_sound.play()
                            moved = False
                            break
                        elif event.key == pygame.K_b:
                            blackpieces[index_forplace] = 'bishop'
                            run = False
                            cap_chk = False
                            if run1:
                                run1 = False
                                run2 = True
                                last_time = time.time()
                            elif run2:
                                run2 = False
                                run1 = True
                                last_time = time.time()
                            promote_sound.play()
                            moved = False
                            break
                        elif event.key == pygame.K_r:
                            blackpieces[index_forplace] = 'rook'
                            run = False
                            cap_chk = False
                            if run1:
                                run1 = False
                                run2 = True
                                last_time = time.time()
                            elif run2:
                                run2 = False
                                run1 = True
                                last_time = time.time()
                            promote_sound.play()
                            moved = False
                            break
                        elif event.key == pygame.K_q:
                            blackpieces[index_forplace] = 'queen'
                            run = False
                            cap_chk = False
                            if run1:
                                run1 = False
                                run2 = True
                                last_time = time.time()
                            elif run2:
                                run2 = False
                                run1 = True
                                last_time = time.time()
                            promote_sound.play()
                            moved = False
                            break
                imger = stepsdisplayer(steps_counter_value)
                screen.blit(imger, (250, 590))
                if run1:
                    elapsed_time = time.time() - last_time
                    timer1 -= elapsed_time
                    last_time = time.time()
                if run2:
                    elapsed_time = time.time() - last_time
                    timer2 -= elapsed_time
                    last_time = time.time()
                time_func()
                points_of_material()
                display_option_b()
                chesBoard()
                piecesdraw()
                chess_board_cords()
                material_caught()
                pygame.display.flip()
        if cap_chk == True:
            take_sound.play()
        elif moved == True:
            move_sound.play()
    elif sc_val % 2 == 1:
        index_forplace = whitepieces_loc.index(pre_locks)
        if new_locks in blackpieces_loc:
            index_forremove = blackpieces_loc.index(new_locks)
            blacks_caught_pieces.append(blackpieces[index_forremove])
            blackpieces[index_forremove] = None
            blackpieces_loc[index_forremove] = (0, 0)
            cap_chk = True
        whitepieces_loc[index_forplace] = new_locks
        moved = True
        if whitepieces[index_forplace] == 'pawn' and whitepieces_loc[index_forplace][1] == 1:
            while run:
                screen.fill(white)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_k:
                            whitepieces[index_forplace] = 'knight'
                            run = False
                            promote_sound.play()
                            if run1:
                                run1 = False
                                run2 = True
                                last_time = time.time()
                            elif run2:
                                run2 = False
                                run1 = True
                                last_time = time.time()
                            cap_chk = False
                            moved = False
                            break
                        elif event.key == pygame.K_b:
                            whitepieces[index_forplace] = 'bishop'
                            run = False
                            cap_chk = False
                            promote_sound.play()
                            if run1:
                                run1 = False
                                run2 = True
                                last_time = time.time()
                            elif run2:
                                run2 = False
                                run1 = True
                                last_time = time.time()
                            moved = False
                            break
                        elif event.key == pygame.K_r:
                            whitepieces[index_forplace] = 'rook'
                            run = False
                            cap_chk = False
                            promote_sound.play()
                            if run1:
                                run1 = False
                                run2 = True
                                last_time = time.time()
                            elif run2:
                                run2 = False
                                run1 = True
                                last_time = time.time()
                            moved = False
                            break
                        elif event.key == pygame.K_q:
                            whitepieces[index_forplace] = 'queen'
                            run = False
                            cap_chk = False
                            promote_sound.play()
                            if run1:
                                run1 = False
                                run2 = True
                                last_time = time.time()
                            elif run2:
                                run2 = False
                                run1 = True
                                last_time = time.time()
                            moved = False
                            break
                imger = stepsdisplayer(steps_counter_value)
                screen.blit(imger, (250, 590))
                if run1:
                    elapsed_time = time.time() - last_time
                    timer1 -= elapsed_time
                    last_time = time.time()
                if run2:
                    elapsed_time = time.time() - last_time
                    timer2 -= elapsed_time
                    last_time = time.time()
                time_func()
                points_of_material()
                chesBoard()
                piecesdraw()
                chess_board_cords()
                display_option_w()
                material_caught()
                pygame.display.flip()
        if cap_chk == True:
            take_sound.play()
        elif moved == True:
            move_sound.play()
def display_option_b():
    pygame.draw.rect(screen,brown,(115,625,620,40))
    pygame.draw.rect(screen,light_brown,(115,665,620,40))
    pygame.draw.rect(screen,black,(115,665,620,2))
    text = font.render("PROMOTE THE BLACK PAWN TO ? (Press the following keys)",True,black)
    screen.blit(text,(125,640))
    text2 = font.render("K = knight",True,black)
    screen.blit(text2,(125,670))
    text3 = font.render("B = bihsop",True,black)
    screen.blit(text3,(235,670))
    text4 = font.render("R = rook",True,black)
    screen.blit(text4,(350,670))
    text5 = font.render("Q = queen",True,black)
    screen.blit(text5,(440,670))
    pygame.draw.rect(screen,black,(115,625,620,80),2)
def display_option_w():
    pygame.draw.rect(screen,brown,(115,625,620,40))
    pygame.draw.rect(screen,light_brown,(115,665,620,40))
    pygame.draw.rect(screen,black,(115,665,620,2))
    text = font.render("PROMOTE THE WHITE PAWN TO ? (Press the following keys)",True,black)
    screen.blit(text,(125,640))
    text2 = font.render("K = knight",True,black)
    screen.blit(text2,(125,670))
    text3 = font.render("B = bihsop",True,black)
    screen.blit(text3,(235,670))
    text4 = font.render("R = rook",True,black)
    screen.blit(text4,(350,670))
    text5 = font.render("Q = queen",True,black)
    screen.blit(text5,(440,670))
    pygame.draw.rect(screen,black,(115,625,620,80),2)
def which_piece_check(locs_):
    if locs_ in whitepieces_loc:
        index = whitepieces_loc.index(locs_)
        return whitepieces[index]
    elif locs_ in blackpieces_loc:
        index = blackpieces_loc.index(locs_)
        return blackpieces[index]
def pawn_moves_list(color_,locs):
    p_move = []
    if color_ == 1 :
        if locs[1] == 7:
            if (locs[0],locs[1]-1) not in blackpieces_loc and ((locs[0],locs[1]-1) not in whitepieces_loc or (locs[0],locs[1]-2) not in blackpieces_loc):
                p_move.append((locs[0],locs[1]-1))
                p_move.append((locs[0],locs[1]-2))
        else:
            if (locs[0],locs[1]-1) not in blackpieces_loc:    
                p_move.append((locs[0],locs[1]-1))
        if (locs[0]-1,locs[1]-1) in blackpieces_loc:
            p_move.append((locs[0]-1,locs[1]-1))
        if (locs[0]+1,locs[1]-1) in blackpieces_loc:
            p_move.append((locs[0]+1,locs[1]-1))
    if color_ == 0:
        if locs[1] == 2:
            if (locs[0],locs[1]+1) not in whitepieces_loc and ((locs[0],locs[1]+1) not in blackpieces_loc or (locs[0],locs[1]+2) not in whitepieces_loc):
                p_move.append((locs[0],locs[1]+1))
                p_move.append((locs[0],locs[1]+2))
        else:
            if (locs[0],locs[1]+1) not in whitepieces_loc:
                p_move.append((locs[0],locs[1]+1))
        if (locs[0]-1,locs[1]+1) in whitepieces_loc:
            p_move.append((locs[0]-1,locs[1]+1))
        if (locs[0]+1,locs[1]+1) in whitepieces_loc:
            p_move.append((locs[0]+1,locs[1]+1))
    return p_move
def knight_moves_list(color,locs):
    k_moves = []
    temp = (locs[0]-1,locs[1]-2)
    if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
        k_moves.append(temp)
    temp = (locs[0]+1,locs[1]-2)
    if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
        k_moves.append(temp)
    temp = (locs[0]-2,locs[1]-1)
    if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
        k_moves.append(temp)
    temp = (locs[0]+2,locs[1]-1)
    if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
        k_moves.append(temp)
    temp = (locs[0]-2,locs[1]+1)
    if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
        k_moves.append(temp)
    temp = (locs[0]+2,locs[1]+1)
    if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
        k_moves.append(temp)
    temp = (locs[0]-1,locs[1]+2)
    if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
        k_moves.append(temp)
    temp = (locs[0]+1,locs[1]+2)
    if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
        k_moves.append(temp)
    if color == 1:    
        for x in k_moves:
            if x in whitepieces_loc:
                k_moves.remove(x)
    elif color == 0:    
        for x in k_moves:
            if x in blackpieces_loc:
                k_moves.remove(x)
    return k_moves
def bishop_moves_list(color,locs):
    b_moves = []
    if color == 1:    
        for i in range(1,9):
            temp = (locs[0]-(1*i),locs[1]-(1*i))
            if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
                if temp in blackpieces_loc:
                    b_moves.append(temp)
                    break
                elif temp in whitepieces_loc:
                    break
                else:
                    b_moves.append(temp)
            else:
                break
        for i in range(1,9):
            temp = (locs[0]+(1*i),locs[1]-(1*i))
            if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
                if temp in blackpieces_loc:
                    b_moves.append(temp)
                    break
                elif temp in whitepieces_loc:
                    break
                else:
                    b_moves.append(temp)
            else:
                break
        for i in range(1,9):
            temp = (locs[0]-(1*i),locs[1]+(1*i))
            if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
                if temp in blackpieces_loc:
                    b_moves.append(temp)
                    break
                elif temp in whitepieces_loc:
                    break
                else:
                    b_moves.append(temp)
            else:
                break
        for i in range(1,9):
            temp = (locs[0]+(1*i),locs[1]+(1*i))
            if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
                if temp in blackpieces_loc:
                    b_moves.append(temp)
                    break
                elif temp in whitepieces_loc:
                    break
                else:
                    b_moves.append(temp)
            else:
                break
    elif color == 0:    
        for i in range(1,9):
            temp = (locs[0]-(1*i),locs[1]-(1*i))
            if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
                if temp in whitepieces_loc:
                    b_moves.append(temp)
                    break
                elif temp in blackpieces_loc:
                    break
                else:
                    b_moves.append(temp)
            else:
                break
        for i in range(1,9):
            temp = (locs[0]+(1*i),locs[1]-(1*i))
            if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
                if temp in whitepieces_loc:
                    b_moves.append(temp)
                    break
                elif temp in blackpieces_loc:
                    break
                else:
                    b_moves.append(temp)
            else:
                break
        for i in range(1,9):
            temp = (locs[0]-(1*i),locs[1]+(1*i))
            if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
                if temp in whitepieces_loc:
                    b_moves.append(temp)
                    break
                elif temp in blackpieces_loc:
                    break
                else:
                    b_moves.append(temp)
            else:
                break
        for i in range(1,9):
            temp = (locs[0]+(1*i),locs[1]+(1*i))
            if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
                if temp in whitepieces_loc:
                    b_moves.append(temp)
                    break
                elif temp in blackpieces_loc:
                    break
                else:
                    b_moves.append(temp)
            else:
                break
    return b_moves
def rook_moves_list(color,locs):
    r_moves = []
    if color == 1:    
        for i in range(1,9):
            temp = (locs[0],locs[1]-(1*i))
            if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
                if temp in blackpieces_loc:
                    r_moves.append(temp)
                    break
                elif temp in whitepieces_loc:
                    break
                else:
                    r_moves.append(temp)
            else:
                break
        for i in range(1,9):
            temp = (locs[0]-(1*i),locs[1])
            if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
                if temp in blackpieces_loc:
                    r_moves.append(temp)
                    break
                elif temp in whitepieces_loc:
                    break
                else:
                    r_moves.append(temp)
            else:
                break
        for i in range(1,9):
            temp = (locs[0]+(1*i),locs[1])
            if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
                if temp in blackpieces_loc:
                    r_moves.append(temp)
                    break
                elif temp in whitepieces_loc:
                    break
                else:
                    r_moves.append(temp)
            else:
                break
        for i in range(1,9):
            temp = (locs[0],locs[1]+(1*i))
            if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
                if temp in blackpieces_loc:
                    r_moves.append(temp)
                    break
                elif temp in whitepieces_loc:
                    break
                else:
                    r_moves.append(temp)
            else:
                break
    elif color == 0:    
        for i in range(1,9):
            temp = (locs[0],locs[1]-(1*i))
            if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
                if temp in whitepieces_loc:
                    r_moves.append(temp)
                    break
                elif temp in blackpieces_loc:
                    break
                else:
                    r_moves.append(temp)
            else:
                break
        for i in range(1,9):
            temp = (locs[0]-(1*i),locs[1])
            if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
                if temp in whitepieces_loc:
                    r_moves.append(temp)
                    break
                elif temp in blackpieces_loc:
                    break
                else:
                    r_moves.append(temp)
            else:
                break
        for i in range(1,9):
            temp = (locs[0]+(1*i),locs[1])
            if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
                if temp in whitepieces_loc:
                    r_moves.append(temp)
                    break
                elif temp in blackpieces_loc:
                    break
                else:
                    r_moves.append(temp)
            else:
                break
        for i in range(1,9):
            temp = (locs[0],locs[1]+(1*i))
            if not (temp[0]<2 or temp[0]>9 or temp[1]<1 or temp[1]>8):
                if temp in whitepieces_loc:
                    r_moves.append(temp)
                    break
                elif temp in blackpieces_loc:
                    break
                else:
                    r_moves.append(temp)
            else:
                break
    return r_moves
def queen_moves_list(color,locs):
    q_moves = []
    q_moves.extend(bishop_moves_list(color,locs))
    q_moves.extend(rook_moves_list(color,locs))
    return q_moves
def king_moves_list(color,locs):
    ki_moves = []
    temp = (locs[0]-1,locs[1]-1)
    if  (2 <= temp[0] <= 9 and 1 <= temp[1] <= 8):
        if color == 1:
            if temp not in whitepieces_loc:
                ki_moves.append(temp)
        elif color == 0:
            if temp not in blackpieces_loc:
                ki_moves.append(temp)
    temp = (locs[0],locs[1]-1)
    if  (2 <= temp[0] <= 9 and 1 <= temp[1] <= 8):
        if color == 1:
            if temp not in whitepieces_loc:
                ki_moves.append(temp)
        elif color == 0:
            if temp not in blackpieces_loc:
                ki_moves.append(temp)
    temp = (locs[0]+1,locs[1]-1)
    if  (2 <= temp[0] <= 9 and 1 <= temp[1] <= 8):
        if color == 1:
            if temp not in whitepieces_loc:
                ki_moves.append(temp)
        elif color == 0:
            if temp not in blackpieces_loc:
                ki_moves.append(temp)
    temp = (locs[0]-1,locs[1])
    if  (2 <= temp[0] <= 9 and 1 <= temp[1] <= 8):
        if color == 1:
            if temp not in whitepieces_loc:
                ki_moves.append(temp)
        elif color == 0:
            if temp not in blackpieces_loc:
                ki_moves.append(temp)
    temp = (locs[0]+1,locs[1])
    if  (2 <= temp[0] <= 9 and 1 <= temp[1] <= 8):
        if color == 1:
            if temp not in whitepieces_loc:
                ki_moves.append(temp)
        elif color == 0:
            if temp not in blackpieces_loc:
                ki_moves.append(temp)
    temp = (locs[0]-1,locs[1]+1)
    if  (2 <= temp[0] <= 9 and 1 <= temp[1] <= 8):
        if color == 1:
            if temp not in whitepieces_loc:
                ki_moves.append(temp)
        elif color == 0:
            if temp not in blackpieces_loc:
                ki_moves.append(temp)
    temp = (locs[0],locs[1]+1)
    if  (2 <= temp[0] <= 9 and 1 <= temp[1] <= 8):
        if color == 1:
            if temp not in whitepieces_loc:
                ki_moves.append(temp)
        elif color == 0:
            if temp not in blackpieces_loc:
                ki_moves.append(temp)
    temp = (locs[0]+1,locs[1]+1)
    if  (2 <= temp[0] <= 9 and 1 <= temp[1] <= 8):
        if color == 1:
            if temp not in whitepieces_loc:
                ki_moves.append(temp)
        elif color == 0:
            if temp not in blackpieces_loc:
                ki_moves.append(temp)
    return ki_moves        
def pieces_move(color_,locs_,):
    moves_list2 = []
    moves_list = []
    piec = which_piece_check(locs_)
    if piec == 'pawn':
        moves_list = pawn_moves_list(color_,locs_)
    elif piec == 'knight':
        moves_list = knight_moves_list(color_,locs_)
    elif piec == 'bishop':
        moves_list = bishop_moves_list(color_,locs_)
    elif piec == 'rook':
        moves_list = rook_moves_list(color_,locs_)
    elif piec == 'queen':
        moves_list = queen_moves_list(color_,locs_)
    elif piec == 'king':
        moves_list = king_moves_list(color_,locs_)
        if color_ == 1:
            moves_list2 = king_moves_list(0,blackpieces_loc[blackpieces.index('king')])
        elif color_ == 0:
            moves_list2 = king_moves_list(1,whitepieces_loc[whitepieces.index('king')])
        for x in moves_list2:
            if x in moves_list:
                moves_list.remove(x)
        if color_ == 1:
            if w_king_moved == False and (7,8) not in whitepieces_loc and (8,8) not in whitepieces_loc :
                moves_list.append((8,8))# this is the way to the moon sire
            if w_king_moved == False and (3,8) not in whitepieces_loc and (4,8) not in whitepieces_loc and (5,8) not in whitepieces_loc :
                moves_list.append((4,8))
        elif color_ == 0:
            if b_king_moved == False and (7,1) not in blackpieces_loc and (8,1) not in blackpieces_loc :
                moves_list.append((8,1))# this is the way to the moon sire
            if b_king_moved == False and (3,1) not in blackpieces_loc and (4,1) not in blackpieces_loc and (5,1) not in blackpieces_loc :
                moves_list.append((4,1))
    return moves_list
def time_func():
        global minutes1, second1,minutes2,second2,timer1,timer2
        timer1 = max(0, timer1)
        timer2 = max(0, timer2)
        minutes1 = int(timer1 // 60)
        second1 = int(timer1 % 60)
        minutes2 = int(timer2 // 60)
        second2 = int(timer2 % 60)
        text2 = font.render(f"Player 1: {minutes1:02}:{second1:02} ", True, (0, 0, 0))
        text1 = font.render(f"Player 2: {minutes2:02}:{second2:02} ", True, (0, 0, 0))
        pygame.draw.rect(screen,grey,(630,40,180,40),0,20)
        pygame.draw.rect(screen,black,(630,40,180,40),2,20)
        screen.blit(text1, (650, 50))
        pygame.draw.rect(screen,grey,(630,490,180,40),0,40)
        pygame.draw.rect(screen,black,(630,490,180,40),2,40)
        screen.blit(text2, (650, 500))
def all_pieces_moves_cal(locations,names,color_):
    moves_list = []
    index = 0
    for piec in names:
        if piec == 'pawn':
            moves_list.extend(pawn_moves_list(color_,locations[index]))
        elif piec == 'knight':
            moves_list.extend(knight_moves_list(color_,locations[index]))
        elif piec == 'bishop':
            moves_list.extend(bishop_moves_list(color_,locations[index]))
        elif piec == 'rook':
            moves_list.extend(rook_moves_list(color_,locations[index]))
        elif piec == 'queen':
            moves_list.extend(queen_moves_list(color_,locations[index]))
        index = index + 1
    return moves_list
def king_in_check(move):
    if move%2 == 1:
        index = whitepieces.index('king')
        if whitepieces_loc[index] in black_all_moves:
            return True
    elif move%2 == 0 :
        index = blackpieces.index('king')
        if blackpieces_loc[index] in white_all_moves:
            return True
    return False
def draw_button(x, y, width, height, text, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height),0,40)
        if click[0]:
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, width, height),0,40)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
def show_red_winner(winner):
    for _ in range(3):
        screen.fill(white)
        pygame.draw.rect(screen, red, (500, 500, 200, 100),0,20)
        pygame.draw.rect(screen, black, (500, 500, 200, 100),2,20)
        text = font.render(f"{winner} Won! ", True, white)
        text_rect = text.get_rect(center=(580,550))
        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(0.5)
        screen.fill(white)
        pygame.display.flip()
        time.sleep(0.5)
def reset_game():
    global p_m
    global steps_counter_value
    global running
    global selection
    global valid_moves
    global started
    global timer_start1
    global timer_start2
    global timer1
    global timer2
    global run1
    global run2
    global moved
    global game_state
    global last_time
    global w_king_moved
    global b_king_moved
    global l_w_rook_moved
    global r_w_rook_moved
    global l_b_rook_moved
    global r_b_rook_moved
    global king_captured
    global min10game
    global min30game
    global pvp
    global pvc
    global started
    global whitepieces_loc
    global blackpieces_loc
    global whites_caught_pieces
    global blacks_caught_pieces
    global blackpieces
    global whitepieces
    global selection_running

    p_m = False
    steps_counter_value = 1
    running = True
    selection = False
    valid_moves = []
    started = False
    timer_start1 = 600
    timer_start2 = 600
    timer1 = timer_start1
    timer2 = timer_start2
    run1 = True
    run2 = False
    moved = False
    game_state = True
    last_time = time.time()
    w_king_moved = False
    b_king_moved = False
    l_w_rook_moved = False
    r_w_rook_moved = False
    l_b_rook_moved = False
    r_b_rook_moved = False
    king_captured = False
    min10game = False
    min30game = False
    pvp = False
    pvc = False
    started = False
    selection_running = True
    blackpieces = ['rook','knight','bishop','queen','king','bishop','knight','rook',
               'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn']
    whitepieces = ['pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn',
               'rook','knight','bishop','queen','king','bishop','knight','rook']
    whitepieces_loc = [(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),(9,7),
                    (2,8),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8),(9,8)]
    blackpieces_loc = [(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),
                    (2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),(9,2)]
    whites_caught_pieces = []
    blacks_caught_pieces = []      
#STOCK FISH RELATED FUNCTIONS
def get_fen():
    global whitepieces,blackpieces,whitepieces_loc,blackpieces_loc
    piece_symbols = {
        "pawn": "P", "rook": "R", "knight": "N", "bishop": "B", "queen": "Q", "king": "K"
    }
    board = [["" for _ in range(8)] for _ in range(8)]
    def convert_positions(piece_positions):
        return [(y - 1, x - 2) for pos in piece_positions if pos is not None for (x, y) in [pos]]
    for i, pos in enumerate(convert_positions(whitepieces_loc)):
        row, col = pos
        if whitepieces[i] == None:
            continue
        board[row][col] = piece_symbols[whitepieces[i]]
    for i, pos in enumerate(convert_positions(blackpieces_loc)):
        row, col = pos
        if blackpieces[i] == None:
            continue
        board[row][col] = piece_symbols[blackpieces[i]].lower()
    fen_rows = []
    for row in board:
        fen_row = ""
        empty_count = 0
        for cell in row:
            if cell == "":
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += cell
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)
    return "/".join(fen_rows) + " b - - 0 1"
def chess_notation_to_index(move):
    move = move[:2] + " " + move[2:]
    file_to_col = {'a': 2, 'b': 3, 'c': 4, 'd': 5, 'e': 6, 'f': 7, 'g': 8, 'h': 9}
    file_to_row = {'1':8, '2':7, '3':6, '4':5, '5':4, '6':3, '7':2, '8':1}
    start, end = move.split()
    start_col = file_to_col[start[0]]
    start_row = file_to_row[start[1]]
    end_col = file_to_col[end[0]]
    end_row = file_to_row[end[1]]
    return (start_col, start_row), (end_col, end_row)
p_m = False
steps_counter_value = 1
running = True
selection = False
valid_moves = []
started = False
timer_start1 = 600
timer_start2 = 600
timer1 = timer_start1
timer2 = timer_start2
run1 = True
run2 = False
moved = False
game_state = True
last_time = time.time()
w_king_moved = False
b_king_moved = False
l_w_rook_moved = False
r_w_rook_moved = False
l_b_rook_moved = False
r_b_rook_moved = False
king_captured = False
min10game = False
min30game = False
pvp = False
pvc = False
started = False
selection_running = True
while running:
    while selection_running:
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if buttons["Player V Player"].collidepoint(x, y):
                    pvp = True
                    pvc = False
                    started = True
                elif buttons["Player V CPU"].collidepoint(x, y):
                    pvc = True
                    pvp = False
                    started = True
                elif buttons["Start"].collidepoint(x, y):
                    selection_running = False
        for text, rect in buttons.items():
            if pvp == True and text == "Player V Player" :
                pygame.draw.rect(screen, dark_grey, rect,0,20)
            elif pvc == True and text == "Player V CPU":
                pygame.draw.rect(screen, dark_grey, rect,0,20)
            elif text == "Start":
                pygame.draw.rect(screen, green, rect,0,20)
            else:
                pygame.draw.rect(screen, grey if text != "Start" else green, rect,0,20)
            pygame.draw.rect(screen,black,(750,350,200,40),2,20)
            pygame.draw.rect(screen,black,(1000,350,200,40),2,20)
            pygame.draw.rect(screen,black,(920,450,100,40),2,20)
            label = font.render(text, True, black)
            screen.blit(label, (rect.x + 25, rect.y + 10))
        chesBoard()
        piecesdraw()
        chess_board_cords()
        pygame.display.flip()
    screen.fill(white)
    if pvc == True:
        index = whitepieces.index('king')
        white_king_location = whitepieces_loc[index]
        if (white_king_location == (8,8)) and w_king_moved == False and r_w_rook_moved == False:
            whitepieces_loc[15] = (7,8)
            w_king_moved = True
            l_w_rook_moved = True
            r_w_rook_moved = True
        elif (white_king_location == (4,8)) and w_king_moved == False and l_w_rook_moved == False:
            whitepieces_loc[8] = (5,8)
            w_king_moved = True
            r_w_rook_moved = True
            l_w_rook_moved = True
        index = blackpieces.index('king')
        black_king_location = blackpieces_loc[index]
        if (black_king_location == (8,1)) and b_king_moved == False and r_b_rook_moved == False:
            blackpieces_loc[7] = (7,1)
            b_king_moved = True
            r_b_rook_moved = True
            l_b_rook_moved = True
        elif (black_king_location == (4,1)) and b_king_moved == False and l_b_rook_moved == False:
            blackpieces_loc[0] = (5,1)
            b_king_moved = True
            l_b_rook_moved = True
            r_b_rook_moved = True
        clock.tick(fps)
        white_all_moves = all_pieces_moves_cal(whitepieces_loc,whitepieces,1)
        black_all_moves = all_pieces_moves_cal(blackpieces_loc,blackpieces,0)
        chesBoard()
        if king_in_check(steps_counter_value):
            if steps_counter_value%2 == 1:
                index = whitepieces.index('king')
                location = whitepieces_loc[index]
                x_val = location[0]
                y_val = location[1]
                x = x_val * 60 
                y = y_val * 60 
                sqre = [x,y,60,60]
                pygame.draw.rect(screen,red,sqre)
            elif steps_counter_value%2 == 0:
                index = blackpieces.index('king')
                location = blackpieces_loc[index]
                x_val = location[0]
                y_val = location[1]
                x = x_val * 60
                y = y_val * 60
                sqre = [x,y,60,60]
                pygame.draw.rect(screen,red,sqre)
        piecesdraw()
        chess_board_cords()
        if steps_counter_value%2 == 0:
            fen = get_fen()
            stockfish.set_fen_position(fen)
            material_caught()
            imger = stepsdisplayer(steps_counter_value)
            screen.blit(imger, (250, 590))
            points_of_material()
            chesBoard()
            piecesdraw()
            chess_board_cords()
            pygame.display.flip()
            move = stockfish.get_best_move()
            start_pos, end_pos = chess_notation_to_index(move)
            if start_pos in whitepieces_loc and end_pos in blackpieces_loc:
                whitepieces_loc[whitepieces_loc.index(start_pos)] = end_pos
                blacks_caught_pieces.append(blackpieces[blackpieces_loc.index(end_pos)])
                blackpieces[blackpieces_loc.index(end_pos)] = None
                blackpieces_loc[blackpieces_loc.index(end_pos)] = None
                take_sound.play()
            elif start_pos in whitepieces_loc :
                whitepieces_loc[whitepieces_loc.index(start_pos)] = end_pos
                move_sound.play()
            elif start_pos in blackpieces_loc and end_pos in whitepieces_loc:
                blackpieces_loc[blackpieces_loc.index(start_pos)] = end_pos
                whites_caught_pieces.append(whitepieces[whitepieces_loc.index(end_pos)])
                whitepieces[whitepieces_loc.index(end_pos)] = None
                whitepieces_loc[whitepieces_loc.index(end_pos)] = None
                take_sound.play()
            elif start_pos in blackpieces_loc :
                blackpieces_loc[blackpieces_loc.index(start_pos)] = end_pos
                move_sound.play()
            steps_counter_value = steps_counter_value + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and selection == False and started == True and steps_counter_value%2 == 1:
                x_cords = event.pos[0] // 60
                y_cords = event.pos[1] // 60
                actcords = (x_cords, y_cords)
                color_chk = checklocs(actcords)
                if color_chk == 1 or color_chk == 0:
                    selection = True
                else:
                    selection = False
                valid_moves = pieces_move(color_chk, actcords)
                p_m = True
            elif event.type == pygame.MOUSEBUTTONDOWN and selection == True and started == True and steps_counter_value%2 == 1:
                x_cords2 = event.pos[0] // 60
                y_cords2 = event.pos[1] // 60
                actcords2 = (x_cords2, y_cords2)
                if steps_counter_value % 2 == color_chk and (check_locks_valid(color_chk, actcords, actcords2) == True) and (actcords2 in valid_moves) and  not (king_in_check(steps_counter_value)):
                    locks_changer(actcords, actcords2, steps_counter_value)
                    p_m = False
                    selection = False
                    steps_counter_value = steps_counter_value + 1 
                    if steps_counter_value%2 == 1 and white_king_location != (8,8) and white_king_location != (4,8) and white_king_location != (6,8):
                            w_king_moved = True
                    if steps_counter_value%2 == 0 and black_king_location != (8,1) and black_king_location != (4,1) and black_king_location != (6,1):
                        b_king_moved = True
                elif king_in_check(steps_counter_value):
                    index1 = whitepieces.index('king')
                    index2 = blackpieces.index('king')
                    if (actcords == whitepieces_loc[index1] or actcords == blackpieces_loc[index2]) and (actcords2 in valid_moves):
                        locks_changer(actcords, actcords2, steps_counter_value)
                        p_m = False
                        selection = False
                        steps_counter_value = steps_counter_value + 1
                    else:
                        selection = False
                else:
                    selection = False
        if started == True:
            imger = stepsdisplayer(steps_counter_value)
            screen.blit(imger, (250, 590))
            points_of_material()
        if started == True:
            if run1:
                elapsed_time = time.time() - last_time
                timer1 -= elapsed_time
                last_time = time.time()
            if run2:
                elapsed_time = time.time() - last_time
                timer2 -= elapsed_time
                last_time = time.time()
            time_func()
            if (minutes1 == 0 and second1 == 0) or 'king' not in whitepieces:
                started = False
                show_red_winner("BLACK")
                reset_game()
            elif (minutes2 == 0 and second2 == 0) or 'king' not in blackpieces :
                started = False
                show_red_winner("WHITE")
                reset_game()
        if p_m == True:
            draw_possible_moves(valid_moves)
        if started == True:
            material_caught()
        if moved == True:
            if run1:
                run1 = False
                run2 = True
                last_time = time.time()
            elif run2:
                run2 = False
                run1 = True
                last_time = time.time()
        moved = False
        pygame.display.flip()
    if pvp == True:            
        index = whitepieces.index('king')
        white_king_location = whitepieces_loc[index]
        if (white_king_location == (8,8)) and w_king_moved == False and r_w_rook_moved == False:
            whitepieces_loc[15] = (7,8)
            w_king_moved = True
            l_w_rook_moved = True
            r_w_rook_moved = True
        elif (white_king_location == (4,8)) and w_king_moved == False and l_w_rook_moved == False:
            whitepieces_loc[8] = (5,8)
            w_king_moved = True
            r_w_rook_moved = True
            l_w_rook_moved = True
        index = blackpieces.index('king')
        black_king_location = blackpieces_loc[index]
        if (black_king_location == (8,1)) and b_king_moved == False and r_b_rook_moved == False:
            blackpieces_loc[7] = (7,1)
            b_king_moved = True
            r_b_rook_moved = True
            l_b_rook_moved = True
        elif (black_king_location == (4,1)) and b_king_moved == False and l_b_rook_moved == False:
            blackpieces_loc[0] = (5,1)
            b_king_moved = True
            l_b_rook_moved = True
            r_b_rook_moved = True
        clock.tick(fps)
        white_all_moves = all_pieces_moves_cal(whitepieces_loc,whitepieces,1)
        black_all_moves = all_pieces_moves_cal(blackpieces_loc,blackpieces,0)
        chesBoard()
        if king_in_check(steps_counter_value):
            if steps_counter_value%2 == 1:
                index = whitepieces.index('king')
                location = whitepieces_loc[index]
                x_val = location[0]
                y_val = location[1]
                x = x_val * 60 
                y = y_val * 60 
                sqre = [x,y,60,60]
                pygame.draw.rect(screen,red,sqre)
            elif steps_counter_value%2 == 0:
                index = blackpieces.index('king')
                location = blackpieces_loc[index]
                x_val = location[0]
                y_val = location[1]
                x = x_val * 60
                y = y_val * 60
                sqre = [x,y,60,60]
                pygame.draw.rect(screen,red,sqre)
        piecesdraw()
        chess_board_cords()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and selection == False and started == True:
                x_cords = event.pos[0] // 60
                y_cords = event.pos[1] // 60
                actcords = (x_cords, y_cords)
                color_chk = checklocs(actcords)
                if color_chk == 1 or color_chk == 0:
                    selection = True
                else:
                    selection = False
                valid_moves = pieces_move(color_chk, actcords)
                p_m = True
            elif event.type == pygame.MOUSEBUTTONDOWN and selection == True and started == True:
                x_cords2 = event.pos[0] // 60
                y_cords2 = event.pos[1] // 60
                actcords2 = (x_cords2, y_cords2)
                if steps_counter_value % 2 == color_chk and (check_locks_valid(color_chk, actcords, actcords2) == True) and (actcords2 in valid_moves) and  not (king_in_check(steps_counter_value)):
                    locks_changer(actcords, actcords2, steps_counter_value)
                    p_m = False
                    selection = False
                    steps_counter_value = steps_counter_value + 1 
                    if steps_counter_value%2 == 1 and white_king_location != (8,8) and white_king_location != (4,8) and white_king_location != (6,8):
                            w_king_moved = True
                    if steps_counter_value%2 == 0 and black_king_location != (8,1) and black_king_location != (4,1) and black_king_location != (6,1):
                        b_king_moved = True
                elif king_in_check(steps_counter_value):
                    index1 = whitepieces.index('king')
                    index2 = blackpieces.index('king')
                    if (actcords == whitepieces_loc[index1] or actcords == blackpieces_loc[index2]) and (actcords2 in valid_moves):
                        locks_changer(actcords, actcords2, steps_counter_value)
                        p_m = False
                        selection = False
                        steps_counter_value = steps_counter_value + 1
                    else:
                        selection = False
                else:
                    selection = False
        if started == True:
            imger = stepsdisplayer(steps_counter_value)
            screen.blit(imger, (250, 590))
            points_of_material()
        if started == True:
            if run1:
                elapsed_time = time.time() - last_time
                timer1 -= elapsed_time
                last_time = time.time()
            if run2:
                elapsed_time = time.time() - last_time
                timer2 -= elapsed_time
                last_time = time.time()
            time_func()
            if (minutes1 == 0 and second1 == 0) or 'king' not in whitepieces:
                started = False
                show_red_winner("BLACK")
                reset_game()
            elif (minutes2 == 0 and second2 == 0) or 'king' not in blackpieces :
                started = False
                show_red_winner("WHITE")
                reset_game()
        if p_m == True:
            draw_possible_moves(valid_moves)
        if started == True:
            material_caught()
        if moved == True:
            if run1:
                run1 = False
                run2 = True
                last_time = time.time()
            elif run2:
                run2 = False
                run1 = True
                last_time = time.time()
        moved = False
        pygame.display.flip()
pygame.quit()
