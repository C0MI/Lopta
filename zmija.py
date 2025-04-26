import pygame
import random
import sys

# inicijalizacija
pygame.init()
sirina, visina = 600, 400
prozor = pygame.display.set_mode((sirina, visina))
pygame.display.set_caption("Zmija juri pokretnu loptu")
sat = pygame.time.Clock()

# Boje
ZELENA = (0, 255, 0)
CRVENA = (255, 0, 0)
CRNA = (0, 0, 0)

# Klase
class Zmija:
    def __init__(self):
        self.blok_velicina = 20
        self.telo = [[300, 200]]
        self.smer = (0, 0)

    def pomeri(self):
        glava_x, glava_y = self.telo[0]
        dx, dy = self.smer
        nova_pozicija = [glava_x + dx, glava_y + dy]
        self.telo.insert(0, nova_pozicija)
        self.telo.pop()

    def pojedi(self):
        self.telo.append(self.telo[-1])

    def crtaj(self):
        for segment in self.telo:
            pygame.draw.rect(prozor, ZELENA, (*segment, self.blok_velicina, self.blok_velicina))

class Lopta:
    def __init__(self, brzina):
        self.r = 10
        self.x = random.randint(self.r, sirina - self.r)
        self.y = random.randint(self.r, visina - self.r)
        self.vx = random.choice([-1, 1]) * brzina
        self.vy = random.choice([-1, 1]) * brzina

    def pomeri(self):
        self.x += self.vx
        self.y += self.vy

        if self.x <= self.r or self.x >= sirina - self.r:
            self.vx *= -1
        if self.y <= self.r or self.y >= visina - self.r:
            self.vy *= -1

    def crtaj(self):
        pygame.draw.circle(prozor, CRVENA, (self.x, self.y), self.r)

# Inicijalizacija objekata
zmija = Zmija()
trenutna_brzina = 1
lopta = Lopta(trenutna_brzina)

# Glavna petlja
while True:
    for dogadjaj in pygame.event.get():
        if dogadjaj.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if dogadjaj.type == pygame.KEYDOWN:
            if dogadjaj.key == pygame.K_LEFT:
                zmija.smer = (-20, 0)
            if dogadjaj.key == pygame.K_RIGHT:
                zmija.smer = (20, 0)
            if dogadjaj.key == pygame.K_UP:
                zmija.smer = (0, -20)
            if dogadjaj.key == pygame.K_DOWN:
                zmija.smer = (0, 20)

    zmija.pomeri()
    lopta.pomeri()

    # Provera kolizije
    glava_x, glava_y = zmija.telo[0]
    if abs(glava_x + 10 - lopta.x) < 15 and abs(glava_y + 10 - lopta.y) < 15:
        zmija.pojedi()
        trenutna_brzina += 1  # poveca brzinu sledece lopte
        lopta = Lopta(trenutna_brzina)

    # Crtanje
    prozor.fill(CRNA)
    zmija.crtaj()
    lopta.crtaj()
    pygame.display.update()
    sat.tick(10)
