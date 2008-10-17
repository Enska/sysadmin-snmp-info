#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# Originaali versio 1.0 - Petteri Klemola
# Nykyinen versio 1.1 - Tommi Ruuth
#
# Saatu luvalla, otettu käyttöön soveltuvin osin ja muokattu edelleen. -TR 20081002
#
#import sys
import cgi
import os
import cgitb; cgitb.enable()
# Oma luokka, lainattu paaosin Petteri Klemolalta
import sivuParseri


sivu = ""
# handle the urls
path = ['']
if os.environ.has_key('PATH_INFO'):
   path = os.environ['PATH_INFO'].split('/')[1:]

urls = {}
fs = cgi.FieldStorage(keep_blank_values=1)
snmp = "testi"


urls['koneet'] = sivuParseri.TeeKoneLista(snmp)



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