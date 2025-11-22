from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import black, blue

def dibujar_contenido_vale(c, folio):
    """
    Dibuja el contenido de un solo vale.
    Se asume que el canvas ya está trasladado (translate) y escalado
    a la posición correcta antes de llamar a esta función.
    Dimensiones base del diseño lógico: 20cm ancho x 7cm alto.
    """
    # --- VARIABLES DE DISEÑO (Coordenadas relativas al 0,0 del vale) ---
    ancho_logico = 20 * cm
    alto_logico = 7 * cm
    linea_corte_x = 5.0 * cm 
    
    # 1. TALÓN (IZQUIERDA)
    labels = ["Bebidas", "Completos", "Pizzetas"]
    y_base_items = 5.5 * cm
    
    c.setLineWidth(2)
    c.setStrokeColor(black)
    
    # Items Talón
    for i, label in enumerate(labels):
        y = y_base_items - (i * 1.2 * cm)
        c.rect(0.2*cm, y, 1.0*cm, 0.7*cm) # Cuadrito
        c.setFont("Helvetica", 9)
        c.drawString(1.4*cm, y+0.2*cm, label)

    # Checkboxes Pago Talón
    pagos = ["Efectivo", "Tarjeta", "Transf."] # Abreviado para espacio
    c.setFont("Helvetica", 6)
    c.setLineWidth(1)
    for i, pago in enumerate(pagos):
        bx = 0.2*cm + (i * 1.5*cm)
        by = 1.5*cm
        c.rect(bx, by, 0.25*cm, 0.25*cm)
        c.drawString(bx + 0.35*cm, by, pago)

    # Folio Vertical Talón
    c.saveState()
    c.translate(0.8*cm, 0.5*cm)
    c.rotate(90)
    c.setFont("Helvetica", 10)
    c.drawString(0, 0, f"Serie: {folio:04d}")
    c.restoreState()

    # Total Talón
    c.setFont("Helvetica", 10)
    c.drawString(1.5*cm, 0.5*cm, "Total: ______")

    # 2. LÍNEA DE CORTE PUNTEADA
    c.setLineWidth(1)
    c.setDash(4, 4)
    c.line(linea_corte_x, 0, linea_corte_x, alto_logico)
    c.setDash()

    # 3. CUERPO (DERECHA)
    margen_cuerpo = 6.0 * cm
    
    # Items Cuerpo (Más grandes)
    c.setLineWidth(2)
    for i, label in enumerate(labels):
        y = y_base_items - (i * 1.2 * cm)
        c.rect(margen_cuerpo, y, 1.5*cm, 0.8*cm)
        c.setFont("Helvetica", 14)
        c.drawString(margen_cuerpo + 1.8*cm, y+0.2*cm, label)

    # Checkboxes Pago Cuerpo
    c.setFont("Helvetica", 11)
    c.setLineWidth(1)
    pagos_full = ["Efectivo", "Tarjeta", "Transferencia"]
    for i, pago in enumerate(pagos_full):
        bx = margen_cuerpo + (i * 3.2*cm)
        by = 1.0*cm
        c.rect(bx, by, 0.5*cm, 0.5*cm)
        c.drawString(bx + 0.7*cm, by+0.15*cm, pago)

    # Folio y Total Cuerpo
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margen_cuerpo, 0.3*cm, f"Serie: {folio:04d}")
    c.drawString(margen_cuerpo + 3.5*cm, 0.3*cm, "TOTAL: ______________")

    # 4. LOGOS (Placeholders)
    # Logo Central (Círculo)
    c.setFillColorRGB(0.2, 0.3, 0.7) # Azul
    c.circle(linea_corte_x, 4.5*cm, 1.3*cm, fill=1, stroke=0)
    c.setFillColor(black)
    # AQUÍ PUEDES PONER: c.drawImage("logo.png", x, y, w, h...)

    # Logo Derecho (Festival)
    c.setFillColorRGB(1, 0.9, 0.8) # Beige
    c.rect(16*cm, 2*cm, 3*cm, 4.5*cm, fill=1, stroke=0) 
    c.setFillColorRGB(0.8, 0.2, 0.2)
    c.drawCentredString(17.5*cm, 4*cm, "FESTIVAL")
    c.setFillColor(black)


def generar_hoja_vales(nombre_archivo, folio_inicial=1):
    c = canvas.Canvas(nombre_archivo, pagesize=A4)
    ancho_pag, alto_pag = A4
    
    # Configuración de la grilla
    filas = 4
    columnas = 2
    
    # Márgenes de la página (para que no se corte al imprimir)
    margen_izq = 1.0 * cm
    margen_sup = 1.0 * cm
    
    # Tamaño de cada celda en la hoja
    ancho_celda = (ancho_pag - 2*margen_izq) / columnas
    alto_celda = (alto_pag - 2*margen_sup) / filas
    
    # Factor de escala (El diseño original era de 20cm, hay que reducirlo para que quepa en ~9.5cm)
    # ancho_celda es aprox 9.5cm. Diseño es 20cm. Escala aprox 0.47
    scale_factor = (ancho_celda - 0.5*cm) / (20*cm) 

    folio_actual = folio_inicial

    # DIBUJAR VALES
    for fila in range(filas):
        for col in range(columnas):
            # Calcular coordenadas de la esquina inferior izquierda de la celda
            x = margen_izq + (col * ancho_celda)
            # En PDF la Y crece hacia arriba, así que calculamos desde arriba hacia abajo
            y = alto_pag - margen_sup - ((fila + 1) * alto_celda)
            
            # Guardar estado antes de transformar
            c.saveState()
            
            # Mover el "cursor" a la posición de la celda y centrar un poco
            padding_x = 0.25 * cm
            padding_y = (alto_celda - (7*cm * scale_factor)) / 2 # Centrado vertical
            
            c.translate(x + padding_x, y + padding_y)
            c.scale(scale_factor, scale_factor)
            
            # Dibujar el vale
            dibujar_contenido_vale(c, folio_actual)
            c.restoreState()
            
            # Incrementar folio
            folio_actual += 1

    # DIBUJAR GUÍAS DE CORTE (CRUCES AZULES)
    c.setStrokeColor(blue)
    c.setLineWidth(0.5)
    long_guia = 0.5 * cm # Longitud de la patita de la cruz
    
    # Dibujar cruces en las intersecciones
    # Iteramos por las líneas divisorias
    for i in range(filas + 1): # Líneas horizontales (incluye bordes)
        y_linea = alto_pag - margen_sup - (i * alto_celda)
        
        for j in range(columnas + 1): # Líneas verticales
            x_linea = margen_izq + (j * ancho_celda)
            
            # Dibujar cruz (+)
            c.line(x_linea - long_guia, y_linea, x_linea + long_guia, y_linea) # Horizontal
            c.line(x_linea, y_linea - long_guia, x_linea, y_linea + long_guia) # Vertical

    c.save()
    print(f"Hoja generada: {nombre_archivo}")

if __name__ == "__main__":
    generar_hoja_vales("hoja_vales_festival.pdf", folio_inicial=1)# Ejecutar la función


