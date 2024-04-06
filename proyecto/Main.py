import pygame
import random
import math
from pygame import  mixer
#inicioamos  libreria
pygame.init()

#crear pantalla
pantalla = pygame.display.set_mode((800,600))

#musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)


#Titulo e icono
pygame.display.set_caption('Invacion espacial extraterretre')
icono = pygame.image.load('extraterrestre.png')
pygame.display.set_icon(icono)
#fondo
fondo = pygame.image.load('fondo.jpg')


#juagdor
img_jugador = pygame.image.load(('nave.png'))
jugador_x = 368
jugador_y = 530
jugador_x_cambio= 0


def Jugador(x,y):
    pantalla.blit(img_jugador,(x,y))

#enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 7

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load(('ovni_enemigo.png')))
    enemigo_x.append(random.randint(0,736))
    enemigo_y.append(random.randint(50,200))
    enemigo_x_cambio.append(0.3)
    enemigo_y_cambio.append(50)



def Enemigo(x,y,ene):
    pantalla.blit(img_enemigo[ene],(x,y))

#Disparo
balas = []
img_disparo = pygame.image.load(('bala.png'))
disparo_x = 0
disparo_y = 530
disparo_x_cambio = 0
disparo_y_cambio = 1
bala_visible = False

#Puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf',32)
text_x = 10
text_y = 10

#final de juego
fuente_final = pygame.font.Font('freesansbold.ttf',32)

def tex_final():
    texto_final = fuente.render(f'Juego terminado', True, (255, 255, 255))
    pantalla.blit(texto_final, (60, 200))

#mostrar puntaje
def mostrar_puntaje(x,y):
    texto = fuente.render(f'Puntaje: {puntaje}',True,(255,255,255))
    pantalla.blit(texto,(x,y))

def disparar(x,y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_disparo, (x+16,y+10))

def detectar_coliciones(x_1,y_1,x_2,y_2):
    distancia = math.sqrt(math.pow(x_2-x_1,2)+math.pow(y_2-y_1,2))
    if distancia < 27:
        return True
    else:
        return False

#ciclo del juego
se_ejecuta = True
while se_ejecuta:

    pantalla.blit(fondo,(0,0) )


    #iterar eventos
    for evento in pygame.event.get():
        #evento cerrar programa
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        #evento precion de teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_d:
                jugador_x_cambio = 1

            if evento.key == pygame.K_a:
                jugador_x_cambio = -1

            if evento.key == pygame.K_SPACE:
                if bala_visible == False:
                    sonidobala= mixer.Sound('disparo.mp3')
                    sonidobala.play()
                    nueva_bala = {
                        "x": jugador_x,
                        "y": jugador_y,
                        "velocidad": -5
                    }
                    balas.append(nueva_bala)


        #evento soltar teclas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_d or evento.key == pygame.K_a:
                jugador_x_cambio = 0



    #asignar movimiento en x
    jugador_x += jugador_x_cambio

    #mantener dentro de border
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736


    # asignar movimiento en x enemigo
    for e in range(cantidad_enemigos):
        if enemigo_y[e] >= 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            tex_final()
            break
        enemigo_x[e] += enemigo_x_cambio[e]
        # mantener dentro de border
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.5
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.5

        # colision
        for bala in balas:
            colision_bala_enemigo = detectar_coliciones(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound("Golpe.mp3")
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(20, 200)
                break

        Enemigo(enemigo_x[e], enemigo_y[e],e)




    #movimiento de balda
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_disparo, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)



    #perdio


    Jugador(jugador_x,jugador_y)

    mostrar_puntaje(text_x,text_y)

    pygame.display.update()