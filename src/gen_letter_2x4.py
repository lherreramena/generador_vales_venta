from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import cm
from reportlab.lib.colors import black, blue, white

def dibujar_contenido_vale(c, folio):
    """
    Dibuja el diseño lógico de un solo vale.
    Base lógica: 19cm ancho x 6.5cm alto
    """
    # --- VARIABLES DE DISEÑO ---
    ancho_logico = 19 * cm
    alto_logico = 6.5 * cm
    linea_corte_x = 5.2 * cm 
    
    # --- 1. LISTA DE ÍTEMS (Ahora son 4) ---
    labels = ["Bebidas", "Completos", "Pizzetas", "Agua Mineral"]
    
    # Ajustamos la altura inicial un poco más arriba para que quepan los 4
    y_base_items = 5.4 * cm 
    
    # Espacio entre ítems (Reducido levemente de 1.1 a 0.95 para que quepan 4)
    item_step = 0.95 * cm

    c.setLineWidth(1.5)
    c.setStrokeColor(black)
    
    # --- DIBUJAR TALÓN (IZQUIERDA) ---
    for i, label in enumerate(labels):
        y = y_base_items - (i * item_step)
        # Cuadrito Talón
        c.rect(0.2*cm, y, 0.9*cm, 0.6*cm) 
        # Texto Talón
        c.setFont("Helvetica", 8)
        c.drawString(1.3*cm, y+0.15*cm, label)

    # Checkboxes Pago Talón (Bajamos un poco la Y para dar aire al 4to ítem)
    pagos = ["Efec.", "Tarj.", "Trans."]
    c.setFont("Helvetica", 6)
    c.setLineWidth(0.8)
    for i, pago in enumerate(pagos):
        bx = 0.2*cm + (i * 1.5*cm)
        by = 1.4*cm # Altura de los checkboxes
        c.rect(bx, by, 0.25*cm, 0.25*cm)
        c.drawString(bx + 0.35*cm, by, pago)

    # Folio Horizontal Talón
    c.setFont("Helvetica-Bold", 9)
    c.drawString(0.2*cm, 0.8*cm, f"Serie: {folio:04d}")

    # Total Talón
    c.setFont("Helvetica", 9)
    c.drawString(0.2*cm, 0.3*cm, "Total: ______")


    # --- 2. LÍNEA DE CORTE PUNTEADA ---
    c.setLineWidth(1)
    c.setDash(3, 3)
    c.line(linea_corte_x, 0, linea_corte_x, alto_logico)
    c.setDash()


    # --- 3. DIBUJAR CUERPO (DERECHA) ---
    
    # Margen derecho amplio para salvar el logo
    margen_cuerpo = 7.2 * cm 
    
    # Items Cuerpo
    c.setLineWidth(1.8)
    for i, label in enumerate(labels):
        y = y_base_items - (i * item_step)
        # Cuadro Grande
        c.rect(margen_cuerpo, y, 1.4*cm, 0.7*cm)
        # Texto Grande
        c.setFont("Helvetica", 13) 
        c.drawString(margen_cuerpo + 1.6*cm, y+0.2*cm, label)

    # Checkboxes Pago Cuerpo
    c.setFont("Helvetica", 10)
    c.setLineWidth(1)
    pagos_full = ["Efectivo", "Tarjeta", "Transferencia"]
    for i, pago in enumerate(pagos_full):
        bx = margen_cuerpo + (i * 3.3*cm)
        by = 1.0*cm # Altura checkboxes cuerpo
        c.rect(bx, by, 0.45*cm, 0.45*cm)
        c.drawString(bx + 0.6*cm, by+0.12*cm, pago)

    # Folio y Total Cuerpo
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margen_cuerpo, 0.3*cm, f"Serie: {folio:04d}")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margen_cuerpo + 3.0*cm, 0.3*cm, "TOTAL: ______________")


    # --- 4. LOGOS (Placeholders) ---
    
    # Logo Central (Simulado)
    cx, cy = linea_corte_x, 4.2*cm
    radio = 1.4*cm 
    
    c.setFillColor(white)
    c.circle(cx, cy, radio, fill=1, stroke=0) # Fondo blanco
    
    c.setFillColorRGB(0.2, 0.3, 0.7) 
    c.circle(cx, cy, radio, fill=1, stroke=0) # Logo simulado
    c.setFillColor(black)
    
    # --> Poner tu imagen aquí:
    # c.drawImage("logo_centro.png", cx-radio, cy-radio, width=2*radio, height=2*radio, mask='auto')
    
    # Poster Festival (Derecha extrema)
    px, py = 16.0*cm, 1.8*cm
    pw, ph = 2.8*cm, 4.5*cm
    
    c.setFillColorRGB(1, 0.95, 0.85)
    c.rect(px, py, pw, ph, fill=1, stroke=0) # Poster simulado
    c.setFillColorRGB(0.8, 0.2, 0.2)
    c.drawCentredString(px + pw/2, py + ph - 1*cm, "FESTIVAL")
    c.setFillColor(black)
    
    # --> Poner tu imagen aquí:
    # c.drawImage("poster.jpg", px, py, width=pw, height=ph, mask='auto')


