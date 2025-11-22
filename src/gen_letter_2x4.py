from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import cm
from reportlab.lib.colors import black, blue, white
import math

def dibujar_contenido_vale(c, folio):
    """
    Dibuja el diseño lógico de un solo vale.
    (Misma función que aprobaste, con 4 items y ajustes de posición)
    """
    # --- VARIABLES DE DISEÑO ---
    ancho_logico = 19 * cm
    alto_logico = 6.5 * cm
    linea_corte_x = 5.2 * cm 
    
    # Items (4 productos)
    labels = ["Bebidas", "Completos", "Pizzetas", "Agua Mineral"]
    y_base_items = 5.4 * cm 
    item_step = 0.95 * cm

    c.setLineWidth(1.5)
    c.setStrokeColor(black)
    
    # --- TALÓN (IZQUIERDA) ---
    for i, label in enumerate(labels):
        y = y_base_items - (i * item_step)
        c.rect(0.2*cm, y, 0.9*cm, 0.6*cm) 
        c.setFont("Helvetica", 8)
        c.drawString(1.3*cm, y+0.15*cm, label)

    # Checkboxes Pago Talón
    pagos = ["Efec.", "Tarj.", "Trans."]
    c.setFont("Helvetica", 6)
    c.setLineWidth(0.8)
    for i, pago in enumerate(pagos):
        bx = 0.2*cm + (i * 1.5*cm)
        by = 1.4*cm 
        c.rect(bx, by, 0.25*cm, 0.25*cm)
        c.drawString(bx + 0.35*cm, by, pago)

    # Folio Horizontal Talón
    c.setFont("Helvetica-Bold", 9)
    c.drawString(0.2*cm, 0.8*cm, f"Serie: {folio:04d}")

    # Total Talón
    c.setFont("Helvetica", 9)
    c.drawString(0.2*cm, 0.3*cm, "Total: ______")

    # Línea de corte punteada
    c.setLineWidth(1)
    c.setDash(3, 3)
    c.line(linea_corte_x, 0, linea_corte_x, alto_logico)
    c.setDash()

    # --- CUERPO (DERECHA) ---
    margen_cuerpo = 7.2 * cm 
    
    # Items Cuerpo
    c.setLineWidth(1.8)
    for i, label in enumerate(labels):
        y = y_base_items - (i * item_step)
        c.rect(margen_cuerpo, y, 1.4*cm, 0.7*cm)
        c.setFont("Helvetica", 13) 
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

    # --- LOGOS (Simulados) ---
    
    # Logo Central
    cx, cy = linea_corte_x, 4.2*cm
    radio = 1.4*cm 
    c.setFillColor(white)
    c.circle(cx, cy, radio, fill=1, stroke=0)
    # c.drawImage("logo_centro.png", cx-radio, cy-radio, width=2*radio, height=2*radio, mask='auto')
    
    # Poster Festival
    px, py = 16.0*cm, 1.8*cm
    pw, ph = 2.8*cm, 4.5*cm
    c.setFillColorRGB(1, 0.95, 0.85) # Color simulado
    c.rect(px, py, pw, ph, fill=1, stroke=0)
    # c.drawImage("poster.jpg", px, py, width=pw, height=ph, mask='auto')
    
    # Restaurar color negro
    c.setFillColor(black)


def generar_lote_masivo(nombre_archivo, cantidad_total=800, folio_inicial=1):
    print(f"Iniciando generación de {cantidad_total} vales...")
    
    # Configuración Hoja
    hoja_ancho, hoja_alto = landscape(letter)
    c = canvas.Canvas(nombre_archivo, pagesize=landscape(letter))
    
    # Grilla
    filas = 4
    columnas = 2
    vales_por_hoja = filas * columnas
    
    # Calcular total de páginas necesarias
    total_paginas = math.ceil(cantidad_total / vales_por_hoja)
    
    # Márgenes y Escala
    margen_x = 0.5 * cm
    margen_y = 0.5 * cm
    ancho_celda = (hoja_ancho - 2*margen_x) / columnas
    alto_celda = (hoja_alto - 2*margen_y) / filas
    
    base_w = 19 * cm
    base_h = 6.5 * cm
    scale_w = (ancho_celda - 0.4*cm) / base_w 
    scale_h = (alto_celda - 0.2*cm) / base_h   
    scale_factor = min(scale_w, scale_h)

    folio_actual = folio_inicial
    vales_generados = 0

    # --- BUCLE PRINCIPAL DE PÁGINAS ---
    for pagina in range(total_paginas):
        
        # Dibujar la grilla de vales en esta página
        for fila in range(filas):
            for col in range(columnas):
                if vales_generados >= cantidad_total:
                    break # Parar si llegamos a 800 exactos aunque quede espacio en la hoja

                # Posición
                x_pos = margen_x + (col * ancho_celda)
                y_pos = hoja_alto - margen_y - ((fila + 1) * alto_celda)
                
                # Transformación y Dibujo
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
                vales_generados += 1

        # Dibujar Guías de Corte (Solo si hubo vales en esta página)
        c.setStrokeColor(blue)
        c.setLineWidth(0.5)
        long_guia = 0.4 * cm
        
        # Guías Horizontales
        for i in range(filas + 1):
            y = hoja_alto - margen_y - (i * alto_celda)
            c.line(margen_x - long_guia, y, margen_x + long_guia, y)
            c.line(hoja_ancho/2 - long_guia, y, hoja_ancho/2 + long_guia, y)
            c.line(hoja_ancho - margen_x - long_guia, y, hoja_ancho - margen_x + long_guia, y)

        # Guías Verticales
        for j in range(columnas + 1):
            x = margen_x + (j * ancho_celda)
            c.line(x, hoja_alto - margen_y + long_guia, x, hoja_alto - margen_y - long_guia)
            c.line(x, margen_y + long_guia, x, margen_y - long_guia)
            for i in range(1, filas):
                y_inter = hoja_alto - margen_y - (i * alto_celda)
                c.line(x, y_inter - long_guia, x, y_inter + long_guia)

        # ¡IMPORTANTE! Terminar la página actual y crear una nueva
        c.showPage()
        
        # Feedback en consola cada 10 páginas
        if (pagina + 1) % 10 == 0:
            print(f"Generando página {pagina + 1} de {total_paginas}...")

    c.save()
    print(f"¡PROCESO TERMINADO! Se generaron {vales_generados} vales en el archivo '{nombre_archivo}'.")

if __name__ == "__main__":
    # Aquí defines la cantidad total
    generar_lote_masivo("vales_800_completos.pdf", cantidad_total=800, folio_inicial=1)