#!/bin/bash

set -x
set -e


qty=280

name=vales_fest_voz

./run_python.sh src/gen_letter_2x4.py -c $qty -p "Te/Cafe" "Queque" "Pie/Kuchen" "Torta" -n ${name}_${qty}_cafeteria.pdf -o assets/img/logo_cpa.png -e assets/img/logo_fest_voz.png 


./run_python.sh src/gen_letter_2x4.py -c $qty -p Bebidas Completos Pizzetas Agua-Mineral -n ${name}_${qty}_comida.pdf -o assets/img/logo_cpa.png -e assets/img/logo_fest_voz.png 
