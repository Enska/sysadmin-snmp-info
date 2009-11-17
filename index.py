#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# Originaali versio 1.0 - Petteri Klemola
# Nykyinen versio 1.1 - Tommi Ruuth
#
# Saatu luvalla, otettu käyttöön soveltuvin osin ja muokattu edelleen. -TR 20081002
#

# TODO
# -snmpkyselyt -> ehkä cron-skripti?
# -asetusten hallinta ja taltiointi
# -inner links between pages
# -

#import sys
import cgi
import os
import cgitb; cgitb.enable()
# Oma luokka, lainattu paaosin Petteri Klemolalta
import sivuParseri

# Maaritellaan muutama hakemisto. joissa filuja pyöritellään
# Perushakemisto, jossa ollaan
#curdir=
# Jos tarvitaan temp-hakemistoa
#tmpdir=
# snmp-kyselyuden tuloksialle hakemisto
#snmpdir=

sivu = ""
# handle the urls
path = ['']
if os.environ.has_key('PATH_INFO'):
   path = os.environ['PATH_INFO'].split('/')[1:]
   # print "Debug: path -> %s"% path

urls = {}
fs = cgi.FieldStorage(keep_blank_values=1)
snmp = "testi"
turha= "joo"

# Here we call the method to create a TeeKoneLista object, which has the information in
urls['/'] = sivuParseri.teePerusSivu(turha)
urls['konelista'] = sivuParseri.teeKoneLista(snmp)
urls['kone'] = sivuParseri.teeKoneLista(snmp)
# urls['konelista'] = sivuParseri.teeKoneLista(snmp)
# print "Debug: path1: -> %s" % path[1:]
# print "Debug: urls -> %s" % urls

# if urls.has_key(path[0]):
if urls.has_key(path[0]):
   # Call the def_name.function
   print "Debug: call: urls[%s].doPage(path[1:]) "%  path[0]
   urls[path[0]].doPage(path[1:])
else:
   print "Debug: Default action on index.py"
   urls['/'].doPage()

# urls['konelista'].doPage()
# sivu = sivuParseri.TeeKoneLista()

# print "Debug: sivu ->", sivu
#urls['/'] = pageHandler.RenderPelikertaPage(db)
# urls['/'] = pageHandler.RenderPeliPage(db)

# sivu = urls['koneet']
# if urls.has_key(path[0]):
#    urls[path[0]].render(path[1:])
#else:
#    urls['/'].render()
#x = pageHandler.RenderPelikerrat().render()
#urls['pelaaja'] = renderPelaaja()
#urls['peli'] = renderPeli()
# print index