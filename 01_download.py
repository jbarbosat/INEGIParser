# coding:utf-8
# 19-feb-2014

# Esto descarga archivos TSV por entidad federativa de muchos temas,
# no sólo del censo, de la pág de descargas masivas de INEGI:
# http://www3.inegi.org.mx/sistemas/descarga/default.aspx?c=28088
# Requiero jqueries pero no lo sé usar así que... selenium + chrome
# Hay que vigilar este archivo cuando lo corremos xq a veces sale
# un mensajito de "El sitio está intentando descargar cosas. Permitir o Denegar?"
# Si no le picamos "Permitir" en cuanto sale (que es cuando intentamos bajar el
# segundo archivo), se hace un relajo. Después de picar "Permitir" ya no hay problema.
# Tarda como 15 minutos en correr


import codecs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from bs4 import BeautifulSoup
#import hadoopy
import html5lib
from time import sleep
import re


chromedriver = "/Users/PandoraMac/Documents/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

# Pág principal
driver.get("http://www3.inegi.org.mx/sistemas/descarga/default.aspx?c=28088")
# Nos aseguramos que sí sea el área de descarga masiva...
assert "Descarga masiva" in driver.title
# Click en "Por entidad federativa"
elem = driver.find_element_by_id('GV_Datos_ctl02_lnkArchivo')
elem.click()
sleep(10)
# Lista de estados y cositos. 
# todos son td's de class TdCenso y sus nombres son GV_Datos_ctl0x_updPanel 
# con x un numerín de 2 a 28
# Iteramos sobre ellos para darles click

estados = ['Nacional','Aguascalientes', 'Baja California', 'Baja California Sur','Campeche','Coahuila de Zaragoza',
	'Colima','Chiapas','Chihuahua','Distrito Federal','Durango','Guanajuato','Guerrero',
	'Hidalgo','Jalisco','México','Michoacán de Ocampo','Morelos','Nayarit','Nuevo León',
	'Oaxaca','Puebla','Querétaro','Quintana Roo','San Luis Potosí','Sinaloa','Sonora',
	'Tabasco','Tamaulipas','Tlaxcala','Veracruz de Ignacio de la Llave','Yucatán','Zacatecas']

# previos=['02','03','04','05']

# nombres=[]
# for num in ['06','07','08','09'] + range(10,39):
# 	nombres.append('GV_Datos_ctl'+str(num)+'_lnkArchivo')

nombres = []

for edo in estados:
	nombres.append()

for estado in nombres:
	# Picamos el nombre del estado
	elem = driver.find_element_by_id(estado)
	elem.click()
	sleep(10)
	# Bajamos el archivo tsv que es zip con notas y con los datos en un file separado x tabs
	elem = driver.find_element_by_link_text('GV_Datos_ctl03_lnkArchivo')
	elem.click()
	sleep(5)
	# Después de sacar la info de cada estado, click en Regresar
	elem = driver.find_element_by_id('GV_Datos_ctl02_lnkArchivo')
	elem.click()
	sleep(10)

# Un último sleep para que acabe de correr todo...
sleep(15)
driver.close()
