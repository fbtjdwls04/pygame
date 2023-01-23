import pygame
import random
import time
from datetime import datetime

pygame.init()

size = [400,900]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("연습제작게임")
clock = pygame.time.Clock()
score = 0
miss = 0
#########################################################################        
class Object:                                                          
    def __init__(self):                                                 
        self.x = 0
        self.y = 0
        self.move = 0
        self.hp = 1
    def add_Object(self, address):
        if address[-3:] == "png":
            self.image = pygame.image.load(address).convert_alpha()
        else:
            self.image = pygame.image.load(address)
        self.size_x, self.size_y = self.image.get_size()
        
    def change_size(self,size_x,size_y):
        self.image = pygame.transform.scale(self.image, (size_x,size_y))
        
        self.size_x, self.size_y = self.image.get_size()
    
    def show(self):
        screen.blit(self.image, (self.x,self.y))
            
class Missile(Object):
    def __init__(self):
        self.hp = 1
class Enemy(Object):
    def __init__(self):
        self.type = "normal"
        self.hp = 5
    
        
def collide(a, b):
    if (a.x - b.size_x <= b.x)and (b.x <= a.x + a.size_x)and (b.y <= a.y + a.size_y)and (b.y >= a.y - b.size_y):
        return True
    return False
#########################################################################        
restart = True

