from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import cm
from reportlab.lib.colors import black, blue, white

def dibujar_contenido_vale(c, folio):
    """
    Dibuja el diseño lógico de un solo vale.
    Base lógica: 19cm ancho x 6.5cm alto (Ligeramente compactado para mejor ajuste)
    """
    # --- VARIABLES DE DISEÑO ---
    ancho_logico = 19 * cm
    alto_logico = 6.5 * cm
    linea_corte_x = 5.2 * cm 
    
    # 1. TALÓN (IZQUIERDA)
    labels = ["Bebidas", "Completos", "Pizzetas"]
    y_base_items = 5.0 * cm
    
    c.setLineWidth(1.5)
    c.setStrokeColor(black)
    
    # Items Talón
    for i, label in enumerate(labels):
        y = y_base_items - (i * 1.1 * cm)
        c.rect(0.2*cm, y, 0.9*cm, 0.65*cm)
        c.setFont("Helvetica", 8)
        c.drawString(1.3*cm, y+0.2*cm, label)

    # Checkboxes Pago Talón
    pagos = ["Efec.", "Tarj.", "Trans."]
    c.setFont("Helvetica", 6)
    c.setLineWidth(0.8)
    for i, pago in enumerate(pagos):
        bx = 0.2*cm + (i * 1.5*cm)
        by = 1.4*cm
        c.rect(bx, by, 0.25*cm, 0.25*cm)
        c.drawString(bx + 0.35*cm, by, pago)

    # Folio Vertical Talón
    c.saveState()
    c.translate(0.7*cm, 0.4*cm)
    c.rotate(90)
    c.setFont("Helvetica", 9)
    c.drawString(0, 0, f"Serie: {folio:04d}")
    c.restoreState()

    # Total Talón
    c.setFont("Helvetica", 9)
    c.drawString(1.5*cm, 0.5*cm, "Total: ______")

    # 2. LÍNEA DE CORTE PUNTEADA
    c.setLineWidth(1)
    c.setDash(3, 3)
    c.line(linea_corte_x, 0, linea_corte_x, alto_logico)
    c.setDash()

    # 3. CUERPO (DERECHA)
    margen_cuerpo = 6.0 * cm
    
    # Items Cuerpo (Grandes)
    c.setLineWidth(1.8)
    for i, label in enumerate(labels):
        y = y_base_items - (i * 1.1 * cm)
        c.rect(margen_cuerpo, y, 1.4*cm, 0.75*cm)
        c.setFont("Helvetica", 13) # Fuente grande
        c.drawString(margen_cuerpo + 1.6*cm, y+0.2*cm, label)

    # Checkboxes Pago Cuerpo
    c.setFont("Helvetica", 10)
    c.setLineWidth(1)
    pagos_full = ["Efectivo", "Tarjeta", "Transferencia"]
    for i, pago in enumerate(pagos_full):
        bx = margen_cuerpo + (i * 3.3*cm)
        by = 1.0*cm
        c.rect(bx, by, 0.45*cm, 0.45*cm)
        c.drawString(bx + 0.6*cm, by+0.12*cm, pago)

    # Folio y Total Cuerpo
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margen_cuerpo, 0.3*cm, f"Serie: {folio:04d}")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margen_cuerpo + 3.0*cm, 0.3*cm, "TOTAL: ______________")

    # 4. LOGOS (Placeholders)
    
    # --- Logo Central (Simulado) ---
    cx, cy = linea_corte_x, 4.2*cm
    radio = 1.3*cm
    # Dibuja un círculo blanco de fondo para tapar la línea punteada si pasa por detrás
    c.setFillColor(white)
    c.circle(cx, cy, radio, fill=1, stroke=0)
    # Dibuja logo azul
    c.setFillColorRGB(0.2, 0.3, 0.7) 
    c.circle(cx, cy, radio, fill=1, stroke=0)
    c.setFillColor(black)
    # --> Poner tu imagen aquí:
    # c.drawImage("logo_centro.png", cx-radio, cy-radio, width=2*radio, height=2*radio, mask='auto')

    
    # --- Poster Festival (Simulado) ---
    px, py = 15.8*cm, 1.8*cm
    pw, ph = 2.8*cm, 4.5*cm
    c.setFillColorRGB(1, 0.95, 0.85)
    c.rect(px, py, pw, ph, fill=1, stroke=0)
    c.setFillColorRGB(0.8, 0.2, 0.2)
    c.drawCentredString(px + pw/2, py + ph - 1*cm, "FESTIVAL")
    c.setFillColor(black)
    # --> Poner tu imagen aquí:
    # c.drawImage("poster.jpg", px, py, width=pw, height=ph, mask='auto')


