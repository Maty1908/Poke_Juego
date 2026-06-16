
import pygame
import sys

pygame.init()

# ---------------- VENTANA ----------------
ANCHO = 1440
ALTO = 900

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Poke-Unsam")

# ---------------- FONDO ----------------
fondo = pygame.image.load(r"C:\Users\Ramiro\Desktop\campus animado.gif")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

# ---------------- FUENTES ----------------

# Opciones del menú
fuente = pygame.font.Font(
    r"C:\Users\Ramiro\Desktop\PressStart2P.ttf",
    25
)

# SOLO para el título
fuente_titulo = pygame.font.Font(
    r"C:\Users\Ramiro\Desktop\PressStart2P.ttf",
    100
)

# Para Juego, Tienda y Gracias
fuente_pantallas = pygame.font.Font(
    r"C:\Users\Ramiro\Desktop\PressStart2P.ttf",
    30
)

# ---------------- ESTADO ACTUAL ----------------
estado = "menu"

# ---------------- OPCIONES ----------------
opciones = ["Comenzar Juego", "Tienda", "Gracias", "Salir"]

# Lista de botones
botones = []

# Reloj
reloj = pygame.time.Clock()

while True:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Click del mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:

            if estado == "menu":

                x_mouse, y_mouse = pygame.mouse.get_pos()

                for i, boton in enumerate(botones):

                    if boton.collidepoint(x_mouse, y_mouse):

                        if opciones[i] == "Comenzar Juego":
                            estado = "juego"

                        elif opciones[i] == "Tienda":
                            estado = "tienda"

                        elif opciones[i] == "Gracias":
                            estado = "gracias"

                        elif opciones[i] == "Salir":
                            pygame.quit()
                            sys.exit()

        # ESC para volver al menú
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                estado = "menu"

    # ---------------- MENÚ ----------------
    if estado == "menu":

        pantalla.blit(fondo, (0, 0))

        # Oscurecer el fondo
        capa = pygame.Surface((ANCHO, ALTO))
        capa.set_alpha(80)
        capa.fill((0, 0, 0))
        pantalla.blit(capa, (0, 0))

        # Sombra del título
        sombra = fuente_titulo.render(
            "Poke-Unsam",
            True,
            (0, 0, 0)
        )

        pantalla.blit(
            sombra,
            (
                ANCHO // 2 - sombra.get_width() // 2 + 4,
                108
            )
        )

        # Título principal
        titulo = fuente_titulo.render(
            "Poke-Unsam",
            True,
            (0, 100, 255)
        )

        pantalla.blit(
            titulo,
            (
                ANCHO // 2 - titulo.get_width() // 2,
                100
            )
        )

        botones = []

        for i, opcion in enumerate(opciones):

            x = ANCHO // 2 - 200
            y = 280 + i * 125

            rect = pygame.Rect(
                x,
                y,
                350,
                50
            )

            # Resaltar botón con el mouse
            if rect.collidepoint(pygame.mouse.get_pos()):

                pygame.draw.rect(
                    pantalla,
                    (255, 220, 0),
                    rect,
                    border_radius=15
                )

                color_texto = (0, 0, 0)

            else:

                pygame.draw.rect(
                    pantalla,
                    (0, 0, 0),
                    rect,
                    border_radius=15
                )

                color_texto = (255, 255, 255)

            texto = fuente.render(
                opcion,
                True,
                color_texto
            )

            pantalla.blit(
                texto,
                (
                    rect.centerx - texto.get_width() // 2,
                    rect.centery - texto.get_height() // 2
                )
            )

            botones.append(rect)

    # ---------------- JUEGO ----------------
    elif estado == "juego":

        pantalla.fill((0, 0, 0))

        texto = fuente_pantallas.render(
            "Aca debera estar: Juego",
            True,
            (255, 255, 255)
        )

        pantalla.blit(
            texto,
            (
                ANCHO // 2 - texto.get_width() // 2,
                ALTO // 2 - texto.get_height() // 2
            )
        )

    # ---------------- TIENDA ----------------
    elif estado == "tienda":

        pantalla.fill((0, 0, 0))

        texto = fuente_pantallas.render(
            "Aca debera estar: Tienda",
            True,
            (255, 255, 255)
        )

        pantalla.blit(
            texto,
            (
                ANCHO // 2 - texto.get_width() // 2,
                ALTO // 2 - texto.get_height() // 2
            )
        )

    # ---------------- GRACIAS ----------------
    elif estado == "gracias":

        pantalla.fill((0, 0, 0))

        texto = fuente_pantallas.render(
            "Aca debera estar: Gracias",
            True,
            (255, 255, 255)
        )

        pantalla.blit(
            texto,
            (
                ANCHO // 2 - texto.get_width() // 2,
                ALTO // 2 - texto.get_height() // 2
            )
        )

    pygame.display.update()
    reloj.tick(60)