def generar_hoja_4items(nombre_archivo, folio_inicial=1):
    # Configuración Hoja: Letter Landscape
    hoja_ancho, hoja_alto = landscape(letter)
    c = canvas.Canvas(nombre_archivo, pagesize=landscape(letter))
    
    # Grilla 2 columnas x 4 filas
    filas = 4
    columnas = 2
    margen_x = 0.5 * cm
    margen_y = 0.5 * cm
    
    ancho_celda = (hoja_ancho - 2*margen_x) / columnas
    alto_celda = (hoja_alto - 2*margen_y) / filas
    
    # Escala Fit-to-box
    base_w = 19 * cm
    base_h = 6.5 * cm
    scale_w = (ancho_celda - 0.4*cm) / base_w 
    scale_h = (alto_celda - 0.2*cm) / base_h   
    scale_factor = min(scale_w, scale_h)

    folio_actual = folio_inicial

    for fila in range(filas):
        for col in range(columnas):
            x_pos = margen_x + (col * ancho_celda)
            y_pos = hoja_alto - margen_y - ((fila + 1) * alto_celda)
            
            c.saveState()
            
            contenido_w = base_w * scale_factor
            contenido_h = base_h * scale_factor
            pad_x = (ancho_celda - contenido_w) / 2
            pad_y = (alto_celda - contenido_h) / 2
            
            c.translate(x_pos + pad_x, y_pos + pad_y)
            c.scale(scale_factor, scale_factor)
            
            dibujar_contenido_vale(c, folio_actual)
            c.restoreState()
            folio_actual += 1

    # Guías de corte
    c.setStrokeColor(blue)
    c.setLineWidth(0.5)
    long_guia = 0.4 * cm
    
    # Horizontales
    for i in range(filas + 1):
        y = hoja_alto - margen_y - (i * alto_celda)
        c.line(margen_x - long_guia, y, margen_x + long_guia, y)
        c.line(hoja_ancho/2 - long_guia, y, hoja_ancho/2 + long_guia, y)
        c.line(hoja_ancho - margen_x - long_guia, y, hoja_ancho - margen_x + long_guia, y)

    # Verticales
    for j in range(columnas + 1):
        x = margen_x + (j * ancho_celda)
        c.line(x, hoja_alto - margen_y + long_guia, x, hoja_alto - margen_y - long_guia)
        c.line(x, margen_y + long_guia, x, margen_y - long_guia)
        for i in range(1, filas):
             y_inter = hoja_alto - margen_y - (i * alto_celda)
             c.line(x, y_inter - long_guia, x, y_inter + long_guia)

    c.save()
    print(f"¡Listo! Archivo creado con 4 ítems: {nombre_archivo}")

if __name__ == "__main__":
    generar_hoja_4items("vales_4items_final.pdf", folio_inicial=1)