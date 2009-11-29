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
# -config handling for servers and other clients
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


# FIX: get baseURL somehow...
sivu = ""
# handle the urls
path = ['']
if os.environ.has_key('PATH_INFO'):
   path = os.environ['PATH_INFO'].split('/')[1:]
   # print "Debug: path -> %s"% path

# contextRoot = os.environ['PATH_INFO']
contextRoot = "http://localhost/tommi/index.py"

#
#for param in os.environ.keys():
#    print "%20s %s" % (param,os.environ[param])

urls = {}
fs = cgi.FieldStorage(keep_blank_values=1)

# variable for debug message
# messag = "Debug: index.py call: urls[%s].doPage(%s) " % (path[0], path[:1])
messag = "Debug: index.py call: urls[%s].doPage(%s) " % (path[0], path[:1])
jj = 0
for hh in (path):
   messag = messag + "<br> param %s: %s " % (jj,hh)
   jj+=1

# Here we call the method to create a TeeKoneLista object, which has the information in
urls['/'] = sivuParseri.doBasicPage(contextRoot)
urls['konelista'] = sivuParseri.doMachineList(contextRoot)
urls['kone'] = sivuParseri.doMachineList(contextRoot)
urls['server'] = sivuParseri.doServerPage(contextRoot)
urls['config'] = sivuParseri.doConfigPage(contextRoot)
urls['savedata'] = sivuParseri.doSaveDataPage(contextRoot)
urls['debug'] = sivuParseri.doDebugPage(contextRoot, messag)
urls['error'] = sivuParseri.Error(contextRoot)

# if urls.has_key(path[0]):
if urls.has_key(path[0]):
   # Call the def_name.function
   #if path[0] == "server":
      # Special case, this needs also the servername
      #urls[path[0]].doPage(path[1:], path[2:])
   #else:
   #print "Debug: call: urls[%s].doPage(%s) " % (path[0], path[1:])

   # The debug way to call. Uncomment this to see first the debug, then
   # the normal page as.
   urls['debug'].doPage(path[1:], messag)

   # The normal way to call
   urls[path[0]].doPage(path[1:])

else:
   # print "Debug: Default action on index.py"
   # The debug way to call. Uncomment this to see first the debug, then
   # the normal page as.
   urls['debug'].doPage(path[1:], messag)

   # The normal way to call
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

