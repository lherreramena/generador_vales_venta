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
    
    # --- 1. TALÓN (IZQUIERDA) ---
    labels = ["Bebidas", "Completos", "Pizzetas"]
    y_base_items = 5.2 * cm
    
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
        by = 1.8*cm
        c.rect(bx, by, 0.25*cm, 0.25*cm)
        c.drawString(bx + 0.35*cm, by, pago)

    # --- CAMBIO 1: FOLIO HORIZONTAL EN EL TALÓN ---
    # Ya no rotamos ni trasladamos el canvas. Lo escribimos directo abajo.
    c.setFont("Helvetica-Bold", 9)
    c.drawString(0.2*cm, 0.9*cm, f"Serie: {folio:04d}")

    # Total Talón (Alineado a la izquierda abajo del folio)
    c.setFont("Helvetica", 9)
    c.drawString(0.2*cm, 0.3*cm, "Total: ______")


    # --- 2. LÍNEA DE CORTE PUNTEADA ---
    c.setLineWidth(1)
    c.setDash(3, 3)
    c.line(linea_corte_x, 0, linea_corte_x, alto_logico)
    c.setDash()


    # --- 3. CUERPO (DERECHA) ---
    
    # --- CAMBIO 2: MARGEN DERECHO AUMENTADO ---
    # Antes era 6.0, lo subimos a 7.2 para salvar el logo
    margen_cuerpo = 7.2 * cm 
    
    # Items Cuerpo (Grandes)
    c.setLineWidth(1.8)
    for i, label in enumerate(labels):
        y = y_base_items - (i * 1.1 * cm)
        c.rect(margen_cuerpo, y, 1.4*cm, 0.75*cm)
        c.setFont("Helvetica", 13) 
        c.drawString(margen_cuerpo + 1.6*cm, y+0.2*cm, label)

    # Checkboxes Pago Cuerpo (Moviéndolos también a la derecha)
    c.setFont("Helvetica", 10)
    c.setLineWidth(1)
    pagos_full = ["Efectivo", "Tarjeta", "Transferencia"]
    for i, pago in enumerate(pagos_full):
        # Ajustamos el espaciado para que quepan bien desde el nuevo margen
        bx = margen_cuerpo + (i * 3.3*cm)
        by = 1.2*cm
        c.rect(bx, by, 0.45*cm, 0.45*cm)
        c.drawString(bx + 0.6*cm, by+0.12*cm, pago)

    # Folio y Total Cuerpo
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margen_cuerpo, 0.3*cm, f"Serie: {folio:04d}")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margen_cuerpo + 3.0*cm, 0.3*cm, "TOTAL: ______________")


    # --- 4. LOGOS (Placeholders) ---
    
    # Logo Central (Simulado)
    # Va centrado en la línea de corte (5.2)
    cx, cy = linea_corte_x, 4.2*cm
    radio = 1.4*cm 
    
    # Círculo blanco de fondo (tapa la línea punteada)
    c.setFillColor(white)
    c.circle(cx, cy, radio, fill=1, stroke=0)
    
    # Logo azul placeholder
    c.setFillColorRGB(0.2, 0.3, 0.7) 
    c.circle(cx, cy, radio, fill=1, stroke=0)
    c.setFillColor(black)
    
    # --> Poner tu imagen aquí (Descomentar y ajustar ruta):
    # c.drawImage("logo_centro.png", cx-radio, cy-radio, width=2*radio, height=2*radio, mask='auto')

    
    # Poster Festival (Derecha extrema)
    px, py = 16.0*cm, 1.8*cm
    pw, ph = 2.8*cm, 4.5*cm
    
    # Placeholder Poster
    c.setFillColorRGB(1, 0.95, 0.85)
    c.rect(px, py, pw, ph, fill=1, stroke=0)
    c.setFillColorRGB(0.8, 0.2, 0.2)
    c.drawCentredString(px + pw/2, py + ph - 1*cm, "FESTIVAL")
    c.setFillColor(black)
    
    # --> Poner tu imagen aquí:
    # c.drawImage("poster.jpg", px, py, width=pw, height=ph, mask='auto')


def generar_hoja_final(nombre_archivo, folio_inicial=1):
    # Hoja Carta Horizontal
    hoja_ancho, hoja_alto = landscape(letter)
    c = canvas.Canvas(nombre_archivo, pagesize=landscape(letter))
    
    # Grilla 2x4
    filas = 4
    columnas = 2
    margen_x = 0.5 * cm
    margen_y = 0.5 * cm
    
    ancho_celda = (hoja_ancho - 2*margen_x) / columnas
    alto_celda = (hoja_alto - 2*margen_y) / filas
    
    # Lógica de escalado "Fit to box"
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
    
    for i in range(filas + 1):
        y = hoja_alto - margen_y - (i * alto_celda)
        c.line(margen_x - long_guia, y, margen_x + long_guia, y)
        c.line(hoja_ancho/2 - long_guia, y, hoja_ancho/2 + long_guia, y)
        c.line(hoja_ancho - margen_x - long_guia, y, hoja_ancho - margen_x + long_guia, y)

    for j in range(columnas + 1):
        x = margen_x + (j * ancho_celda)
        c.line(x, hoja_alto - margen_y + long_guia, x, hoja_alto - margen_y - long_guia)
        c.line(x, margen_y + long_guia, x, margen_y - long_guia)
        for i in range(1, filas):
             y_inter = hoja_alto - margen_y - (i * alto_celda)
             c.line(x, y_inter - long_guia, x, y_inter + long_guia)

    c.save()
    print(f"¡Listo! Archivo creado: {nombre_archivo}")

if __name__ == "__main__":
    generar_hoja_final("vales_definitivo_v3.pdf", folio_inicial=1)