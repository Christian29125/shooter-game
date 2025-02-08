#Create your own shooter
from time import time as timer
from random import randint
from pygame import *
display.set_caption('Shooter')
win = display.set_mode((700, 500))
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
bullet_sound = mixer.Sound("fire.ogg")
bullet_image = 'bullet.png'

class game_character(sprite.Sprite):
    def __init__(self, player_image, width, height, x, y, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
max_Lost = 3
lost = 0
score = 0
goal = 10
class Enemy(game_character):
    def update(self):
        self.rect.y += self.speed
        global lost 
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost  += 1

font.init()
font1 = font.Font(None, 80)
winner = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0) )

ufos = sprite.Group()
for i in range(1, 6):
    ufo = Enemy('ufo.png', 80, 50, randint(80, 620), 0, randint(1,5)) #, randint(1,5)
    ufos.add(ufo)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy('asteroid.png', 80, 50, randint(80, 620), 0, randint(1,5))
    asteroids.add(asteroid)



bullets = sprite.Group()
class control(game_character):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(bullet_image, 15, 20, self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)
rocket = control('rocket.png', 50, 120, 10, 380, 10)


font2 = font.Font(None, 36)

class Bullet(game_character):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

rel_time = False
num_fire = 0

finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 7 and rel_time == False:
                    num_fire += 1
                    bullet_sound.play()
                    rocket.fire()
                if num_fire >= 7 and rel_time == False:
                    last_time = timer()
                    rel_time = True 


    if finish == False:
        win.blit(background, (0, 0))
        rocket.update()
        ufos.update()
        asteroids.update()
        bullets.update()
        collides = sprite.groupcollide(ufos, bullets, True, True)
        for c in collides: 
            score = score + 1 
            monster =  ufo = Enemy('ufo.png', 80, 50, randint(80, 620), 0, randint(1,5))
            ufos.add(ufo)
        collide2 =  sprite.groupcollide(asteroids, bullets, True, True)  
        for c in collide2: 
            score = score + 1 
            monster =  asteroid = Enemy('asteroid.png', 80, 50, randint(80, 620), 0, randint(1,5))
            asteroids.add(asteroid)
        if sprite.spritecollide(rocket, ufos, False) or lost >= max_Lost:
            finish = True
            win.blit(lose, (200, 200))
        if sprite.spritecollide(rocket, asteroids, False) or lost >= max_Lost:
            Finish = True
            win.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            win.blit(winner, (200, 300))

        if rel_time == True:
            now_time = timer() 
            if now_time - last_time < 3: 
                reload = font2.render('wait, reload...', 1, (150, 0, 0))
                win.blit(reload, (260, 460)) 
            else:
                num_fire = 0
                rel_time = False
        rocket.reset()
        ufos.draw(win)
        asteroids.draw(win)
        bullets.draw(win)

        text = font2.render("score :" + str(score), 1, (255, 255, 255))
        win.blit(text, (10,20))

        text = font2.render("miss :" + str(lost), 1, (255, 255, 255))
        win.blit(text, (10,50))
        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        for b in bullets:
            b.kill()
        for u in ufos:
            u.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range (1,6):
            ufo = Enemy('ufo.png', 80, 50, randint(80, 620), 0, randint(1,5))
            ufos.add(ufo)
        for i in range(1, 3):
            asteroid = Enemy('asteroid.png', 80, 50, randint(80, 620), 0, randint(1,5))
            asteroids.add(asteroid)
    time.delay(50)











