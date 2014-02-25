#!/bin/bash
#
# Descomprimir los TSV's que bajamos de INEGI
#
# Based on el trabajo de @rafaelcr (Rafael Cardenas)

echo "Descomprimiendo archivos de INEGI..."
DATOSDIR='/Users/PandoraMac/Downloads/'
DESTINODIR='/Users/PandoraMac/Documents/INEGIParser/datos'

cd $DATOSDIR

for z in *.zip; 
do
  dir=${z:0:(${#z}-4)}
  mkdir $DESTINODIR/$dir
  #echo $DESTINODIR/$dir
  unzip $z -d $DESTINODIR/$dir
  # rm $z
done