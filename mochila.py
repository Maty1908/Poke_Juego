import pygame
import estilo


blanco = (255,255,255)

def inicializar_menu():
    return {
        "abierto": False,
        "seccion": "PRINCIPAL",  # "PRINCIPAL", "POKEMONS", "OBJETOS"
        "indice_seleccionado": 0,
        "fuente": pygame.font.Font("tipografia/pokemon_font.ttf", 20),
        "fuente_chica": pygame.font.Font("tipografia/pokemon_font.ttf", 16)
    }

def dibujar_menu(ventana, jugador, menu):
    """
    Maneja la lógica visual y el renderizado del menú.
    Modifica el diccionario 'menu' internamente.
    """
    # Si el menú no está abierto, no dibujamos nada
    if not menu["abierto"]:
        return

    # --- CONFIGURACIÓN VISUAL DEL CONTENEDOR ---
    ancho_menu = 250
    x_menu = estilo.ANCHO_VENTANA - ancho_menu
    
    # Fondo del menú (Gris oscuro con borde blanco)
    rect_menu = pygame.Rect(x_menu, 0, ancho_menu, estilo.ALTO_VENTANA)
    pygame.draw.rect(ventana, (30, 30, 30), rect_menu)
    pygame.draw.rect(ventana, blanco, rect_menu, 4)

    fuente_menu = menu["fuente"]
    fuente_chica = menu["fuente_chica"]

    # --- SECCIÓN: PRINCIPAL ---
    if menu["seccion"] == "PRINCIPAL":
        txt_titulo = fuente_menu.render("MENU", True, blanco)
        ventana.blit(txt_titulo, (x_menu + 20, 30))

        opciones = ["1. POKEMONS", "2. OBJETOS"]
        for i, opc in enumerate(opciones):
            color = (255, 215, 0) if i == menu["indice_seleccionado"] else blanco
            txt_opc = fuente_menu.render(opc, True, color)
            ventana.blit(txt_opc, (x_menu + 30, 100 + i * 40))
        
        txt_ayuda = fuente_chica.render("[C] Entrar  [X] Salir", True, (150, 150, 150))
        ventana.blit(txt_ayuda, (x_menu + 20, estilo.ALTO_VENTANA - 40))

    # --- SECCIÓN: POKÉMONS ---
    elif menu["seccion"] == "POKEMONS":
        txt_titulo = fuente_menu.render("MIS POKEMONS", True, blanco)
        ventana.blit(txt_titulo, (x_menu + 20, 30))

        lista_pokes = jugador.pokemons[:6]
        if not lista_pokes:
            txt_vacio = fuente_chica.render("No tenes Pokemons", True, (255, 100, 100))
            ventana.blit(txt_vacio, (x_menu + 25, 100))
        else:
            for i, poke in enumerate(lista_pokes):
                nombre_poke = poke.nombre
                txt_poke = fuente_menu.render(f"{i+1}. {nombre_poke}", True, blanco)
                ventana.blit(txt_poke, (x_menu + 25, 100 + i * 35))

        txt_ayuda = fuente_menu.render("[X] Volver", True, (150, 150, 150))
        ventana.blit(txt_ayuda, (x_menu + 20, estilo.ALTO_VENTANA - 40))

    # --- SECCIÓN: OBJETOS ---
    elif menu["seccion"] == "OBJETOS":
        txt_titulo = fuente_menu.render("MIS OBJETOS", True, blanco)
        ventana.blit(txt_titulo, (x_menu + 20, 30))

        y_item = 100
        for item, cantidad in jugador.inventario.items():
            txt_item = fuente_menu.render(f"{item.capitalize()}: x{cantidad}", True, blanco)
            ventana.blit(txt_item, (x_menu + 25, y_item))
            y_item += 40

        txt_ayuda = fuente_menu.render("[X] Volver", True, (150, 150, 150))
        ventana.blit(txt_ayuda, (x_menu + 20, estilo.ALTO_VENTANA - 40))