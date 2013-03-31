#!/usr/bin/python

"""Parser INEGI

Recibe un TSV de informacion de cierta Entidad Federativa y lo transmite hacia
una base de datos MongoDB.
http://www3.inegi.org.mx/sistemas/descarga/default.aspx?c=28088

Los nombres de archivos y directorios estan basados en la convencion de nombres
especificada por INEGI

"""

__author__ = '@rafaelcr (Rafael Cardenas)'

import csv
import sys

class INEGIParser(object):

  def __init__(self, directory):
    self.columnas = None
    self.entradas = {}
    self.notas = {}
    self.path = directory.strip('/')
    self.entidad = self.path.split('/')[-1:][0][:-3]
    self.parse()

  def parse(self):
    """Parsea los archivos hacia diccionarios.
    Hay ciertas inconsistencias en los nombres y cantidad de columnas entre
    archivos. Algunas de las siguientes lineas tratan de corregirlo.
    """
    with open('%s/%sNotas.tsv' % (self.path, self.entidad)) as inegi_tsv:
      for l, line in enumerate(csv.reader(inegi_tsv, dialect="excel-tab")):
        if l == 0 or len(line) == 1:
          continue
        self.notas[line[0]] = line[2]
    with open('%s/%sValor.tsv' % (self.path, self.entidad)) as inegi_tsv:
      for l, line in enumerate(csv.reader(inegi_tsv, dialect="excel-tab")):
        if not self.columnas:
          self.columnas = line
          continue
        self.parseline(line, 'valor')
    with open('%s/%sUnidadMedida.tsv' % (self.path, self.entidad)) as inegi_tsv:
      for l, line in enumerate(csv.reader(inegi_tsv, dialect="excel-tab")):
        if l==0:
          continue
        self.parseline(line, 'unidades')
    with open('%s/%sFuente.tsv' % (self.path, self.entidad)) as inegi_tsv:
      for l, line in enumerate(csv.reader(inegi_tsv, dialect="excel-tab")):
        if l == 0:
          continue
        self.parseline(line, 'fuente')

  def parseline(self, line, source):
    """Parsea una linea sencilla de TSV"""
    entrada = {}
    for i, val in enumerate(line):
      if val:
        if self.columnas[i].isdigit():
          entrada[self.columnas[i]] = {source: val}
        else:
          entrada[self.columnas[i]] = val
    self.organize(entrada, source)

  def organize(self, entrada, source):
    """Inserta lineas en el diccionario de entradas organizadamente.
    Llave primaria se compone de clave de municipio e ID de indicador"""
    key = '%s-%s' % (entrada['Cve_Municipio'], entrada['Id_Indicador'])
    if entrada['Id_Indicador'] in self.notas:
      entrada['Notas'] = self.notas[entrada['Id_Indicador']]
    if not (key in self.entradas):
      self.entradas[key] = entrada
    else:
      for k in entrada.iterkeys():
        if not (k in self.entradas[key]):
            self.entradas[key][k] = entrada[k]
        elif k.isdigit():
          self.entradas[key][k][source] = entrada[k][source]

def main():
  args = sys.argv[1:]
  if len(args) < 2:
    print 'usage: parse.py {--print | --dbhost [database hostname] \
--dbport [database port]} [directory...]'
    sys.exit(1)
  printd = False
  if args[0] == '--print':
    printd = True
    del args[0]

  p = INEGIParser(args[0])
  if printd:
    print p.entradas

if __name__ == '__main__':
  main()