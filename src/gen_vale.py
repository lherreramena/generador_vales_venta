from PIL import Image, ImageDraw, ImageFont

def generar_vale(serie="0001", total="$0", salida="vale.png"):
    ancho, alto = 1000, 400
    imagen = Image.new("RGB", (ancho, alto), "white")
    draw = ImageDraw.Draw(imagen)

    # Cargar fuentes (ajusta la ruta si es necesario)
    fuente = ImageFont.truetype("../assets/fonts/PottiSreeramulu.ttf", 20)
    fuente_titulo = ImageFont.truetype("../assets/fonts/PottiSreeramulu.ttf", 28)

    # Sección izquierda
    x_left_seccion = 40
    #draw.text((20, 20), "Centro de Padres Colegio Patrona", font=fuente_titulo, fill="black")
    #draw.text((20, 70), "Alimentos:", font=fuente, fill="black")
    draw.text((x_left_seccion, 100), "[ ] Te/Cafe", font=fuente, fill="black")
    draw.text((x_left_seccion, 130), "[ ] Queque", font=fuente, fill="black")
    draw.text((x_left_seccion, 160), "[ ] Pie/Kuchen", font=fuente, fill="black")
    draw.text((x_left_seccion, 190), "[ ] Torta", font=fuente, fill="black")

    draw.text((20, 200), "Pago:", font=fuente, fill="black")
    draw.text((x_left_seccion, 230), "[ ] Efectivo", font=fuente, fill="black")
    draw.text((x_left_seccion+30, 230), "[ ] Tarjeta", font=fuente, fill="black")
    draw.text((x_left_seccion+60, 230), "[ ] Transferencia", font=fuente, fill="black")

    draw.text((20, 330), f"Serie: {serie}", font=fuente, fill="black")
    draw.text((20, 360), f"Total: {total}", font=fuente, fill="black")

    # Sección derecha
    x_right_seccion = 520
    draw.text((x_right_seccion, 70), "Bingo Solidario 2025", font=fuente_titulo, fill="black")
    #draw.text((x_right_seccion, 110), "COLOQUIO FORMATIVO\nSEMANA DE LA CONVIVENCIA", font=fuente, fill="black")
    #draw.text((x_right_seccion, 160), "MIÉRCOLES 26 DE ABRIL\n12:00 HORAS\nGIMNASIO", font=fuente, fill="black")
    #draw.text((x_right_seccion, 230), "COLEGIO PATRONA", font=fuente, fill="black")
    draw.text((x_right_seccion, 330), f"Serie: {serie}", font=fuente, fill="black")
    draw.text((x_right_seccion, 360), f"Total: {total}", font=fuente, fill="black")

    draw.text((x_right_seccion, 100), "[ ] Te/Cafe", font=fuente, fill="black")
    draw.text((x_right_seccion, 130), "[ ] Queque", font=fuente, fill="black")
    draw.text((x_right_seccion, 160), "[ ] Pie/Kuchen", font=fuente, fill="black")
    draw.text((x_right_seccion, 190), "[ ] Torta", font=fuente, fill="black")

    draw.text((20, 200), "Pago:", font=fuente, fill="black")
    draw.text((x_right_seccion, 230), "[ ] Efectivo", font=fuente, fill="black")
    draw.text((x_right_seccion+30, 230), "[ ] Tarjeta", font=fuente, fill="black")
    draw.text((x_right_seccion+60, 230), "[ ] Transferencia", font=fuente, fill="black")

    draw.text((20, 330), f"Serie: {serie}", font=fuente, fill="black")
    draw.text((20, 360), f"Total: {total}", font=fuente, fill="black")

    imagen.save(salida)
    print(f"Vale guardado como {salida}")

if __name__ == '__main__':
    # Ejemplo de uso
    generar_vale(serie="0025", total="$3.500")
