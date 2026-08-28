#!/bin/bash

set -x
set -e


qty=120

name=vales_jamboree

#./run_python.sh src/gen_letter_2x4.py -c $qty -p "Te/Cafe" "Queque" "Pie/Kuchen" "Sopaipillas" -n ${name}_${qty}_cafeteria.pdf -o assets/img/logo_grupo_scout.png -e assets/img/logo_jamboree.png 


./run_python.sh src/gen_letter_2x4.py -c $qty -p "Lata_Bebida" "Completos" "Sin/Tomate" "Sin/Palta" -n ${name}_${qty}_completada.pdf -o assets/img/logo_grupo_scout.png -e assets/img/logo_jamboree.png -f 120