def generar_hoja_2x4(nombre_archivo, folio_inicial=1):
    # Configuración Hoja: Letter Landscape (27.9cm x 21.6cm)
    hoja_ancho, hoja_alto = landscape(letter)
    c = canvas.Canvas(nombre_archivo, pagesize=landscape(letter))
    
    # GRILLA: 2 Columnas x 4 Filas
    filas = 4
    columnas = 2
    
    # Márgenes reducidos a 0.5cm para aprovechar al máximo la hoja Carta
    margen_x = 0.5 * cm
    margen_y = 0.5 * cm
    
    # Dimensiones de cada celda
    ancho_celda = (hoja_ancho - 2*margen_x) / columnas
    alto_celda = (hoja_alto - 2*margen_y) / filas
    
    # Diseño lógico base (19x6.5)
    base_w = 19 * cm
    base_h = 6.5 * cm
    
    # Factor de escala: "Fit to box" (ajustar a la caja)
    scale_w = (ancho_celda - 0.4*cm) / base_w  # 0.4cm de padding interno
    scale_h = (alto_celda - 0.2*cm) / base_h   # 0.2cm de padding interno
    scale_factor = min(scale_w, scale_h)       # Usar el menor para que no se corte

    folio_actual = folio_inicial

    for fila in range(filas):
        for col in range(columnas):
            # Coordenadas esquina inferior izquierda de la celda
            x_pos = margen_x + (col * ancho_celda)
            # Y crece hacia arriba, calculamos desde arriba hacia abajo
            y_pos = hoja_alto - margen_y - ((fila + 1) * alto_celda)
            
            c.saveState()
            
            # Calcular centrado dentro de la celda
            contenido_w = base_w * scale_factor
            contenido_h = base_h * scale_factor
            pad_x = (ancho_celda - contenido_w) / 2
            pad_y = (alto_celda - contenido_h) / 2
            
            c.translate(x_pos + pad_x, y_pos + pad_y)
            c.scale(scale_factor, scale_factor)
            
            dibujar_contenido_vale(c, folio_actual)
            c.restoreState()
            
            folio_actual += 1

    # --- GUÍAS DE CORTE ---
    c.setStrokeColor(blue)
    c.setLineWidth(0.5)
    long_guia = 0.4 * cm
    
    # Líneas Horizontales (Divisiones + Bordes)
    for i in range(filas + 1):
        y = hoja_alto - margen_y - (i * alto_celda)
        # Solo dibujamos las cruces en los bordes y centro vertical
        c.line(margen_x - long_guia, y, margen_x + long_guia, y) # Izquierda
        c.line(hoja_ancho/2 - long_guia, y, hoja_ancho/2 + long_guia, y) # Centro
        c.line(hoja_ancho - margen_x - long_guia, y, hoja_ancho - margen_x + long_guia, y) # Derecha

    # Líneas Verticales
    for j in range(columnas + 1):
        x = margen_x + (j * ancho_celda)
        c.line(x, hoja_alto - margen_y + long_guia, x, hoja_alto - margen_y - long_guia) # Arriba
        c.line(x, margen_y + long_guia, x, margen_y - long_guia) # Abajo
        # Cruces internas
        for i in range(1, filas):
             y_inter = hoja_alto - margen_y - (i * alto_celda)
             c.line(x, y_inter - long_guia, x, y_inter + long_guia)

    c.save()
    print(f"Generado exitosamente: {nombre_archivo} (2x4 Carta Horizontal)")

if __name__ == "__main__":
    generar_hoja_2x4("vales_carta_2x4.pdf", folio_inicial=1)