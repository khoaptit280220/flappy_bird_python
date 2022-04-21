import pygame
from random import randint

pygame.init()

# set tỷ lệ dài và rộng của màn hình
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption('Flappy Bird K.NT')

clock = pygame.time.Clock()

# set background cho game
background_img = pygame.image.load('images/background.png')

# set kích thước image background cho đúng tỷ lệ màn hình
background_img = pygame.transform.scale(background_img, (400, 600))

x_bird = 50
y_bird = 350

# đưa ảnh chim vào game
bird_img = pygame.image.load('images/bluebird-midflap.png')
bird1_img = pygame.image.load('images/bluebird-downflap.png')
bird2_img = pygame.image.load('images/bluebird-upflap.png')

# set kích thước con chim trong game
bird_img = pygame.transform.scale(bird_img, (35, 35))

# set vị trí ống
tube1_x = 400
tube2_x = 600
tube3_x = 800

# set độ rộng ống
tube_width = 50

# set chiều cao ống lấy random
tube1_height = randint(100, 400)
tube2_height = randint(100, 400)
tube3_height = randint(100, 400)

# khoảng cách giữa 2 tube đối diện nhau
d_2tube = 150

# set biến để chim rơi
bird_drop_velocity = 0
gravity = 0.5
tube_velocity = 2

# ghi điểm ra màn hình
score = 0
font = pygame.font.SysFont('san', 20)
font1 = pygame.font.SysFont('san', 35)

# đưa ảnh ống vào game
tube_img = pygame.image.load('images/tube.png')

# đưa ảnh ống đối diện vào
tube_op_img = pygame.image.load('images/tube_op.png')

#đưa âm thanh vào
#sound = pygame.mixer.Sound('no6.wav')
sound_die = pygame.mixer.Sound('sound/die.wav')
sound_hit = pygame.mixer.Sound('sound/hit.wav')
sound_point = pygame.mixer.Sound('sound/point.wav')
sound_swoosh = pygame.mixer.Sound('sound/swoosh.wav')
sound_wing = pygame.mixer.Sound('sound/wing.wav')


#đưa ảnh khi chim rơi
sand_img = pygame.image.load('images/sand.png')
sand_img = pygame.transform.scale(sand_img,(400,30))

# kiểm tra xem các ống đã đi qua chim chưa
tube1_pass = False
tube2_pass = False
tube3_pass = False
pausing = False

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0,0,255)

running = True
while running:
    #pygame.mixer.Sound.play(sound)
    # nháy 60 lần / 1 giây
    clock.tick(60)

    # set màu nền
    screen.fill(WHITE)

    # vẽ background vào khung hình game
    screen.blit(background_img, (0, 0))

    # ép ống và vẽ  ống
    tube1_img = pygame.transform.scale(tube_img, (tube_width, tube1_height))
    tube1 = screen.blit(tube1_img, (tube1_x, 0))

    tube2_img = pygame.transform.scale(tube_img, (tube_width, tube2_height))
    tube2 = screen.blit(tube2_img, (tube2_x, 0))

    tube3_img = pygame.transform.scale(tube_img, (tube_width, tube3_height))
    tube3 = screen.blit(tube3_img, (tube3_x, 0))

    # ép ống và vẽ ống đối diện
    tube1_op_img = pygame.transform.scale(
        tube_op_img, (tube_width, 600-(tube1_height + d_2tube)))
    tube1_op = screen.blit(tube1_op_img, (tube1_x, tube1_height + d_2tube))

    tube2_op_img = pygame.transform.scale(
        tube_op_img, (tube_width, 600-(tube2_height + d_2tube)))
    tube2_op = screen.blit(tube2_op_img, (tube2_x, tube2_height + d_2tube))

    tube3_op_img = pygame.transform.scale(
        tube_op_img, (tube_width, 600-(tube3_height + d_2tube)))
    tube3_op = screen.blit(tube3_op_img, (tube3_x, tube3_height + d_2tube))

    # ống di chuyển sang trái
    tube1_x -= tube_velocity
    tube2_x -= tube_velocity
    tube3_x -= tube_velocity

    # tạo ống mới
    if tube1_x < -tube_width:
        tube1_x = 550
        tube1_height = randint(100, 400)
        tube1_pass = False

    if tube2_x < -tube_width:
        tube2_x = 550
        tube2_height = randint(100, 400)
        tube2_pass = False

    if tube3_x < -tube_width:
        tube3_x = 550
        tube3_height = randint(100, 400)
        tube3_pass = False

    #vẽ cát
    sand = screen.blit(sand_img,(0,570))
    
    #khởi tạo mảng con chim
    birds = [bird_img, bird1_img, bird_img,bird2_img]
           
    # vẽ con chim vào game
    bird = screen.blit(bird_img, (x_bird, y_bird))
    bird1 = screen.blit(bird1_img, (x_bird, y_bird))
    bird2 = screen.blit(bird2_img, (x_bird, y_bird))

    # chim rơi
    y_bird += bird_drop_velocity
    bird_drop_velocity += gravity

    # ghi điểm
    score_txt = font.render("Score:"+str(score), True, RED)
    screen.blit(score_txt, (5, 5))

    #cộng điểm
    if tube1_x + tube_width <= x_bird and tube1_pass == False:
        pygame.mixer.Sound.play(sound_point)
        score += 1
        tube1_pass = True
    if tube2_x + tube_width <= x_bird and tube2_pass == False:
        pygame.mixer.Sound.play(sound_point)
        score += 1
        tube2_pass = True
    if tube3_x + tube_width <= x_bird and tube3_pass == False:
        pygame.mixer.Sound.play(sound_point)
        score += 1
        tube3_pass = True
    
    #kiểm tra sự va chạm
    tubes =[tube1, tube2, tube3, tube1_op, tube2_op, tube3_op, sand]
    for tube in tubes:
        if bird.colliderect(tube) or bird1.colliderect(tube) or bird2.colliderect(tube):
            if pausing == False:
                sound_hit.play()
                sound_die.play()
            tube_velocity =0
            bird_drop_velocity =0
            game_over_txt = font1.render("Game over, Score:" +str(score),True,RED)
            screen.blit(game_over_txt,(85,260))
            space_txt = font.render("Press Space to continue!", True, BLUE)
            screen.blit(space_txt,(120,290))
            pausing = True

    # kiểm tra các sự kiện trong game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # set cho chim nhảy lên
        if event.type == pygame.KEYDOWN:
                
            # vẽ con chim vào game
            for bird in birds:
                    
                if event.key == pygame.K_SPACE:
                
                    bird = screen.blit(bird, (x_bird, y_bird))
                    pygame.mixer.Sound.play(sound_wing)
                    bird_drop_velocity = 0
                    bird_drop_velocity -= 6
                    if pausing:
                    #pygame.mixer.unpause()
                        x_bird =50
                        y_bird = 350
                        tube1_x = 400
                        tube2_x = 600
                        tube3_x = 800
                        tube_velocity = 2
                        score =0
                        pausing = False
                    
    # hiển thị ra màn hình
    pygame.display.flip()
pygame.quit()
