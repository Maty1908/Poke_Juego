import io
import json
import tkinter as tk
from tkinter import messagebox
from urllib.request import Request, urlopen
from PIL import Image, ImageTk, ImageSequence

ventana = tk.Tk()                                                           # Configuración de la ventana principal
ventana.title("Poke Pelea")                                                 # Agrego un titulo a la ventana
ventana.geometry("1064x584")                                                # Configuro el tamaño de la ventana

canvas = tk.Canvas(ventana, width=1064, height=584, highlightthickness=0)
canvas.pack(fill="both", expand=True)

imagen_fondo_original = Image.open("fondo.png").resize((1064, 584), Image.Resampling.NEAREST)
fondo_pantalla = ImageTk.PhotoImage(imagen_fondo_original)

canvas.create_image(0, 0, image=fondo_pantalla, anchor="nw")

pokemon_rival_id = canvas.create_image(750, 200, anchor="center")
pokemon_mio_id = canvas.create_image(300, 300, anchor="center")

gif_rival = []      # Destino un almacen para el gif del rival 
gif_mio = []        # Destino un almacen para el gif del propio

index_rival = 0     # Tiempo inicial del gif del rival
index_mio = 0       # Tiempo inicial del gif del propio

url_1 = "https://pokeapi.co/api/v2/pokemon/" + input("Ingrese el nombre del pokemon: ")   # URL del pokemon mio
url_mio = url_1           
url_rival = "https://pokeapi.co/api/v2/pokemon/alakazam"

def cargar_gifs():
    global gif_rival, gif_mio   # Se usa para poder modificar variales initialized afuera

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"} # Evita que la api te bloquee

    try:
        # --- Carga del rival ---
        requests_rival = Request(url_rival, headers=headers)                                 # Pasamos la url a un request
        with urlopen(requests_rival) as respuesta_r:                                         # Abrimos la url y obtenemos la respuesta
            datos_rival = json.loads(respuesta_r.read().decode("utf-8"))     # decodificamos la respuesta

        gif_url_rival = datos_rival["sprites"]["versions"]["generation-v"][  # Busca los datos rel gif 
            "black-white"]["animated"]["front_default"]

        requests_gif_r = Request(gif_url_rival, headers=headers)             # Hace una peticion
        with urlopen(requests_gif_r) as respuesta_gif_r:                                     # Abre la url del gif y obtiene la respuesta
            img_original_r = Image.open(io.BytesIO(respuesta_gif_r.read()))  # Carga la imagen del gif en un espacio de la memoria

        gif_rival.clear()                                                                    # Vacia la lista del pokemon anterior 
        for f in ImageSequence.Iterator(img_original_r):                                     # Recorre cada frame del gif original
            f_rgba = f.convert("RGBA").resize(                                               # Agranda la imagen manteniendo la calidad
                (250, 250), Image.Resampling.NEAREST
            )
            gif_rival.append(ImageTk.PhotoImage(f_rgba))                                     # cambia a formato tinker y lo guarda en la memoria

        # --- Carga del mio ---
        req_mio = Request(url_mio, headers=headers)
        with urlopen(req_mio) as respuesta_m:
            datos_mio = json.loads(respuesta_m.read().decode("utf-8"))

        gif_url_mio = datos_mio["sprites"]["versions"]["generation-v"][
            "black-white"
        ]["animated"]["back_default"]

        req_gif_m = Request(gif_url_mio, headers=headers)
        with urlopen(req_gif_m) as respuesta_gif_m:
            img_original_m = Image.open(io.BytesIO(respuesta_gif_m.read()))

        gif_mio.clear()                                           
        for f in ImageSequence.Iterator(img_original_m):
            f_rgba = f.convert("RGBA").resize(
                (350, 350), Image.Resampling.NEAREST
            )
            gif_mio.append(ImageTk.PhotoImage(f_rgba))

        animar_combate()                                     

    except Exception as e:
        print(f"Error al cargar los GIFs: {e}")


def animar_combate():
    global index_rival, index_mio, gif_rival, gif_mio

    if gif_rival:
        canvas.itemconfig(pokemon_rival_id, image=gif_rival[index_rival])
        index_rival = (index_rival + 1) % len(gif_rival)

    if gif_mio:
        canvas.itemconfig(pokemon_mio_id, image=gif_mio[index_mio])
        index_mio = (index_mio + 1) % len(gif_mio)

    ventana.after(90, animar_combate)


cargar_gifs()

ventana.mainloop()