wait_running = True
while restart:  # 다시 시작 시 캐릭터 재 생성 및 적 개체 초기화    
    space_ship = Object()
    space_ship.add_Object("C:/Users/ahtl0/OneDrive/바탕 화면/pythonworkspace/pygame_basic/image/space_ship.png")
    space_ship.change_size(30,50)
    space_ship.x = round(size[0]/2) - round(space_ship.size_x/2)
    space_ship.y = size[1] - space_ship.size_y - 30
    space_ship.move = 0.2
    to_x_left = 0
    to_x_right = 0
    to_y_up = 0
    to_y_down = 0

    missile_shot = False
    missile_tick = 0

    color = (20,20,20)

    start_time = datetime.now()
    
    missile_list = []
    enemy_list = []

    running = True
    while running:  # 게임 진행
        while wait_running:
            clock.tick(60)
            font = pygame.font.Font("C:/Users/ahtl0/AppData/Local/Microsoft/Windows/Fonts/D2Coding-Ver1.3.2-20180524.ttc", 30)
            text = font.render("PLAY to press 'SPACE_KEY'",True,(255,255,255))
            screen.blit(text, (15,450))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        wait_running = False
                if event.type == pygame.QUIT:
                    pygame.quit()
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    to_x_left -= space_ship.move
                elif event.key == pygame.K_RIGHT:
                    to_x_right += space_ship.move
                elif event.key == pygame.K_UP:
                    to_y_up -= space_ship.move
                elif event.key == pygame.K_DOWN:
                    to_y_down += space_ship.move
                elif event.key == pygame.K_SPACE:
                    missile_shot = True
                    missile_tick = 0

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    to_x_left = 0
                elif event.key == pygame.K_RIGHT:
                    to_x_right = 0
                elif event.key == pygame.K_UP:
                    to_y_up = 0
                elif event.key == pygame.K_DOWN:
                    to_y_down = 0
                elif event.key == pygame.K_SPACE:
                    missile_shot = False
        ################# 시간에 따른 변화 ############################################    
        space_ship.x += (to_x_left + to_x_right) * dt
        space_ship.y += (to_y_up + to_y_down) * dt

        current_time = datetime.now()
        delta_time = round((current_time - start_time).total_seconds())

        if space_ship.x < 0:
            space_ship.x = 0
        elif space_ship.x > size[0] - space_ship.size_x:
            space_ship.x = size[0] - space_ship.size_x
        if space_ship.y < 0:
            space_ship.y = 0
        elif space_ship.y > size[1] - space_ship.size_y:
            space_ship.y = size[1] - space_ship.size_y

        ####################### 미사일 처리 ###########################################
        if missile_shot and missile_tick == 0:
            missile_sound = pygame.mixer.Sound( "C:/Users/ahtl0/OneDrive/바탕 화면/pythonworkspace/pygame_basic/sound/gun_sound.wav" )
            missile_sound.play()
            missile = Missile()
            missile.add_Object("C:/Users/ahtl0/OneDrive/바탕 화면/pythonworkspace/pygame_basic/image/missile.png")
            missile.change_size(10,30)
            missile.x = round(space_ship.x + space_ship.size_x/2 - missile.size_x / 2)
            missile.y = space_ship.y
            missile.move = 2
            missile_list.append(missile)    

        # 미사일 공격속도   
        missile_tick += 1
        if missile_tick == 5:
            missile_tick = 0

        # 미사일 이동    
        for m in missile_list:
            if m.y < 0 or m.hp <= 0:
                missile_list.remove(m)
            m.y -= missile.move * dt

        ############################ 적 처리 ##########################################    
        if random.random() > 0.97:
            enemy = Enemy()
            enemy.add_Object("C:/Users/ahtl0/OneDrive/바탕 화면/pythonworkspace/pygame_basic/image/enemy.png")
            enemy.change_size(40,40)
            enemy.x = random.randrange(0,size[0]-enemy.size_x)
            enemy.y = 0 - enemy.size_y
            enemy.move = 0.1
            enemy_list.append(enemy)
        if random.random() > 0.999:
            elite_enemy = Enemy()
            elite_enemy.add_Object("C:/Users/ahtl0/OneDrive/바탕 화면/pythonworkspace/pygame_basic/image/elite_enemy.png")
            elite_enemy.change_size(100,100)
            elite_enemy.x = random.randrange(0,size[0]-enemy.size_x)
            elite_enemy.y = 0 - enemy.size_y
            elite_enemy.type = "elite"
            elite_enemy.hp = 50
            elite_enemy.move = 0.02
            enemy_list.append(elite_enemy)    

        # 적 이동    
        for e in enemy_list:

            for m in missile_list:          # 적과 투사체의 충돌 판정
                if collide(m,e):
                    m.hp -= 1
                    e.hp -= 1

            if e.y >= size[1]:              # 화면 밖으로 나가면 없어짐
                enemy_list.remove(e)
                miss += 1
            elif e.hp <= 0:
                    enemy_list.remove(e)
                    if e.type == "normal":
                        score += 1
                    elif e.type == "elite":
                        score += 20

            if collide(space_ship, e):             # 적과 캐릭터의 충돌 판정
                space_ship.hp -= 1
                if space_ship.hp <= 0:
                    game_over = True
                    while game_over:
                        clock.tick(60)
                        font = pygame.font.Font("C:/Users/ahtl0/AppData/Local/Microsoft/Windows/Fonts/D2Coding-Ver1.3.2-20180524.ttc", 50)
                        text = font.render("GAME OVER",True,(255,0,0))
                        
                        screen.blit(text, (90,450))
                        
                        font = pygame.font.Font("C:/Users/ahtl0/AppData/Local/Microsoft/Windows/Fonts/D2Coding-Ver1.3.2-20180524.ttc", 30)
                        text = font.render("restart 'SPACE'",True,(255,0,0))
                        
                        screen.blit(text,(90,500))
                        
                        pygame.display.flip()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            if event.type == pygame.KEYDOWN:      # GAME OVER 시 SPACE BAR 입력시 재 시작
                                if event.key == pygame.K_SPACE:
                                    game_over = False
                                    running = False

            e.y += e.move * dt


        ######################## 전사 작업 ############################################
        screen.fill(color)

        font = pygame.font.Font("C:/Users/ahtl0/AppData/Local/Microsoft/Windows/Fonts/D2Coding-Ver1.3.2-20180524.ttc", 20)
        text = font.render(f"score = {score} Miss = {miss} time = {delta_time}",True, (255,255,255))
        screen.blit(text, (5,0))

        space_ship.show()

        for e in enemy_list:
            e.show()

        for m in missile_list:
            m.show()

        pygame.display.flip()


pygame.quit()
