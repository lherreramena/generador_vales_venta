from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import black, lightgrey

def dibujar_vale(nombre_archivo, folio_inicio=1):
    # Configuración del tamaño del lienzo (Ancho x Alto). 
    # Usaremos un tamaño personalizado ancho y bajo, similar a un talonario.
    ancho = 22 * cm
    alto = 8 * cm
    c = canvas.Canvas(nombre_archivo, pagesize=(ancho, alto))

    # --- COORDENADAS Y VARIABLES ---
    linea_corte_x = 5.5 * cm  # Donde va la línea punteada
    margen_izq_talon = 0.5 * cm
    margen_izq_cuerpo = 7.5 * cm
    
    # Posiciones Y para los items (de arriba a abajo)
    #y_items = [6.5*cm, 5.2*cm, 3.9*cm]
    y_items = [6.6*cm, 5.4*cm, 4.2*cm, 3.0*cm]
    labels = ["Aguas", "Bebidas", "Completos", "Pizzetas"]

    # --- 1. DIBUJAR TALÓN (IZQUIERDA) ---
    
    # Cuadros de items (Talón)
    c.setLineWidth(2)
    for i, label in enumerate(labels):
        y = y_items[i]
        # Cuadro
        c.rect(margen_izq_talon, y, 1.2*cm, 0.8*cm)
        # Texto
        c.setFont("Helvetica", 10)
        #c.drawString(margen_izq_talon + 1.4*cm, y + 0.2*cm, label)
        c.drawString(margen_izq_talon + 1.4*cm, y, label)

    # Checkboxes de pago (Talón)
    tipos_pago = ["Efectivo", "Tarjeta", "Transferencia"]
    c.setFont("Helvetica", 7)
    c.setLineWidth(1)
    start_x_pago = margen_izq_talon
    for i, pago in enumerate(tipos_pago):
        # Checkbox pequeño
        c.rect(start_x_pago + (i * 1.6*cm), 2.8*cm, 0.3*cm, 0.3*cm)
        c.drawString(start_x_pago + (i * 1.6*cm) + 0.4*cm, 2.8*cm, pago)

    # Folio Vertical (Talón)
    c.saveState()
    c.translate(1.5*cm, 0.5*cm)
    c.rotate(90)
    c.setFont("Helvetica", 12)
    c.drawString(0, 0, f"Serie: {folio_inicio:04d}")
    c.restoreState()

    # Total (Talón)
    c.setFont("Helvetica", 12)
    c.drawString(2.5*cm, 0.8*cm, "Total: _________")


    # --- 2. LÍNEA DE CORTE CENTRAL ---
    c.setLineWidth(1)
    c.setDash(3, 3) # Patrón punteado
    c.line(linea_corte_x, 0, linea_corte_x, alto)
    c.setDash() # Restaurar línea sólida


    # --- 3. DIBUJAR CUERPO PRINCIPAL (DERECHA) ---

    # Cuadros de items (Cuerpo) grandes
    c.setLineWidth(2.5)
    for i, label in enumerate(labels):
        y = y_items[i]
        # Cuadro grande
        c.rect(margen_izq_cuerpo, y, 2.0*cm, 1.0*cm)
        # Texto grande
        c.setFont("Helvetica", 16)
        c.drawString(margen_izq_cuerpo + 2.2*cm, y + 0.3*cm, label)

    # Checkboxes de pago (Cuerpo) grandes
    c.setFont("Helvetica", 14)
    c.setLineWidth(1.5)
    start_x_pago_cuerpo = margen_izq_cuerpo + 0.5*cm
    for i, pago in enumerate(tipos_pago):
        offset = i * 3.5*cm
        # Checkbox grande
        c.rect(start_x_pago_cuerpo + offset, 1.8*cm, 0.7*cm, 0.7*cm)
        c.drawString(start_x_pago_cuerpo + offset + 0.9*cm, 2.0*cm, pago)

    # Folio y Total (Cuerpo)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(8.5*cm, 0.5*cm, f"Serie: {folio_inicio:04d}")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(11.5*cm, 0.5*cm, "TOTAL: _________________")


    # --- 4. LOGOTIPOS (Simuladores) ---
    # Nota: Para usar tus imágenes reales, descomenta las líneas 'drawImage' 
    # y comenta los bloques de dibujo geométrico.

    # A) Logo Central (Centro de Padres)
    # Este logo va centrado en la línea de corte
    cx, cy = linea_corte_x, 5.5*cm
    radio = 1.8*cm
    
    # --- Simulación del logo (Circulo azul) ---
    c.setFillColorRGB(0.2, 0.3, 0.6) # Azul
    c.circle(cx, cy, radio, fill=1, stroke=0)
    c.setFillColor(black) # Reset color
    # Texto simulado en curva es complejo, ponemos texto plano por ahora
    c.setFont("Helvetica-Bold", 8)
    c.setFillColorRGB(1,1,1)
    c.drawCentredString(cx, cy, "LOGO CENTRO")
    c.drawCentredString(cx, cy-10, "DE PADRES")
    c.setFillColor(black)
    # -------------------------------------------
    
    # Para poner tu imagen real del logo central usa:
    c.drawImage("./assets/img/logo.png", cx-radio, cy-radio, width=2*radio, height=2*radio, mask='auto')


    # B) Logo Derecho (Festival)
    # Va a la derecha extrema
    rect_x = 18*cm
    rect_y = 2.5*cm
    rect_w = 3.5*cm
    rect_h = 5*cm
    
    # --- Simulación del Poster (Rectangulo rosa) ---
    c.setFillColorRGB(1, 0.9, 0.8) # Beige claro
    c.rect(rect_x, rect_y, rect_w, rect_h, fill=1, stroke=0)
    c.setFillColorRGB(0.8, 0.2, 0.2)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(rect_x + rect_w/2, rect_y + 4*cm, "Festival")
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawCentredString(rect_x + rect_w/2, rect_y + 3.5*cm, "DE LA VOZ")
    # -------------------------------------------

    # Para poner tu imagen real del poster usa:
    # c.drawImage("ruta/a/tu_poster.jpg", rect_x, rect_y, width=rect_w, height=rect_h, mask='auto')

    c.save()
    print(f"¡Listo! Archivo '{nombre_archivo}' generado correctamente.")

# Ejecutar la función
if __name__ == "__main__":
    dibujar_vale("vale_patrona_lourdes.pdf", folio_inicio=1)
