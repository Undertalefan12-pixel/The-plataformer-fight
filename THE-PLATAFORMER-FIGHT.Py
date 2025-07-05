#pgzero
import random

WIDTH = 450
HEIGHT = 450
TITLE = "THE PLATAFORMER FIGHT!"
Tile_size = 18
FPS = 45
# ACTORES
personaje = Actor("aliencam", (100, 100))
fondo = Actor("fondo", size=(450, 450))
hongovid = Actor("tile_0128", (50, 200))
bomba = Actor("tile_0008", (300, 200))
corazon1 = Actor("tile_0044", (10, 10))
corazon2 = Actor("tile_0044", (30, 10))
corazon3 = Actor("tile_0044", (50, 10))
enemigos = [Actor("tile_0145", (100, 250))]

# MAPA
my_map = [
    ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],
    ["1","1","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","1","1"],
    ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],
    ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","1"],
    ["1","1","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","1","1"],
    ["1","1","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","1","1","1"],
    ["1","1","1","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","1","1","1","1","1"],
    ["1","1","1","1","0","1","1","1","1","1","1","1","1","1","0","0","0","0","1","1","1","1","1","1"],
    ["0","2","2","0","0","0","0","1","1","1","0","0","0","0","0","1","1","1","1","2","2","0","0","0"],
    ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
]

# ESTADO DEL JUEGO
vidas = 3
vel_y = 0
vel_x = 0
gravedad = 1
en_suelo = False
tiempo = 0
record = 0

def en_el_suelo():
    global en_suelo
    x_tile = int(personaje.x // Tile_size)
    y_tile = int((personaje.y + Tile_size // 2) // Tile_size)
    if 0 <= x_tile < len(my_map[0]) and 0 <= y_tile < len(my_map):
        tile_abajo = my_map[y_tile][x_tile]
        en_suelo = tile_abajo in ["1", "2"]
    else:
        en_suelo = False
    return en_suelo

def agregar_enemigo():
    enemigos.append(Actor("tile_0145", (random.randint(0, WIDTH), random.randint(0, HEIGHT // 2))))

def draw():
    screen.clear()
    fondo.draw()

    for y, fila in enumerate(my_map):
        for x, tile in enumerate(fila):
            if tile == "1":
                screen.blit("tierra", (x * Tile_size, y * Tile_size))
            elif tile == "2":
                screen.blit("tile_0047", (x * Tile_size, y * Tile_size))

    hongovid.draw()
    bomba.draw()
    personaje.draw()
    corazon1.draw()
    corazon2.draw()
    corazon3.draw()

    for enemigo in enemigos:
        enemigo.draw()

    screen.draw.text("Tiempo: " + str(tiempo), topleft=(300, 10), fontsize=20, color="white")
    screen.draw.text("Record: " + str(record), topleft=(300, 30), fontsize=20, color="white")

def update(dt):
    global vel_y, vel_x, vidas, tiempo, record

    # Gravedad
    vel_y += gravedad
    personaje.y += vel_y

    # Suelo
    if en_el_suelo():
        if vel_y > 0:
            vel_y = 0
        if keyboard.up or keyboard.w or keyboard.space:
            if not hasattr(update, 'salto_presionado') or not update.salto_presionado:
                vel_y = -10
                update.salto_presionado = True
        else:
            update.salto_presionado = False

    # Movimiento lateral con fricción
    if keyboard.left or keyboard.a:
        vel_x = max(vel_x - 0.5, -3)
    elif keyboard.right or keyboard.d:
        vel_x = min(vel_x + 0.5, 3)
    else:
        if vel_x > 0:
            vel_x = max(0, vel_x - 0.3)
        elif vel_x < 0:
            vel_x = min(0, vel_x + 0.3)

    personaje.x += vel_x

    # Fuera del mapa = muerte instantánea
    if personaje.y > HEIGHT or personaje.x < 0 or personaje.x > WIDTH:
        vidas = 0

    en_el_suelo()

    # Colisiones
    if personaje.colliderect(hongovid) and vidas < 3:
        vidas += 1
        hongovid.pos = (-100, -100)

    if personaje.colliderect(bomba):
        vidas -= 1
        bomba.pos = (-100, -100)

    for enemigo in enemigos:
        if personaje.x < enemigo.x:
            enemigo.x -= 1
        elif personaje.x > enemigo.x:
            enemigo.x += 1
        if personaje.y < enemigo.y:
            enemigo.y -= 1
        elif personaje.y > enemigo.y:
            enemigo.y += 1

        if personaje.colliderect(enemigo):
            vidas -= 1
            enemigos.remove(enemigo)
            break

    # Corazones
    corazon1.image = "tile_0044" if vidas >= 1 else "tile_0046"
    corazon2.image = "tile_0044" if vidas >= 2 else "tile_0046"
    corazon3.image = "tile_0044" if vidas >= 3 else "tile_0046"

    if vidas <= 0:
        record = max(record, tiempo)
        reset_game()

def reset_game():
    global vidas, tiempo, enemigos, personaje, hongovid, bomba, vel_x, vel_y
    vidas = 3
    tiempo = 0
    vel_x = 0
    vel_y = 0
    personaje.pos = (100, 100)
    enemigos = [Actor("tile_0145", (100, 250))]
    hongovid.pos = (50, 200)
    bomba.pos = (300, 200)

def contar_tiempo():
    global tiempo
    tiempo += 1
    if tiempo % 30 == 0:
        agregar_enemigo()

clock.schedule_interval(contar_tiempo, 1)

#Terminado!  
