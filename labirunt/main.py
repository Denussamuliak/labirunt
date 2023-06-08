from pygame import *

'''Необхідні класи'''


# клас-батько для спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()

        # кожен спрайт має зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (55, 55))
        self.speed = player_speed

        # кожен спрайт має зберігати властивість rect - прямокутник, у який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# клас-спадкоємець для спрайта-гравця (керується стрілками)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed


# клас-спадкоємець для спрайта-ворога (переміщується сам)
class Enemy(GameSprite):
    side = "left"

    def update(self):
        if self.rect.x <= 470:
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


# клас для спрайтів-перешкод
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height

        # картинка стіни - прямокутник потрібних розмірів і кольору
        self.image = Surface([self.width, self.height])
        self.image.fill((color_1, color_2, color_3))

        # кожен спрайт має зберігати властивість rect - прямокутник
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


'''Опис гри'''

# Ігрова сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("background3.png"), (win_width, win_height))

w1 = Wall(154, 205, 50, 100, 20, 450, 10)
w2 = Wall(154, 205, 50, 100, 480, 350, 10)
w3 = Wall(154, 205, 50, 100, 20, 10, 380)
w4 = Wall(154, 205, 50, 200, 130, 10, 350)
w5 = Wall(154, 205, 50, 450, 130, 10, 360)
w6 = Wall(154, 205, 50, 300, 20, 10, 350)
w7 = Wall(154, 205, 50, 390, 120, 130, 10)

# Персонажі гри:
packman = Player('hero.png', 5, win_height - 80, 4)
monster = Enemy('cyborg.png', win_width - 80, 280, 2)
monster1 = Enemy('cyborg.png', win_width - 80, 180, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

# Музика
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    keys = key.get_pressed()
    if finish and keys[K_r]:
        packman.rect.x = 5
        packman.rect.y = win_height - 80
        finish = False

    if finish != True:
        window.blit(background, (0, 0))
        packman.update()
        monster.update()
        monster1.update()

        packman.reset()
        monster.reset()
        monster1.reset()
        final.reset()

        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        w7.draw_wall()

        # Ситуація "Поразка"
        if sprite.collide_rect(packman, monster) or sprite.collide_rect(packman, w1) or sprite.collide_rect(packman,
            w2) or sprite.collide_rect(packman, w2) or sprite.collide_rect(packman, w3) or sprite.collide_rect(packman,
            w4) or sprite.collide_rect(packman, w5) or sprite.collide_rect(packman, w6) or sprite.collide_rect(packman,
            w7) or sprite.collide_rect(packman, monster1):
            finish = True
            window.blit(lose, (200, 200))
            kick.play()

        # Ситуація "Перемога"
        if sprite.collide_rect(packman, final):
            finish = True
            window.blit(win, (200, 200))
            money.play()


    display.update()
    clock.tick(FPS)